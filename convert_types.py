import streamlit as st
import pandas as pd
from typing import List
import zipfile
#from datetime import date

def handle_zip_file(zipado: str) -> List[pd.DataFrame]:
    with zipfile.ZipFile(zipado, "r") as zf:
        list_types = [file.split(".")[-1] for file in zf.namelist()]
        if len(list_types) > 1:
            print("Há arquivos em formatos distintos no zip!")
            return False
        
        for file in zf.namelist():
            ...

        

            


def handle_file(file: str) -> pd.DataFrame:
    if file.split(".")[-1] == "csv":
        return pd.read_csv(file)
    
    if file.split(".")[-1] in ["xlsx", "xls"]:
        return pd.read_excel(file)
    
    if file.split(".")[-1] == "zip":
        return handle_zip_file(file)

st.title("Agente Formatador")
uploaded_file = st.file_uploader("Arquivo a ser formatado!", type=["csv", "xls", "xlsx", "zip"])



if uploaded_file is not None:
    if uploaded_file.type == "application/zip":

    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("Formatação atual:")
    st.dataframe(df, width="stretch")
    


    st.subheader("Escolha o formato de cada coluna:")
    


    formatos_escolhidos = {}
    
    for col in df.columns:
        primeiro_valor = df[col].iloc[0] if len(df) > 0 else None
        
        st.markdown(f"**{col}** (exemplo: `{primeiro_valor}`)")
        
        formato = st.radio(
            "Formato:",
            options=["str", "int", "float", "date"],
            index=None,
            horizontal=True,
            key=f"formato_{col}"
        )
        
        if formato:
            formatos_escolhidos[col] = formato
            st.success(f"{col} → {formato}")
        else:
            st.info(f"{col} → formato não definido")
        st.divider()
    
    if st.button("Converter dados conforme formatos selecionados", type="primary"):
        if formatos_escolhidos:
            df_converted = df.copy()
            
            for col, formato_escolhido in formatos_escolhidos.items():
                if col in df_converted.columns:
                    try:
                        if formato_escolhido == "int":
                            df_converted[col] = pd.to_numeric(df_converted[col], downcast="integer")
                        elif formato_escolhido == "float":
                            df_converted[col] = pd.to_numeric(df_converted[col], downcast="float")
                        elif formato_escolhido == "str":
                            df_converted[col] = df_converted[col].astype(str)
                        elif formato_escolhido == "date":
                            df_converted[col] = pd.to_datetime(df_converted[col]).dt.date
                        
                        st.success(f"Convertido '{col}' para {formato_escolhido}")
                    except Exception as e:
                        st.error(f"Erro ao converter '{col}' para {formato_escolhido}: {e}")
            
            st.subheader("Dados convertidos:")
            st.dataframe(df_converted, width="stretch")
            
            df_converted.to_csv("converted_data.csv")
            
            st.subheader("Tipos finais:")
            tipos_final = {col: str(df_converted[col].dtype) for col in df_converted.columns}
            st.json(tipos_final)
        else:
            st.warning("Nenhum formato selecionado! Escolha o formato de pelo menos uma coluna.")
    
    edited_df = st.data_editor(df, num_rows="dynamic")
    st.text("Teste")
    st.data_editor(df, key="my_key", num_rows="dynamic")
    st.write("Here's the value in Session State:")
    st.write(st.session_state["my_key"])