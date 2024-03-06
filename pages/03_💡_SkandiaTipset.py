# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:20:41 2024

@author: LILJAC
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import plotly.graph_objects as go
import pickle
from scipy.optimize import minimize_scalar




# Streamlit app
def streamlit_app():
    # Display the initial section
    image = Image.open('Skandia2.png')
    st.image(image,width=700)
    st.title('Automatisk rådgivare')
    st.info('Fyll i nedan information för att förbättra din optimering')
    barn = st.radio('Har du ett eller flera barn?', ['Ja','Nej'])
    if barn == 'Ja':
        barn = 1
    else:
        barn = 0
    relation = st.radio('Har du en partner?', ['Ja','Nej'])
    if relation == 'Ja':
        relation = 1
    else:
        relation = 0
    lon = st.slider('Vad är din ungefärliga nettolön?', min_value=0, max_value=300000, value = 40000)
    current_balance = st.slider("Nuvarande sparkapital:", min_value=0, max_value=10000000, value = 100000)
    yearly_rate_of_return = 0.05
    current_age = st.slider("Nuvarande ålder:", min_value=20, max_value=80, value=25)
    retirement_age = st.slider("Önskad pensionsålder:", min_value=current_age+1, max_value=100, value=65)
    age_of_death = st.number_input("Ålder vid sista utbetalning:", value=100)
    desired_monthly_pension = st.number_input("Önskad månatlig pensionsutbetalning:", value=45000)
    current_private_savings = st.number_input("Nuvarande månadssparande (Pension + privat):", value=4000)
    investment_horizon_years = retirement_age - current_age
    months_after_retirement = (age_of_death - retirement_age) * 12

    def calculate_balance(current_balance, yearly_rate_of_return, current_monthly_savings, investment_horizon_years, months_after_retirement, desired_monthly_pension):
        # Calculate monthly parameters
            monthly_return_rate = yearly_rate_of_return / 12
            total_months = investment_horizon_years * 12
        
            # Initialize lists to store monthly data
            months = []
            balances = []
            
            # Calculate the balance for each month
            balance = current_balance
            for month in range(1, total_months + 1):
                # Calculate interest for the month
                interest = balance * monthly_return_rate
                # Add monthly savings
                balance += current_monthly_savings
                # Add interest to balance
                balance += interest
                # Store data for this month
                months.append(month)
                balances.append(balance)
            
            savings_at_retirement = balances[-1]
            for month in range(1, months_after_retirement + 1):
                savings_at_retirement -= desired_monthly_pension
                interest = savings_at_retirement * monthly_return_rate
                savings_at_retirement += interest
            
            return savings_at_retirement

    def objective_function(current_monthly_savings):
        return abs(calculate_balance(current_balance, yearly_rate_of_return, current_monthly_savings, investment_horizon_years, months_after_retirement, desired_monthly_pension))
    # Use scipy.optimize.minimize_scalar to find the minimum of the objective function
    result = minimize_scalar(objective_function)
    optimal_current_monthly_savings = result.x
    current_monthly_savings = round(optimal_current_monthly_savings)
    percentage = round((optimal_current_monthly_savings / current_private_savings) * 100)

    list_features = ['age', 'marital', 'has_children', 'salary_monthly']
    file_class = 'rf_model_class.sav'
    file_reg = 'rf_model_reg.sav'

    model_class = pickle.load(open(file_class, 'rb'))
    model_reg = pickle.load(open(file_reg, 'rb'))

    alder = current_age
    rel_status = relation
    har_barn = barn
    lon_manad = lon

    input = pd.DataFrame(np.array([[alder, rel_status, har_barn, lon_manad]]), columns=list_features)

    
    preds_class = model_class.predict(input) 
    preds_reg = model_reg.predict(input)
    preds_prob_class = model_class.predict_proba(input)

    bin_efterlevandeskydd, bin_lonevaxling, bin_halsoförsakring, bin_vardforsakring = preds_class[0]
    livforsakring, liv_link = preds_reg[0]
    arr_efterlevandeskydd, arr_lonevaxling, arr_halsoförsakring, arr_vardforsakring = preds_prob_class
    p_efterlevandeskydd = arr_efterlevandeskydd[0][1]
    p_lonevaxling = arr_lonevaxling[0][1]
    p_halsoförsakring = arr_halsoförsakring[0][1]
    p_vardforsakring = arr_vardforsakring[0][1]

    arr_lf = np.array([0,1000000,2000000])
    pos = np.argmin(abs(arr_lf - livforsakring))
    livforsakring = arr_lf[pos]
    arr_liv_link = np.array([0.5, 0.75, 1])
    pos = np.argmin(abs(arr_liv_link - liv_link))
    liv_link = arr_liv_link[pos]

    return current_monthly_savings, percentage, bin_efterlevandeskydd, bin_lonevaxling, bin_halsoförsakring, bin_vardforsakring, livforsakring, liv_link, current_private_savings, p_efterlevandeskydd, p_halsoförsakring, p_vardforsakring, p_lonevaxling

if __name__ == "__main__":
    current_monthly_savings, percentage, bin_efterlevandeskydd, bin_lonevaxling, bin_halsoförsakring, bin_vardforsakring, livforsakring, liv_link, current_private_savings, p_efterlevandeskydd, p_halsoförsakring, p_vardforsakring, p_lonevaxling=streamlit_app()

def create_progress_bar(progress_value, produkt):
    # Create a figure for the progress bar
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=progress_value,
        title={'text': f"{produkt}"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkgreen"},
               'bgcolor': "white",
               'steps': [
                   {'range': [0, 100], 'color': 'lightgreen'}
               ]}
    ))

    # Update layout for the figure
    fig.update_layout(
        autosize=False,
        width=200,
        height=200,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    return fig
# Function to create an Indicator figure
def create_indicator(value, reference,produkt, show_delta=False):
    delta_config = {'reference': reference, 'relative': False} if show_delta else None

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value,
        title={"text": f"{produkt}"},
        delta=delta_config,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        autosize=False,
        width=200,
        height=200,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    return fig

value_1 = round(liv_link*100)
reference_1 = 100
value_2 = round((1-liv_link)*100)
reference_2 = 0
value_3 = current_monthly_savings
reference_3 = current_private_savings
value_4 = livforsakring
reference_4 = 1000000

fig1 = create_indicator(value_1, reference_1, '% Traditionell',show_delta=True)
fig2 = create_indicator(value_2, reference_2, '% Fondförsäkring',show_delta=True)
fig3 = create_indicator(value_3, reference_3, 'Sparande kr',show_delta=True)
fig8 = create_indicator(value_4, reference_4, 'Livförsäkring',show_delta=True)


progress_value_1 = round(p_efterlevandeskydd,2)
progress_value_2 = round(p_halsoförsakring,2)
progress_value_3 = round(p_vardforsakring,2)
progress_value_4 = round(p_lonevaxling,2)

fig4 = create_progress_bar(progress_value_1*100, 'Efterlevandeskydd %')
fig5 = create_progress_bar(progress_value_2*100, 'Hälsoförsäkring %')
fig6 = create_progress_bar(progress_value_3*100, 'Vårdförsäkring %')
fig7 = create_progress_bar(progress_value_4*100, 'Löneväxling %')
if st.button('Starta rådgivningsprocess'):
    
        # Show a spinner during a process
        with st.spinner(text='Hämtar din information...'):
            time.sleep(3)
            st.warning('Förbereder rekomendationer baserat på din livssituation och dina nuvarande försäkringar...')
            
            # Show and update progress bar
            bar = st.progress(50)
            time.sleep(5)
            bar.progress(100)
        st.info('Nedan finner du dina nuvarande försäkringslösningar')
        with st.container():
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            col7, col8, col9 = st.columns(3)  # Second row of columns
            
            # Add metrics to each column
            col1.metric('% Traditionell', 100)
                
            col2.metric('% Fondförsäkring',0)
            
            col3.metric('Sparande kr', current_private_savings)
                
            
            
            # Metrics for the second row
            halso = 'Ja'
            col4.metric("Efterlevandeskydd", "Ja")
        
            col5.metric("Hälsoförsäkring", "Nej")
        
            col6.metric("Vårdförsäkring", "Nej")
    
            col7.metric("Löneväxling", "Nej")
        
            col8.metric("Livförsäkring", f"{1000000:,} kr")

        bar = st.progress(50)
        time.sleep(5)
        bar.progress(100)
        st.balloons()
        st.toast('Hooray!', icon='🎉')
        st.success('Hurra! Vi har tagit fram rekomenderade produkter och sparstrategier som vi tror passar dig!')


        
        with st.container():
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            col7, col8, col9 = st.columns(3)  # Second row of columns
            

            # Display the indicators in Streamlit using columns layout manager
            
            with col1:
                st.plotly_chart(fig1)
            with col2:
                st.plotly_chart(fig2)
            with col3:
                st.plotly_chart(fig3)
            
            
            # Metrics for the second row
            if bin_efterlevandeskydd == 1:
                with col1:
                #col4.metric("Efterlevandeskydd", "Ja")
                    st.plotly_chart(fig4)
                    st.write("⬆️ Andel som valt **Efterlevandeskydd**")
            else:
                #col4.metric("Efterlevandeskydd", "Nej")
                with col1:
                    st.plotly_chart(fig4)
                    st.write("⬆️ Andel som valt **Efterlevandeskydd**")
            if bin_halsoförsakring == 1:
                with col2:
                    st.plotly_chart(fig5)
                    st.write("⬆️ Andel som valt **Hälsoförsäkring**")
                #col5.metric("Hälsoförsäkring", "Ja", '😲', help = "Hoppsan! Du har visst inte en hälsoförsäkring, vill du veta mer? [Läs mer här!](https://www.skandia.se/foretag/tips-for-foretagare/tips-for-foretagare/10-bra-skal-till-att-skaffa-en-halsoforsakring/)")
                #st.write("Hoppsan! Du har visst inte en hälsoförsäkring, vill du veta mer? [Läs mer här!](https://www.skandia.se/foretag/tips-for-foretagare/tips-for-foretagare/10-bra-skal-till-att-skaffa-en-halsoforsakring/)")
            else:
                with col2:
                    st.plotly_chart(fig5)
                    st.write("⬆️ Andel som valt **Hälsoförsäkring**")
                #col5.metric("Hälsoförsäkring", "Nej",  help = "De flesta med liknande profiler som dig har valt att inte teckna en hälsoförsäkring, vi rekommenderar dig däremot att teckna försäkringen. [Läs mer här!](https://www.skandia.se/foretag/tips-for-foretagare/tips-for-foretagare/10-bra-skal-till-att-skaffa-en-halsoforsakring/)")
            if bin_vardforsakring == 1:
                with col3:
                    st.plotly_chart(fig6)
                    st.write("⬆️ Andel som valt **Vårdförsäkring**")
                #col6.metric("Vårdförsäkring", "Ja", '😲', help = "Hoppsan! Du har visst inte en vårdförsäkring, vill du veta mer? [Läs mer här!](https://www.skandia.se/forsakra/privata-personforsakringar/vardforsakring/)")
            else:
                 with col3:
                    st.plotly_chart(fig6)
                    st.write("⬆️ Andel som valt **Vårdförsäkring**")
                #col6.metric("Vårdförsäkring", "Nej",  help = "De flesta med liknande profiler som dig har valt att inte teckna en vårdförsäkring, vi rekommenderar dig däremot att teckna försäkringen. [Läs mer här!](https://www.skandia.se/forsakra/privata-personforsakringar/vardforsakring/)")
            if bin_lonevaxling == 1:
                 with col7:
                    st.plotly_chart(fig7)
                    st.write("⬆️ Andel som valt att **Löneväxla**")
                #col7.metric("Löneväxling", "Ja", '😲', help = "Hoppsan! Du löneväxlar inte, vill du veta mer? [Läs mer här!](https://www.skandia.se/spara-pension/pension/tjanstepension/guide/lonevaxla/)")
                #st.write("Hoppsan! Du löneväxlar inte, vill du veta mer? [Läs mer här!](https://www.skandia.se/spara-pension/pension/tjanstepension/guide/lonevaxla/)")
            else:
                with col7:
                    st.plotly_chart(fig7)
                    st.write("⬆️ Andel som valt att **Löneväxla**")
            with col8:
                st.plotly_chart(fig8)
            #col8.metric("Livförsäkring", f"{livforsakring:,} kr", f"{((livforsakring/1000000)-1)*100} %")


