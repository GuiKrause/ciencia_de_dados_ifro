import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('titanic3.csv', sep=";")
    return df

df = load_data()

# Sidebar com filtros
st.sidebar.title("Filtros")
sexo = st.sidebar.multiselect("Sexo", options=df['sex'].dropna().unique(), default=df['sex'].dropna().unique())
classe = st.sidebar.multiselect("Classe (pclass)", options=sorted(df['pclass'].dropna().unique()), default=sorted(df['pclass'].dropna().unique()))
sobrevivente = st.sidebar.multiselect("Sobrevivência", options=[0, 1], default=[0, 1])

# Aplicar filtros
df_filtered = df[
    (df['sex'].isin(sexo)) &
    (df['pclass'].isin(classe)) &
    (df['survived'].isin(sobrevivente))
]

# Visão Geral dos Dados
st.title("Quem Sobreviveu no Titanic?")
st.subheader("1. Visão Geral dos Dados")

st.write(f"Número total de passageiros: {df_filtered.shape[0]}")
taxa_sobrevivencia = df_filtered['survived'].value_counts(normalize=True).rename({0: 'Não Sobreviveu', 1: 'Sobreviveu'})
st.write("Taxa de sobrevivência:")
st.write(taxa_sobrevivencia.map(lambda x: f"{x:.1%}"))

# Dados Ausentes
st.subheader("2. Dados Ausentes")
missing = df_filtered.isnull().sum()
missing_percent = (missing / df_filtered.shape[0]) * 100
missing_data = pd.DataFrame({'Total': missing, 'Percentual': missing_percent})
st.dataframe(missing_data[missing_data['Total'] > 0])

# Visualizações
st.subheader("3. Análises Visuais")

# Sobrevivência por Sexo
st.write("Sobrevivência por Sexo")
fig1 = px.histogram(df_filtered, x='sex', color='survived', barmode='group',
                    category_orders={"survived": [0, 1]},
                    labels={'survived': 'Sobreviveu'})
st.plotly_chart(fig1)

# Sobrevivência por Classe
st.write("Sobrevivência por Classe (pclass)")
fig3 = px.histogram(df_filtered, x='pclass', color='survived', barmode='group',
                    category_orders={"pclass": [1, 2, 3]},
                    labels={'survived': 'Sobreviveu'})
st.plotly_chart(fig3)

# Sexo + Classe vs Sobrevivência
st.write("Sobrevivência por Sexo e Classe")
fig4 = px.histogram(df_filtered, x='sex', color='survived', barmode='group',
                    facet_col='pclass', category_orders={"pclass": [1, 2, 3]},
                    labels={'survived': 'Sobreviveu'})
st.plotly_chart(fig4)