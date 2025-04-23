import pandas as pd
import streamlit as st
import plotly.express as px

# Título da página
st.title("Análise de Acidentes de Trânsito por Estado")

# Carregar datasets
@st.cache_data
def carregar_dados():
    df_acidentes = pd.read_csv("./acidentes_2022.csv", low_memory=False)
    df_localidades = pd.read_csv("./localidades_2022.csv")
    return df_acidentes, df_localidades

df_acidentes, df_localidades = carregar_dados()

# Verificar colunas disponíveis (debug)
st.sidebar.subheader("Colunas disponíveis (debug)")
if st.sidebar.checkbox("Ver colunas dos arquivos"):
    st.sidebar.write("📄 Acidentes:", df_acidentes.columns.tolist())
    st.sidebar.write("📄 Localidades:", df_localidades.columns.tolist())

# Menu lateral para seleção de estado
estados_disponiveis = sorted(df_acidentes['uf_acidente'].unique())
estado_selecionado = st.sidebar.selectbox("Selecione o Estado", ["Todos os Estados"] + estados_disponiveis)

# Filtrar os dados pelo estado selecionado ou mostrar todos os acidentes
if estado_selecionado == "Todos os Estados":
    df_acidentes_estado = df_acidentes
    df_localidades_estado = df_localidades
else:
    df_acidentes_estado = df_acidentes[df_acidentes['uf_acidente'] == estado_selecionado]
    df_localidades_estado = df_localidades[df_localidades['uf'] == estado_selecionado]

# Agrupar dados de acidentes por município
df_acidentes_por_cidade = df_acidentes_estado.groupby('codigo_ibge').size().reset_index(name='total_acidentes')

# Selecionar colunas que existem
colunas_desejadas = ['codigo_ibge', 'municipio', 'qtde_habitantes', 'frota_total']
colunas_presentes = [col for col in colunas_desejadas if col in df_localidades_estado.columns]
municipios_unicos = df_localidades_estado[colunas_presentes].drop_duplicates(subset='codigo_ibge')

# Mesclar
df_acidentes_por_cidade = pd.merge(df_acidentes_por_cidade, municipios_unicos, on='codigo_ibge', how='left')

# Calcular indicadores, com proteção contra ausência de colunas
if 'qtde_habitantes' in df_acidentes_por_cidade.columns:
    df_acidentes_por_cidade['total_acidentes_por_mil_habitantes'] = (
        df_acidentes_por_cidade['total_acidentes'] / df_acidentes_por_cidade['qtde_habitantes'].replace({0: None}) * 1000
    )
else:
    df_acidentes_por_cidade['total_acidentes_por_mil_habitantes'] = None

if 'frota_total' in df_acidentes_por_cidade.columns:
    df_acidentes_por_cidade['total_acidentes_por_mil_veiculos'] = (
        df_acidentes_por_cidade['total_acidentes'] / df_acidentes_por_cidade['frota_total'].replace({0: None}) * 1000
    )
else:
    df_acidentes_por_cidade['total_acidentes_por_mil_veiculos'] = None

top5_por_habitante = df_acidentes_por_cidade.sort_values(by='total_acidentes_por_mil_habitantes', ascending=False).head(5)
top5_por_veiculo = df_acidentes_por_cidade.sort_values(by='total_acidentes_por_mil_veiculos', ascending=False).head(5)

if df_acidentes_por_cidade['total_acidentes_por_mil_habitantes'].notna().any():
    st.header(f'Top 5 por mil habitantes em {estado_selecionado}' if estado_selecionado != "Todos os Estados" else "Top 5 por mil habitantes")
    fig2 = px.bar(top5_por_habitante, x='municipio', y='total_acidentes_por_mil_habitantes', color='total_acidentes_por_mil_habitantes')
    st.plotly_chart(fig2)
else:
    st.warning("Dados de habitantes não disponíveis para este estado.")

if df_acidentes_por_cidade['total_acidentes_por_mil_veiculos'].notna().any():
    st.header(f'Top 5 por mil veículos em {estado_selecionado}' if estado_selecionado != "Todos os Estados" else "Top 5 por mil veículos")
    fig3 = px.bar(top5_por_veiculo, x='municipio', y='total_acidentes_por_mil_veiculos', color='total_acidentes_por_mil_veiculos')
    st.plotly_chart(fig3)
else:
    st.warning("Dados de frota de veículos não disponíveis para este estado.")

# Mapa
st.header(f"Mapa dos acidentes em {estado_selecionado}" if estado_selecionado != "Todos os Estados" else "Mapa de todos os acidentes")
if 'latitude_acidente' in df_acidentes_estado.columns and 'longitude_acidente' in df_acidentes_estado.columns:
    mapa_dados = df_acidentes_estado[['latitude_acidente', 'longitude_acidente']].dropna()
    mapa_dados.columns = ['latitude', 'longitude']  # renomear para que o st.map entenda
    if not mapa_dados.empty:
        st.map(mapa_dados)
    else:
        st.warning("Coordenadas vazias para este estado.")
else:
    st.warning("Colunas de latitude e longitude não estão disponíveis no dataset.")
