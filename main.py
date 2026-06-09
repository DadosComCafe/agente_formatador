import streamlit as st
import pandas as pd

st.title("Agente Formatador")
uploaded_file = st.file_uploader("Arquivo a ser formatado!", type=["csv", "xls", "xlsx"])


if uploaded_file is not None:
    situacao = "Formatando..."
    
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    #st.subheader("Formatação atual:")
    #st.dataframe(df, width="stretch")
    
    st.subheader("Informações das colunas:")
    info_colunas = []
    for col in df.columns:
        info_colunas.append({
            "Coluna": col,
            "Formato": str(df[col].dtype)
        })
    df_info = pd.DataFrame(info_colunas)
    st.dataframe(df_info, hide_index=True)