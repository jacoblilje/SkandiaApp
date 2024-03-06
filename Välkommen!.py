import streamlit as st
import streamlit as st
import numpy as np
import pandas as pd
import subprocess

try:
  # replace "yourpackage" with the package you want to import
  import streamlit as st
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

# This block executes only on the first run when your package isn't installed
except ModuleNotFoundError as e:
  subprocess.open([f'{sys.executable} -m pip install git+https://${{token}}@github.com/jacoblilje/SkandiaApp.git'], shell=True)
  # wait for subprocess to install package before running your actual code below
  time.sleep(90)
import streamlit as st
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

st.set_page_config(
    page_title="Om SkandiaTipset",
    page_icon="👋",
)

st.write("# Välkommen till SkandiaTipset! 👋")
st.video("https://www.youtube.com/watch?v=whpZ7x8jtRo")


st.markdown(
    """
    Här kan du få tips på försäkring- och pensionssprodukter baserat på vad Skandiakunder i din livssituation har tecknat. Du kan också se vilka företag som har behörighet till din försäkringsdata. 
    👈 Nyfiken? 
    - Gå till **SkandiaTipset** för att använda få en snabb rådgivning baserat på livssituation och befintliga försäkringar.
    - Gå till **Behörighetsdashboard** för att se över vilka företag om har behörighet till din försäkringsdata. 
    - Gå till **Sparkalkylatorn** för att se hur ditt sparkapital utvecklas med tiden. Har du hört talas om ränta-på-ränta effekten? [Titta på det här!](https://www.youtube.com/watch?v=_SB3an68ZiI)

"""
)
