import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mapeador de Tipos de CSV", layout="wide")

st.title("Mapeador de Tipos de Colunas")
st.write("Faça do CSV, verifique os tipos detectados e defina os novos tipos desejados.")

# 1. Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, nrows=5)
    
    st.success("CSV carregado com sucesso!")
    
    opcoes_tipos = ["Texto (str)", "Inteiro (int)", "Decimal (float)", "Booleano (bool)", "Data/Hora (datetime)"]
    
    # Mapeamento interno para o dicionário final
    mapa_conversao = {
        "Texto (str)": "str",
        "Inteiro (int)": "int",
        "Decimal (float)": "float",
        "Booleano (bool)": "bool",
        "Data/Hora (datetime)": "datetime"
    }

    st.divider()
    

    col_nome, col_tipo_original, col_novo_tipo = st.columns([2, 2, 3])
    with col_nome:
        st.markdown("**Nome da Coluna**")
    with col_tipo_original:
        st.markdown("**Tipo Detectado**")
    with col_novo_tipo:
        st.markdown("**Selecione o Novo Tipo**")
        
    st.divider()

    for coluna in df.columns:
        tipo_original = str(df[coluna].dtype)
        
        c_nome, c_orig, c_novo = st.columns([2, 2, 3])
        
        with c_nome:
            st.text(coluna)
            
        with c_orig:
            st.code(tipo_original, language="text")
            
        with c_novo:
            escolha = st.selectbox(
                f"Tipo para {coluna}",
                options=opcoes_tipos,
                label_visibility="collapsed",
                key=f"input_{coluna}"
            )
            st.session_state.mapeamento_tipos[coluna] = mapa_conversao[escolha]

    st.divider()

    if st.button("Gerar Dicionário de Tipos", type="primary"):
        st.subheader("⚙️ Dicionário Gerado:")
        
        st.json(st.session_state.mapeamento_tipos)
