import streamlit as st
from PIL import Image
import plotly.graph_objects as go


st.set_page_config(
    page_title="Om SkandiaTipset",
    page_icon="👋",
)

st.write("# Funderar du på hur SkandiaTipset fungerar?")

st.markdown(
    """
    SkandiaTipset är en maskininlärningsmodell som föreslår försäkring- och pensionssprodukter baserat på vad Skandiakunder i din livssituation har tecknat. Modellen är tränad på ett dataset som är noga utvalt av oss på Skandia. Samtliga kunder har varit på rådgivningsmöte och har gjort sina val tillsammans med en rådgivare. På så vis har modellen blivit skolad av våra duktiga rådgivare här på Skandia!    
    
"""
)
image = Image.open('radgivning3.png')
st.image(image,width=700)
