# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:59:46 2024

@author: LILJAC
"""
from turtle import color
import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import plotly.graph_objects as go
# Function to calculate the future balance
def calculate_balance(current_balance, expected_yearly_return, monthly_savings, investment_horizon_years, time_to_pension):
    # Calculate monthly parameters
    monthly_return_rate = expected_yearly_return / 12
    total_months = investment_horizon_years * 12
    
    # Initialize lists to store monthly data
    months = []
    balances = []
    cumulative_savings = []
    
    # Calculate the balance for each month
    balance = current_balance
    savings = current_balance
    for month in range(1, total_months + 1):
        # Calculate interest for the month
        interest = balance * monthly_return_rate
        # Add monthly savings
        balance += monthly_savings
        savings += monthly_savings
        # Add interest to balance
        balance += interest
        # Store data for this month
        months.append(month)
        balances.append(balance)
        cumulative_savings.append(savings)
    
    return months, balances, cumulative_savings

# Streamlit app
def main():
    st.title('Sparkalkylator')
    st.info('Testa vår sparkalkylator för att räkna ut ditt framtida kapital!')
    
    # Sidebar for input parameters
    st.sidebar.header('Input Sparparametrar')
    
    # Slider for expected yearly return
    expected_yearly_return = st.sidebar.slider('Förväntad avkastning (%)', min_value=0.1, max_value=20.0, value=6.0, step=0.1)
    
    # Slider for monthly savings
    monthly_savings = st.sidebar.slider('Månadssparande (kr)', min_value=0, max_value=25000, value=1500, step=100)
    
    # Slider for investment horizon
    investment_horizon_years = st.sidebar.slider('Investeringshorisont (År)', min_value=1, max_value=50, value=15, step=1)
    
    # Slider for investment horizon
    time_to_pension = st.sidebar.slider('Tid till pension (År)', min_value=1, max_value=55, value=15, step=1)
    
    # Input for current balance
    current_balance = st.number_input('Nuvarande saldo (kr)', min_value=0)
    
    # Calculate balance
    months, balances, cumulative_savings = calculate_balance(current_balance, expected_yearly_return / 100, monthly_savings, investment_horizon_years, time_to_pension)
    df = pd.DataFrame({'Månader': months, 'Sparkapital (kr)': balances, 'Sparande (kr)': cumulative_savings})
    st.metric("Värde", f"{round(balances[-1]):,} kr")
    
    # Plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=balances, fill='tozeroy', mode='lines', name='Endast sparande', fillcolor='lightgreen'))
    fig.add_trace(go.Scatter(x=months, y=cumulative_savings, fill='tonexty', mode='lines', name='Sparande med avkastning', fillcolor='darkgreen'))
    fig.add_shape(type='line', x0=time_to_pension*12, y0=df[['Sparkapital (kr)', 'Sparande (kr)']].min().min(), x1=time_to_pension*12, y1=df[['Sparkapital (kr)', 'Sparande (kr)']].max().max(), line=dict(color='black', width=2, dash='dash'))
    fig.update_layout(title='Sparkapital över tid', xaxis_title='Månader', yaxis_title='Sparkapital (kr)', font=dict(size=12, color='black', family='Arial, sans-serif'), title_font=dict(size=14, color='black', family='Arial, sans-serif'))
    st.plotly_chart(fig)

main()

