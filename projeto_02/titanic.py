import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

dataset = pd.read_csv('titanic3.csv')

print(dataset.head())