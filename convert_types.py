import streamlit as st
import pandas as pd
from utils import handle_file

st.title("Agente Formatador")
uploaded_file = st.file_uploader("Arquivo a ser formatado!", type=["csv", "xlsx", "zip"])
if uploaded_file:
    if uploaded_file.type != "application/zip":
        df = handle_file(uploaded_file)

        st.subheader("Formatação atual:")
        st.dataframe(df, width="stretch")
        
        st.subheader("Escolha o formato de cada coluna:")
        
        formatos_escolhidos = {}
        tipos_saida = [".xlsx", ".csv"]

        #for tipo in tipos_saida:
        st.markdown(f"Tipo de arquivo a ser exportado:")
        formato_tipo = st.radio(
            "Formato:",
            options=tipos_saida,
            index=None,
            horizontal=True,
            key=f"saida"

        )

        if formato_tipo:
            #formato_saida[tipo] = formato_tipo
            st.success(f"{formato_tipo}")
        else:
            st.info(f"formato de saída não definido")
        st.divider()


        for col in df.columns:
            primeiro_valor = df[col].iloc[0] if len(df) > 0 else None
            
            st.markdown(f"**{col}** (exemplo: `{primeiro_valor}`)")
            
            formato_colunas = st.radio(
                "Formato:",
                options=["str", "int", "float", "date"],
                index=None,
                horizontal=True,
                key=f"formato_{col}"
            )

            if formato_colunas:
                formatos_escolhidos[col] = formato_colunas
                st.success(f"{col} → {formato_colunas}")
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
                if formato_tipo == ".csv":
                    df_converted.to_csv("converted_data.csv")
                else:
                    df_converted.to_excel("converted_data.xlsx")
                
                st.subheader("Tipos finais:")
                tipos_final = {col: str(df_converted[col].dtype) for col in df_converted.columns}
                st.json(tipos_final)
            else:
                st.warning("Nenhum formato selecionado! Escolha o formato de pelo menos uma coluna.")
        
        edited_df = st.data_editor(df, num_rows="dynamic")
        st.data_editor(df, key="my_key", num_rows="dynamic")