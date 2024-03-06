import streamlit as st
import pandas as pd

st.write("# Välkommen till din behörighetsdashboard!")
st.markdown(
    """
    Här kan du begränsa företags behörighet till din försäkringsdata.
"""
)

LIST_COMPANIES = ['Nordea', 'Handelsbanken', 'Folksam', 'Alecta', 'SEB', 'Länsförsäkringar']

# Define paths or URLs to the logos
LOGO_PATHS = {
    'Nordea': 'nordea.png',
    'Handelsbanken': 'handelsbanken.png',
    'Folksam': 'folksam.png',
    'Alecta': 'alecta.png',
    'SEB': 'seb.png',
    'Länsförsäkringar': 'lf.png'
}

comp_remove = st.multiselect('Ta bort behörigheter för följande företag:', LIST_COMPANIES)

if len(comp_remove) == 0:
    st.write('Företag som har behörighet till din försäkringsdata:')
    df = pd.DataFrame(LIST_COMPANIES, columns=['Företag'])
    for index, row in df.iterrows():
        st.image(LOGO_PATHS[row['Företag']], width=100)
        st.write(row['Företag'])
if len(comp_remove) > 0:
    list_companies_v2 = LIST_COMPANIES.copy()
    st.write('**Du har tagit bort behörigheter för följande företag**:')
    for comp in comp_remove:
        st.write(comp)
        list_companies_v2.remove(comp)
    st.write('**Företag som har behörighet till din försäkringsdata**:')
    df = pd.DataFrame(list_companies_v2, columns=['Företag'])
    for index, row in df.iterrows():
        st.image(LOGO_PATHS[row['Företag']], width=100)
        st.write(row['Företag'])
    



