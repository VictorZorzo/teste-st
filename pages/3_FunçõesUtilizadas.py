import streamlit as st

code = '''def DBCreation():
    conn = sqlite3.connect('DataBase.db')
    
    ano = 2023

    while ano >= 2018:

        df = pd.read_csv(filepath_or_buffer='C:\\Users\\Victor\\Documents\\GitHub\\teste2.1\\ComponentesTarifarias'+str(ano)+'.csv')

        df = df.loc[::, ('SigNomeAgente',
                        'DatInicioVigencia', 
                        'DscBaseTarifaria',
                        'DscSubGrupoTarifario',
                        'DscModalidadeTarifaria',
                        'DscClasseConsumidor',
                        'DscSubClasseConsumidor',
                        'DscUnidade',
                        'DscComponenteTarifario',
                        'VlrComponenteTarifario'
                    )]

        df = df[(df['DscSubGrupoTarifario'] == 'B1') &
                (df['DscModalidadeTarifaria'] == 'Convencional') &
                (df['DscBaseTarifaria'] == 'Tarifa de Aplicação') &
                (df['DscSubClasseConsumidor'] == 'Residencial') &
                (df['DscComponenteTarifario'].isin(['TUSD', 'TE', 'TUSD_FioB']))
                ]

        df.to_sql('tusdte'+str(ano), conn, if_exists='replace', index=False)

        ano = ano -1

    df_irradsolloc = pd.read_csv(filepath_or_buffer='C:\\Users\\Victor\\Documents\\GitHub\\teste2.1\\global_horizontal_means.csv', delimiter= ';')

    df_irradsolloc = df_irradsolloc.loc[::, 'LON':'DEC']

    df_irradsolloc.to_sql('irradsolloc', conn, if_exists='replace', index=False)

    conn.close()

def QueryVlrkWh(SigNomeAgente, icms, pis, cofins):
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor() 

    vlrkwhlist = []

    df = []

    anos = []

    ano = 2018  

    while ano <= 2023:

        table = 'tusdte'+str(ano)  
    
        sqlquery = (f"SELECT * FROM {table} WHERE SigNomeAgente LIKE ?")

        c.execute(sqlquery, (SigNomeAgente+'%',))

        results = c.fetchall()

        columns = [desc[0] for desc in c.description]  

        Df = pd.DataFrame(results, columns=columns)

        df.append(Df)

        row = Df.loc[Df['DscComponenteTarifario'] == 'TUSD']

        tusd= 0

        for i in row['VlrComponenteTarifario'].str.replace(',','.').values:
            if i != '0' and float(i) > tusd:
                tusd = float(i)

        row = Df.loc[Df['DscComponenteTarifario'] == 'TE']

        te = 0

        for i in row['VlrComponenteTarifario'].str.replace(',','.').values:
            if i != '0' and float(i) > te:
                te = float(i)

        #row = df.loc[df['DscComponenteTarifario'] == 'TUSD_FioB']

        #tusdb = 0

        #for i in row['VlrComponenteTarifario'].str.replace(',','.').values:
        #    if i != '0' and float(i) > 0:
        #        tusdb = float(i)

        VlrkWh = ((te + tusd) / ((1-icms) * (1-(pis + cofins)) * 1000))

        vlrkwhlist.append(VlrkWh)

        anos.append(str(ano))

        ano = ano +1

    conn.close()

    df = pd.concat(df, ignore_index=True)

    vlrkwh = pd.DataFrame(data= vlrkwhlist, index= anos, columns= ['vlrkwh'] )

    line = 0

    diff_list = []

    while line < 5:
        diff = vlrkwh.iloc[line + 1, 0] / vlrkwh.iloc[line, 0]
        if diff > 1: 
            diff_list.append(diff)
        line = line + 1

    Diff = round(sum(diff_list)/len(diff_list), 4)

    return vlrkwh, df, Diff

def CalcGer(end, cons, Vlrkwp):
    geolocator = Nominatim(user_agent='victor.ynz28@gmail.com')
    location = geolocator.geocode(end)
    
    conn = sqlite3.connect('DataBase.db')
    c = conn.cursor()     
    
    sqlquery = ("""SELECT * FROM irradsolloc""")

    c.execute(sqlquery)

    results = c.fetchall()

    columns = [desc[0] for desc in c.description]  

    df = pd.DataFrame(results, columns=columns)
    
    df['closeness'] = abs(df['LON']- location.longitude) + abs(df['LAT'] - location.latitude)

    df = df.sort_values(by='closeness')

    df = df.loc[::, 'ANNUAL': 'DEC']

    pt = pd.DataFrame(df.iloc[0])

    modulo = 2.279*1.134

    area = cons / ((pt.iloc[0].item() * 0.2 * (365/12)) / 10**3) 

    qtd_modulo = round(int(area / modulo) + 0.6)

    ger = ((pt * 0.2 * (365/12)) * round(int(qtd_modulo * modulo) + 0.6)) / 10**3

    finalvalue = round((qtd_modulo * 0.55 * Vlrkwp), 2)
   
    return finalvalue, ger, qtd_modulo

def CalRet(Ret, End, Cons, Conc, Icms, Pis, Cofins, Vlrkwp):

    finalvalue, ger, qtd_modulo = CalcGer(end= End, cons= Cons, Vlrkwp= Vlrkwp)

    vlrkwh, df, Diff = QueryVlrkWh(SigNomeAgente= Conc , icms= Icms, pis= Pis, cofins= Cofins)

    Vlrkwh = vlrkwh.iloc[5,0]

    Annual_Ajust = Diff
        
    Annual_Generation = round((ger.iloc[0] * 12), 2)

    Annual_Return = Annual_Generation * (Vlrkwh)

    line = 0

    found = 0

    while line < len(Ret):
        if line == 0:
            Ret.iloc[line, 0] = Annual_Return - finalvalue
            line = line +1
        else:
            Annual_Return = Annual_Return * Annual_Ajust
            Ret.iloc[line, 0] = Ret.iloc[line - 1, 0]  + Annual_Return 
            line = line + 1
            if Ret.iloc[line -1, 0] > 0 and found == 0:
                Tret = Ret.iloc[line -1,::]
                found = 1

    return Ret, Vlrkwh, Tret, Diff

'''

st.code(body= code)