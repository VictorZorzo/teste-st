import streamlit as st

st.set_page_config(initial_sidebar_state= 'expanded', menu_items= {'About': 'https://github.com/VictorZorzo/teste-st'})

st.markdown(
    """
    ### Bem Vindo à Plataforma de Predição de Valores para Sistemas de Energia Solar no Brasil!
    ## Os Principais Objetivos Deste Projeto São:
    - Obter os valores das Componentes Tarifárias que compõem o valor do kWh cobrado por cada concessionária de energia do Brasil;
    - Com base nestes calcular o valor do kWh cobrado por cada concessionária, assumindo valores aproximados para os impostos envolvidos(ICMS, PIS/PASEP, COFINS);
    - Com base nos valores referentes aos anos anteriores, calcular a taxa de aumento médio do valor do kWh para cada Concessionária;
    - Obter os valores de Irradiação Solar mensais para todo o Brasil e ,com base no endereço provido, descobrir os valores para o local em questão;
    - Levando em consideração Valores Padrão de eficiencia e dimensão para módulos fotovoltaicos, calcular a quantidade necessária de módulos para suprir o consumo provido;
    - Com base na potência de pico total do sistema e levando em consideração valores aproximados para o custo do kWp praticado no mercado Brasileiro, calcular o custo total do sistema;
    - A parir dos valores obtidos (valor do kWh, Taxa de aumento deste, geração mensal e valor total do sistema), calcular o tempo estimado para o retorno do investimento inicial.
    ## Este Projeto Não Contempla:
    - Simulações Para Grupos Tarifários Diferentes do B1;
    - Implementação dos valores relativos ao FIO B no cálculo de retorno;
    - Valores precisos para impostos ICMS, PIS/PASEP, COFINS, para maior precisão insira os valores específicos para seu Estado;
    - Implementação dos valores de COSIP no cálculo de retorno.
"""
)