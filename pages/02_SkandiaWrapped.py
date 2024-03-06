# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:09:12 2024

@author: LILJAC
"""

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_lchart_card import streamlit_lchart_card
import plotly.graph_objects as go
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from random import randint
import streamlit as st
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
import time
import math
import pydeck as pdk
def rose():
    option = {
            "legend": {"top": "bottom"},
            "toolbox": {
                "show": True,
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True},
                },
            },
            "series": [
                {
                    "name": "面积模式",
                    "type": "pie",
                    "radius": [50, 250],
                    "center": ["50%", "50%"],
                    "roseType": "area",
                    "itemStyle": {"borderRadius": 8},
                    "data": [
                        {"value": 40, "name": "rose 1"},
                        {"value": 38, "name": "rose 2"},
                        {"value": 32, "name": "rose 3"},
                        {"value": 30, "name": "rose 4"},
                        {"value": 28, "name": "rose 5"},
                        {"value": 26, "name": "rose 6"},
                        {"value": 22, "name": "rose 7"},
                        {"value": 18, "name": "rose 8"},
                    ],
                }
            ],
        }
    st_echarts(
            options=option, height="600px",
        )
    
def liquid():
    liquidfill_option = {
    "series": [{"type": "liquidFill", "data": [0.6, 0.5, 0.4, 0.3]}]}
    st_echarts(liquidfill_option)

def evo():
    option_evolution = {
    "title": {"text": "Kapitalutveckling"},
    "legend": {"data": ['2022', '2023']},
    "toolbox": {
        "feature": {
            "magicType": {"type": ['stack']},
            "dataView": {},
            "saveAsImage": {"pixelRatio": 2}
        }
    },
    "tooltip": {},
    "xAxis": {"data": ['A' + str(i) for i in range(100)], "splitLine": {"show": False}},
    "yAxis": {},
    "series": [
        {
            "name": '2022',
            "type": 'bar',
            "data": [((math.sin(i / 5) * (i / 5 - 10) + i / 6) * 5) for i in range(100)],
            "emphasis": {"focus": 'series'},
            "animationDelay": "function (idx) {return idx * 10;}"
        },
        {
            "name": '2023',
            "type": 'bar',
            "data": [((math.cos(i / 5) * (i / 5 - 10) + i / 6) * 5) for i in range(100)],
            "emphasis": {"focus": 'series'},
            "animationDelay": "function (idx) {return idx * 10 + 100;}"
        }
    ],
    "animationEasing": 'elasticOut',
    "animationDelayUpdate": "function (idx) {return idx * 5;}"
}
    st_echarts(option_evolution, height="800px")

def cards():
    t = pd.date_range(start=datetime(year=2023, month=1, day=1),
                    end=datetime(year=2024, month=1, day=1), freq="1m")
#%%
    
    temps = [210, 201.35, 225.23, 210.12, 233.12, 229.12, 225.12, 233.12, 243.12, 238.12, 236.12, 231.12]
    pHs =  [240, 201.35, 265.3, 210.12, 233.12, 300.5, 225.12, 233.12, 243.12, 310.2, 215.5, 240.5]
    nitrates = [110, 215.35, 225.23, 240.12, 233.12, 269.12, 225.12, 273.12, 243.12, 288.12, 256.12, 210.12]
    ammonias = [210, 256.35, 276.23, 288.12, 280.12, 276.12, 265.12, 270.12, 275.12, 280.12, 281.12, 265.12]
    water_levels = [210, 233.35, 288.23, 255.12, 258.12, 277.12, 243.12, 244.12, 229.12, 238.12, 258.12, 265.12]
    #%%
    df_temps = pd.DataFrame({"date": t, "measure": temps})
    df_pHs = pd.DataFrame({"date": t, "measure": pHs})
    df_nitrates = pd.DataFrame({"date": t, "measure": nitrates})
    df_ammonias = pd.DataFrame({"date": t, "measure": ammonias})
    df_water_levels = pd.DataFrame({"date": t, "measure": water_levels})

    multiple_graphs = st.columns(4)
    with multiple_graphs[0]:
        streamlit_lchart_card(title="Skandia Time Global", df=df_temps, x="date", y="measure",
                            labels={"date": "Date"}, defaultColor="rgb(255, 180, 15)", rounding=1, format="%d/%m", thresh=f"{round(((df_temps['measure'].iloc[-1]/df_temps['measure'].iloc[0])-1)*100)} %")
    with multiple_graphs[1]:
        streamlit_lchart_card(title="Länsförsäkringar Global", df=df_nitrates, x="date", y="measure",thresh = f"{round(((df_nitrates['measure'].iloc[-1]/df_nitrates['measure'].iloc[0])-1)*100)} %",
                            labels={"date": "Date"}, defaultColor="rgb(132, 99, 255)",
                            rounding=2, format="%d/%m")
    with multiple_graphs[2]:
        streamlit_lchart_card(title="AMF Sverige Index", df=df_pHs, x="date", y="measure",thresh = f"{round(((df_pHs['measure'].iloc[-1]/df_pHs['measure'].iloc[0])-1)*100)} %",
                            labels={"date": "Date"}, defaultColor="rgb(99, 255, 132)",
                            rounding=2, format="%d/%m")
    with multiple_graphs[3]:
        streamlit_lchart_card(title="Spiltan Småbolag", df=df_ammonias, x="date", y="measure",thresh = f"{round(((df_ammonias['measure'].iloc[-1]/df_ammonias['measure'].iloc[0])-1)*100)} %",
                            labels={"date": "Date"}, defaultColor="rgb(90, 90, 90)",
                            rounding=2, format="%d/%m")
        
    #%%


    b = (
        Bar()
        .add_xaxis(["Skandia Time Global", "Länsförsäkringar Global", "AMF Sverige Index", "Spiltan Småbolag"])
        .add_yaxis(
            "2023-2024 Innehav i (%)", [33, 27, 25, 20],
            itemstyle_opts=opts.ItemStyleOpts(color="green")  # Set color of bars to green
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Din fördelning av fonder", subtitle="2017-2018 Fördelning"
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )

    st_pyecharts(b)

def skandia_map():
    # Sample data for heatmap
    heatmap_data = {
        'latitude': [0, -1, 5, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, -15, -6, 10, 11, 12, -22],  # Latitude values for the countries you want to highlight
        'longitude': [20, 25, 30, 22, 23, 24, 21, 22, 23, 24, 25, 26, 27, 27, 35, 8, 9, 3, 17],  # Longitude values for the countries you want to highlight
    }

    # Create DataFrame from sample data
    heatmap_df = pd.DataFrame(heatmap_data)

    # Define the initial view state for Africa
    view_state = pdk.ViewState(
        latitude=0,  # Centered around the equator
        longitude=20,  # Centered around the middle of Africa
        zoom=3,  # Zoom level
        pitch=50  # Angle to view the map
    )

    # Custom color palette for the heatmap (more green)
    custom_color_palette = [
        [0, 128, 0],    # Dark green
        [0, 255, 0],    # Green
        [173, 255, 47], # Green yellow
    ]

    # Create a PyDeck map centered over Africa with custom styling
    map = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",  # Change the map style (dark theme)
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=heatmap_df,
                get_position=["longitude", "latitude"],
                radius=50000,  # Adjust the radius size as needed
                intensity=1,  # Adjust the intensity of the heatmap
                color_range=custom_color_palette,  # Apply custom color palette
            ),
        ]
    )

    # Render the map in Streamlit
    st.pydeck_chart(map)

def branch():
    options = {
    "title": {"text": "Pensionskälla"},
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "cross",
            "label": {"backgroundColor": "#6a7985"},
        },
    },
    "legend": {"data": ["Privat pension", "Premiepension", "Inkomstpension", "Tjänstepension"]},
    "toolbox": {"feature": {"saveAsImage": {}}},
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": [
        {
            "type": "category",
            "boundaryGap": False,
            "data": ["2017", "2018", "2019", "2020", "2021", "2022", "2023"],
        }
    ],
    "yAxis": [{"type": "value"}],
    "series": [
        {
            "name": "Privat pension",
            "type": "line",
            "stack": "Branch",
            "areaStyle": {},
            "data": [15, 5, 30, 30, 15, 25, 20],
        },
        {
            "name": "Premiepension",
            "type": "line",
            "stack": "Branch",
            "areaStyle": {},
            "data": [20, 20, 20, 10, 5, 10, 8],
        },
        {
            "name": "Inkomstpension",
            "type": "line",
            "stack": "Branch",
            "areaStyle": {},
            "data": [35, 40, 25, 40, 45, 40, 45],
        },
        {
            "name": "Tjänstepension",
            "type": "line",
            "stack": "Branch",
            "areaStyle": {},
            "data": [30, 35, 25, 20, 35, 25, 27],
        },
        
    ],
}
    st_echarts(options)
def costum_pie():
    option_custom_pie = {
    "tooltip": {
        "trigger": 'item',
        "formatter": '{a} <br/>{b}: {c} ({d}%)'
    },
    "legend": {
        "data": [
        'USA',
        'Sverige',
        'Asien',
        'Industri',
        'Finans',
        'Teknik',
        'Hållbarhet',
        'AI',
        'Råvaror',
        'Övrigt'
        ]
    },
    "series": [
        {
        "name": 'Access From',
        "type": 'pie',
        "selectedMode": 'single',
        "radius": [0, '30%'],
        "label": {
            "position": 'inner',
            "fontSize": 14
        },
        "labelLine": {
            "show": False
        },
        "data": [
            { "value": 1548, "name": 'USA' },
            { "value": 775, "name": 'Sverige', "selected": True  },
            { "value": 679, "name": 'Asien'}
        ]
        },
        {
        "name": 'Andel',
        "type": 'pie',
        "radius": ['45%', '60%'],
        "labelLine": {
            "length": 30
        },
        "label": {
            "formatter": '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
            "backgroundColor": '#F6F8FC',
            "borderColor": '#8C8D8E',
            "borderWidth": 1,
            "borderRadius": 4,
            "rich": {
            "a": {
                "color": '#6E7079',
                "lineHeight": 22,
                "align": 'center'
            },
            "hr": {
                "borderColor": '#8C8D8E',
                "width": '100%',
                "borderWidth": 1,
                "height": 0
            },
            "b": {
                "color": '#4C5058',
                "fontSize": 14,
                "fontWeight": 'bold',
                "lineHeight": 33
            },
            "per": {
                "color": '#fff',
                "backgroundColor": '#4C5058',
                "padding": [3, 4],
                "borderRadius": 4
            }
            }
        },
        "data": [
            { "value": 1048, "name": 'Hållbarhet' },
            { "value": 335, "name": 'Industri' },
            { "value": 310, "name": 'Finans' },
            { "value": 251, "name": 'Teknik' },
            { "value": 234, "name": 'AI' },
            { "value": 147, "name": 'Råvaror' },
            { "value": 135, "name": 'Kommunikation' },
            { "value": 102, "name": 'Övrigt' }
        ]
        }
    ]
    }
    st_echarts(option_custom_pie, height="800px")

def single_bar():
    options = {
    "xAxis": {
        "type": "category",
        "data": ["2017", "2018", "2019", "2020", "2021", "2022", "2023"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": [
                120,
                200,
                220,
                145,
                170,
                210,
                {"value": 280, "itemStyle": {"color": "#006400"}},
            ],
            "type": "bar",
        }
    ],
}
    st_echarts(
    options=options,
    height="400px",
)
#-----------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("Välkommen till Skandia  Wrapped!")
if st.button("Se ditt pensionsår!"):
    progress_text = "Skapar ditt Skandia Wrapped"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    #st.success('Så har ditt pensionssparande sett ut under året!', icon="💲")
    st.markdown("<h1 style='text-align: center; color: green;'>Så har ditt pensionssparande sett ut under året! 💲</h1>", unsafe_allow_html=True)
#--------------------------------------------------------------------------------------
    st.metric("Pensionskapital", f"Under 2023 sparade du: {280000} kr", "11%")

    progress_text = "Så har ditt sparande utveklats:"
    single_bar()
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    #st.success('Så såg fördelningen av ditt sparande ut', icon="📊")
    st.markdown("<h1 style='text-align: center; color: green;'>Så såg fördelningen av ditt sparande ut 📊</h1>", unsafe_allow_html=True)
    branch()
#-----------------------------------------------------------------------------------------

if st.button("Så ser dina innehav ut!"):
    progress_text = "Analyserar dina innehav..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    #st.success('Så har dina fonder presterat under året', icon="📈")
    st.markdown("<h1 style='text-align: center; color: green;'>Så har dina fonder presterat under året 📈</h1>", unsafe_allow_html=True)

    cards()
    #st.success('Så har dina fonder presterat i jämförelse med 2022', icon="🏆")
    st.markdown("<h1 style='text-align: center; color: green;'>Så har dina fonder presterat i jämförelse med 2022 📈</h1>", unsafe_allow_html=True)
    evo()
    #st.success('Så har du fördelat pengarna mellan olika brancher', icon="⚖️")
    st.markdown("<h1 style='text-align: center; color: green;'>Så har du fördelat pengarna mellan olika brancher ⚖️</h1>", unsafe_allow_html=True)
    costum_pie()
#_---------------------------------------------------------------------------------------
if st.button("Så hållbara är dina investeringar"):
    progress_text = "Analyserar hållbarheten i dina investeringar..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    #st.success('Dina investeringar bidrog med att reningen av Östersjön ökade med...', icon="💧")
    st.markdown("<h1 style='text-align: center; color: green;'>Dina investeringar bidrog med att reningen av Östersjön ökade med... 💧</h1>", unsafe_allow_html=True)
    st.balloons()
    liquid()
    #st.success('Dina investeringar bidrog även med gröna avtryck i...', icon="🌱")
    st.markdown("<h1 style='text-align: center; color: green;'>Dina investeringar bidrog även med gröna avtryck i... 🌱</h1>", unsafe_allow_html=True)
    skandia_map()



#----------------------------------------------------------------------------------------------------------
# Define the data
import pandas as pd
import streamlit as st

# Sample data
data = {
    'Country': ['China', 'India', 'Japan', 'South Korea', 'Pakistan', 
                'Indonesia', 'Bangladesh', 'Philippines', 'Vietnam', 'Turkey'],
    'CaseCount': [1000, 2500, 800, 1200, 600, 1500, 700, 900, 1000, 2000],
    'Region': ['Asia'] * 10,
    'lat': [35.8617, 20.5937, 36.2048, 35.9078, 30.3753, -0.7893, 23.6850, 12.8797, 14.0583, 38.9637],  # Dummy latitude values
    'lon': [104.1954, 78.9629, 138.2529, 127.7669, 69.3451, 113.9213, 90.3563, 121.7740, 108.2772, 35.2433]  # Dummy longitude values
}




