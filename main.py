import streamlit as st
import pandas as pd

situacao = "Aguardando..."
st.title("Agente Formatador")
uploaded_file = st.file_uploader("Arquivo a ser formatado!", type=["csv", "xls", "xlsx"])
st.text(situacao)

if uploaded_file is not None:
    situacao = "Formatando..."#entender como eu apago o texto anterior
    st.text(uploaded_file.type)
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        print(df.keys())
        st.table(df)