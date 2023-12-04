import streamlit as st
import pandas as pd

from Functions import CalcGer, CalRet

st.set_page_config(initial_sidebar_state= 'expanded', layout= 'wide')

endereço = st.sidebar.text_input(label= '1-Endereço', value='Rua Endereço, 123', placeholder= 'Rua Endereço, 123')
consumo = st.sidebar.number_input(label= '2-Consumo (kWh)', value= 0, placeholder= 0)
concessionaria = st.sidebar.text_input(label= '3-Concessionária')

Parametros = st.sidebar.expander(label='Parâmetros')

tab1, tab2 = st.tabs(['Geração', 'Retorno'])

icms, pis, cofins = [0.12, 0.65, 3]

vlrkwp = 3500

with Parametros:
    icms = (st.number_input(label= 'ICMS - %',  value= 12)) / 100

    pis = (st.number_input(label= 'PIS/PASEP - %',  value= 0.65)) / 100

    cofins = (st.number_input(label= 'COFINS - %',  value= 3.0)) / 100

    vlrkwp = st.number_input(label= 'Valor do kWp - R$',  value= 3500)

with tab1:

    st.header('Geração Mensal Estimada')

    ger = pd.DataFrame(index= ('ANNUAL','JAN','FEV','MAR','ABR','JUN','JUL','AGO','SET','OUT','NOV','DEC'), data= {'GER':(0,0,0,0,0,0,0,0,0,0,0,0)})

    if concessionaria == '': 
        
        st.bar_chart( data = ger)

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(label= 'Quantidade de Módulos', value= '')

        with col2:

            st.text_input(label= 'Valor Estimado', value= '')

        
    if consumo != 0 and endereço != 'Rua Endereço, 123' and concessionaria != '':
           
        finalvalue, ger, qtd_modulo = CalcGer(end= endereço, cons= consumo, Vlrkwp= vlrkwp)

        st.bar_chart( data = ger)

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(label= 'Quantidade de Módulos', value= qtd_modulo)

        with col2:
            
            st.text_input(label= 'Valor Estimado', value= 'R$' + '  ' + str(finalvalue))


with tab2:

    st.header('Cálculo de Retorno Financeiro Estimado')

    ret = pd.DataFrame(index= ('2024','2025','2026','2027','2028','2029','2030','2031','2032','2033','2034'), data= {'GER':(0,0,0,0,0,0,0,0,0,0,0)})

    if concessionaria == '':
        col1, col2 = st.columns(2)

        with col1:

            st.text_input(label='Valor do kWh em 2023')

        with col2:

            st.text_input(label= 'Aumento Anual Médio')

        st.bar_chart(ret)

        st.text_input(label= 'Retorno do Investimento Estimado para')

        
    if consumo != 0 and endereço != 'Rua Endereço, 123' and concessionaria != '':

        ret, Vlrkwh, tret, Diff = CalRet(Ret= ret, Cons= consumo, End= endereço, Conc= concessionaria, Icms= icms, Pis= pis, Cofins= cofins, Vlrkwp= vlrkwp)

        diff = round(((Diff*100)-100), 2)

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(label='Valor do kWh em 2023', value= 'R$'+''+str(Vlrkwh))

        with col2:
            st.text_input(label= 'Aumento Anual Médio', value= str(diff)+'%')
      
        st.bar_chart(ret)

        st.text_input(label= 'Retorno do Investimento Estimado para', value= tret.name) 

        