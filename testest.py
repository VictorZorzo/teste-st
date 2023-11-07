import streamlit as st
import pandas as pd
import time
from geopy.geocoders import Nominatim

Endereço = st.sidebar.text_input(label= 'Endereço')
Consumo = st.sidebar.number_input(label= 'Consumo')

while Consumo > 0 and Endereço.strip():
    time.sleep(1)

    geolocator = Nominatim(user_agent='victor.ynz28@gmail.com')
    location = geolocator.geocode(Endereço)

    df = pd.read_csv(delimiter= ';', filepath_or_buffer='C:\\Users\\Victor\\Documents\\GitHub\\teste2.1\\global_horizontal_means.csv')

    df['closeness'] = abs(df['LON']- location.longitude) + abs(df['LAT'] - location.latitude)

    df = df.sort_values(by='closeness')

    df = df.loc[::, 'ANNUAL': 'DEC']

    pt = pd.DataFrame(df.iloc[0])

    modulo = 2.279*1.134

    area = Consumo / ((pt.iloc[0].item() * 0.2 * (365/12)) / 10**3) 

    qtd_modulo = round(int(area / modulo) + 0.6)

    gr = ((pt * 0.2 * (365/12)) * round(int(qtd_modulo * modulo) + 0.6)) / 10**3

    st.header('Geração Mensal Estimda')

    st.bar_chart( data = gr)

    st.text_input(label= 'Quantidade de Módulos', value= qtd_modulo)

    st.text_input(label= 'Valor Estimado', value= 'R$' + '  ' + str(qtd_modulo * 0.55 * 3500))

    Consumo = 0