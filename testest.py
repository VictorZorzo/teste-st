import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim

st.set_page_config(initial_sidebar_state= 'expanded', layout= 'wide')

End = 'Rua Endereço, 123'
Con= 0

Endereço = st.sidebar.text_input(label= 'Endereço', value= End, placeholder= End)
Consumo = st.sidebar.number_input(label= 'Consumo (kWh)', value= Con, placeholder= Con)

tab1, tab2 = st.tabs(['Geração', 'Retorno'])

with tab1:

    st.header('Geração Mensal Estimada')

    ger = pd.DataFrame(index= ('ANNUAL','JAN','FEV','MAR','ABR','JUN','JUL','AGO','SET','OUT','NOV','DEC'), data= {'GER':(0,0,0,0,0,0,0,0,0,0,0,0)})

    qtd_modulo = ""

    finalvalue = ""


    if Consumo == 0: 
        
        st.bar_chart( data = ger)

        st.text_input(label= 'Quantidade de Módulos', value= qtd_modulo)

        st.text_input(label= 'Valor Estimado', value= finalvalue)

        
    if Consumo != Con and Endereço != End:
            
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

        ger = ((pt * 0.2 * (365/12)) * round(int(qtd_modulo * modulo) + 0.6)) / 10**3

        FinalValue = qtd_modulo * 0.55 * 3500

        finalvalue= 'R$' + '  ' + str(FinalValue)

        st.bar_chart( data = ger)

        st.text_input(label= 'Quantidade de Módulos', value= qtd_modulo)

        st.text_input(label= 'Valor Estimado', value= finalvalue)


with tab2:

    st.header('Cálculo de Retorno Financeiro Estimado')

    ret = pd.DataFrame(index= ('2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033'), data= {'GER':(0,0,0,0,0,0,0,0,0,0,0)})

    if Consumo == 0:

        st.bar_chart(ret)

    if Consumo != Con and Endereço != End:

        kWh_Cost = 0.79

        Annual_Ajust = 1.07
        
        Annual_Generation = (ger.iloc[0] * 12)

        Annual_Return = Annual_Generation * (kWh_Cost)

        line = 0

        while line < len(ret):
            if line == 0:
                ret.iat[line, 0] = Annual_Return - FinalValue
                line = line +1
            else:
                ret.iat[line, 0] = ret.iat[line - 1, 0]  + (Annual_Return * Annual_Ajust) 
                line = line + 1
      
        st.bar_chart(ret)