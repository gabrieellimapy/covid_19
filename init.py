# ---------------------------------- PROJETO --------------------------------- #

# -------- Neste projeto vamos trabalhar sobre os seguintes requisitos ------- #
# ------------ 1 - Exibir as regiões do Brasil com casos de covid ------------ #
# --------------------- 2 - Exibir as datas dos registros -------------------- #
# --------------- 3 - Exibir resultado acumulado de novos casos -------------- #
# -------------- 4 - Exibir resultado acumulado de novos óbitos -------------- #
# ----------------- 5 - Exibir dado acumulado de recuperações ---------------- #

# ---------------------- Colunas escolhidas do dataframe --------------------- #
#regiao, estado, municipio, data, casosAcumulado, obitosAcumulado, Recuperadosnovos

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------- Carregando os dados --------------------------- #

covid_1 = pd.read_csv('dados\covid_2020_1.csv', sep=';')
covid_2 = pd.read_csv('dados\covid_2020_2.csv', sep=';')
covid_3 = pd.read_csv('dados\covid_2021_1.csv', sep=';')
covid_4 = pd.read_csv('dados\covid_2021_2.csv', sep=';')
covid_5 = pd.read_csv('dados\covid_2022_1.csv', sep=';')
covid_6 = pd.read_csv('dados\covid_2022_2.csv', sep=';')
covid_7 = pd.read_csv('dados\covid_2023_1.csv', sep=';')

# -------------------------- concatenando databases -------------------------- #
database = pd.concat([covid_1,
                      covid_2,
                      covid_3,
                      covid_4,
                      covid_5,
                      covid_6,
                      covid_7], ignore_index= True)

# ----------- Ajustando apenas para as colunas que serão utilizadas ---------- #

database = database.loc[:, ['regiao','estado','municipio','data','casosAcumulado','obitosAcumulado', 'Recuperadosnovos']]

# ----------- Ajustando para dados diferentes do Brasil (sintético) ---------- #
# ------------------------ Redefinindo índices também ------------------------ #

database = database.query('regiao != "Brasil"')
database.reset_index(drop = True, inplace=True)

# ------------------ Alterando dados nulos para não definido ----------------- #

database.loc[:, ['estado', 'municipio']] = database.loc[:, ['estado', 'municipio']].fillna('Não definido')

# -------------- Alterando tipagem de dados para algumas colunas ------------- #
database['casosAcumulado'] = database['casosAcumulado'].astype(int)

# ---------------- Ajustando valores das colunas por 0 ou nulo --------------- #

database[['estado', 'municipio']] = database[['estado', 'municipio']].fillna('Não definido')

# ------------ Convertendo valores de data nas colunas respectivas ----------- #

database['data'] = pd.to_datetime(database['data'])

# --------------- Criando colunas MM/AA/DD/HH para controle de dados --------------- #

database['mes'] = database['data'].dt.month
database['ano'] = database['data'].dt.year
database['dia'] = database['data'].dt.day

# ---------------- Definindo dicionários para os meses do ano ---------------- #

meses = {
    1: 'Jan',
    2: 'Fev',
    3: 'Mar',
    4: 'Abr',
    5: 'Mai',
    6: 'Jun',
    7: 'Jul',
    8: 'Ago',
    9: 'Set',
    10: 'Out',
    11: 'Nov',
    12: 'Dez'
}


# --------------------------- Retirando duplicidade -------------------------- #
database = database.drop_duplicates(subset=['estado','casosAcumulado'])

# ------------- Gerando gráfico de progressão por região do país ------------- #

df_grouped = database.groupby(['regiao', 'ano', 'mes'])['casosAcumulado'].sum().reset_index()
df_grouped['mes'] = df_grouped['mes'].apply(lambda x: meses[x])

sns.set_style('whitegrid')
plt.figure(figsize=(15, 8))
sns.barplot(data=df_grouped, x='mes', y='casosAcumulado', hue='regiao', palette='bright')
plt.title('Casos acumulados de COVID-19 por mês e região do Brasil')
plt.xlabel('Mês')
plt.ylabel('Casos acumulados')
plt.legend(loc='upper left')
plt.show()