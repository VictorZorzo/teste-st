import streamlit as st

from Functions import QueryVlrkWh

st.set_page_config(initial_sidebar_state= 'expanded', layout= 'wide')

concessionaria = st.sidebar.text_input(label= 'Concessionária')

Icms = (st.sidebar.number_input(label= 'ICMS - %', placeholder= 12, value= 12)) / 100

Pis = (st.sidebar.number_input(label= 'PIS/PASEP - %', placeholder= 0.65, value= 0.65)) / 100

Cofins = (st.sidebar.number_input(label= 'COFINS - %', placeholder= 3.0, value= 3.0)) / 100

if concessionaria == '':
    st.header('Escolha Uma Concessionária Para Realizar a Pesquisa')  

if concessionaria != '':    
    
    Vlrkwh, df, Diff = QueryVlrkWh(SigNomeAgente= concessionaria, icms= Icms, pis= Pis, cofins= Cofins )

    diff = round(((Diff*100)-100), 2)

    st.dataframe(df, height= 200)

    col1, col2 = st.columns([0.8,0.2])

    with col1:
        st.line_chart(Vlrkwh)

    with col2:
        st.dataframe(Vlrkwh)

        st.text_input(label= 'Aumento Anual Médio', value= str(diff)+'%')
