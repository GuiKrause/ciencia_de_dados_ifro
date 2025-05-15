import pandas as pd
import streamlit as st

dataset = pd.read_csv("./acidentes_2022.csv")

st.title("Exemplo de Dataframe de Acidentes")

st.write("Aqui estão nossos dados:")

dataset = dataset[dataset['uf_acidente'] == 'RO']

st.dataframe(dataset)