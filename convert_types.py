import streamlit as st
import pandas as pd
from utils import handle_file
import zipfile
import io
import os


st.title("Agente Formatador")
uploaded_file = st.file_uploader("Arquivo a ser formatado!", type=["csv", "xlsx", "zip"])


if uploaded_file:
    if uploaded_file.type == "application/zip":
        st.subheader("Processando arquivo ZIP com múltiplos arquivos...")
        
        zip_bytes = uploaded_file.read()
        
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
            nomes_arquivos = [nome for nome in zip_file.namelist() 
                           if nome.lower().endswith(('.csv', '.xlsx')) and not nome.startswith('__') and not nome.endswith('/')]
            
            if not nomes_arquivos:
                st.error("Nenhum arquivo CSV ou XLSX encontrado no ZIP!")
                st.stop()
            
            st.info(f"Encontrados {len(nomes_arquivos)} arquivo(s) para processar: {', '.join(nomes_arquivos)}")
            
            tipos_saida = [".xlsx", ".csv"]
            st.markdown("Tipo de arquivo a ser exportado:")
            formato_tipo = st.radio(
                "Formato:",
                options=tipos_saida,
                index=None,
                horizontal=True,
                key="saida_zip"
            )
            
            if not formato_tipo:
                st.info("formato de saída não definido")
                st.stop()
            
            st.success(f"{formato_tipo}")
            st.divider()
            
            nome_arquivo_exemplo = nomes_arquivos[0]
            with zip_file.open(nome_arquivo_exemplo) as arquivo_entrada:
                if nome_arquivo_exemplo.lower().endswith('.csv'):
                    df_exemplo = pd.read_csv(arquivo_entrada)
                else:
                    df_exemplo = pd.read_excel(arquivo_entrada)
            
            st.subheader("Formatação atual (do primeiro arquivo):")
            st.dataframe(df_exemplo, width="stretch")
            
            st.subheader("Escolha o formato de cada coluna (será aplicado a TODOS os arquivos):")
            
            formatos_escolhidos = {}
            st.divider()
            
            for col in df_exemplo.columns:
                primeiro_valor = df_exemplo[col].iloc[0] if len(df_exemplo) > 0 else None
                
                st.markdown(f"**{col}** (exemplo: `{primeiro_valor}`)")
                
                nome_colunas = st.text_input(
                    "Novo nome da coluna (opcional):",
                    key=f"nome_{col}",
                    placeholder=col
                )


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
            
            st.divider()
            


            if st.button("Converter dados conforme formatos selecionados para TODOS os arquivos", type="primary"):
                if formatos_escolhidos:
                    st.success(f"Aplicando formatação a {len(nomes_arquivos)} arquivo(s)...")
                    
                    arquivos_processados = {}
                    
                    for nome_arquivo in nomes_arquivos:
                        try:
                            with zip_file.open(nome_arquivo) as arquivo_entrada:
                                if nome_arquivo.lower().endswith('.csv'):
                                    df = pd.read_csv(arquivo_entrada)
                                else:
                                    df = pd.read_excel(arquivo_entrada)
                            
                            df_converted = df.copy()
                            
                            # Aplicar renomeação de colunas primeiro
                            for col_original, col_nova in zip(df_exemplo.columns, [st.session_state.get(f"nome_{col}", col) if st.session_state.get(f"nome_{col}", col) else col for col in df_exemplo.columns]):
                                if col_original in df_converted.columns and col_nova != col_original:
                                    df_converted.rename(columns={col_original: col_nova}, inplace=True)
                            
                            for col, formato_escolhido in formatos_escolhidos.items():
                                # Ajustar nome da coluna se foi renomeado
                                col_atual = col
                                for col_original, col_nova in zip(df_exemplo.columns, [st.session_state.get(f"nome_{c}", c) if st.session_state.get(f"nome_{c}", c) else c for c in df_exemplo.columns]):
                                    if col_original == col and col_nova != col_original:
                                        col_atual = col_nova
                                        break
                                
                                if col_atual in df_converted.columns:
                                    try:
                                        if formato_escolhido == "int":
                                            #Dar uma pensada aqui
                                            df_converted[col_atual] = pd.to_numeric(df_converted[col_atual], errors='coerce')
                                            df_converted[col_atual] = df_converted[col_atual].fillna(0).astype(int)
                                        elif formato_escolhido == "float":
                                            #E aqui
                                            df_converted[col_atual] = pd.to_numeric(df_converted[col_atual], errors='coerce')
                                            df_converted[col_atual] = df_converted[col_atual].fillna(0.0)
                                        elif formato_escolhido == "str":
                                            df_converted[col_atual] = df_converted[col_atual].astype(str)
                                        elif formato_escolhido == "date":
                                            df_converted[col_atual] = pd.to_datetime(df_converted[col_atual], errors='coerce')
                                        
                                        st.success(f"Convertido '{col_atual}' para {formato_escolhido} em {nome_arquivo}")
                                    except Exception as e:
                                        st.error(f"Erro ao converter '{col_atual}' para {formato_escolhido} em {nome_arquivo}: {e}")
                            
                            arquivos_processados[nome_arquivo] = df_converted
                        except Exception as e:
                            st.error(f"Erro ao processar arquivo {nome_arquivo}: {e}")
                    
                    st.success(f"Todos {len(nomes_arquivos)} arquivo(s) processados com sucesso!")
                    
                    zip_saida = io.BytesIO()
                    
                    with zipfile.ZipFile(zip_saida, 'w', zipfile.ZIP_DEFLATED) as zip_final:
                        for nome_arquivo, df in arquivos_processados.items():
                            nome_base = os.path.splitext(nome_arquivo)[0]
                            
                            if formato_tipo == ".csv":
                                nome_saida = f"{nome_base}_formatado.csv"
                                csv_buffer = io.StringIO()
                                df.to_csv(csv_buffer)
                                zip_final.writestr(nome_saida, csv_buffer.getvalue())
                            else:
                                nome_saida = f"{nome_base}_formatado.xlsx"
                                xlsx_buffer = io.BytesIO()
                                df.to_excel(xlsx_buffer)
                                zip_final.writestr(nome_saida, xlsx_buffer.getvalue())
                    
                    zip_saida.seek(0)
                    
                    st.subheader("Download do arquivo formatado:")
                    st.download_button(
                        label="📦 Baixar ZIP com todos os arquivos formatados",
                        data=zip_saida,
                        file_name="arquivos_formatados.zip",
                        mime="application/zip"
                    )
                    
                    if nomes_arquivos[0] in arquivos_processados:
                        st.subheader("Exemplo de dados convertidos (primeiro arquivo):")
                        st.dataframe(arquivos_processados[nomes_arquivos[0]], width="stretch")
                        
                        st.subheader("Tipos finais (primeiro arquivo):")
                        tipos_final = {col: str(arquivos_processados[nomes_arquivos[0]][col].dtype) for col in arquivos_processados[nomes_arquivos[0]].columns}
                        st.json(tipos_final)
                else:
                    st.warning("Nenhum formato selecionado! Escolha o formato de pelo menos uma coluna.")
            
    else:
        df = handle_file(uploaded_file)


        st.subheader("Formatação atual:")
        st.dataframe(df, width="stretch")
        
        st.subheader("Escolha o formato de cada coluna:")
        
        formatos_escolhidos = {}
        tipos_saida = [".xlsx", ".csv"]


        st.markdown(f"Tipo de arquivo a ser exportado:")
        formato_tipo = st.radio(
            "Formato:",
            options=tipos_saida,
            index=None,
            horizontal=True,
            key="saida"
        )


        if formato_tipo:
            st.success(f"{formato_tipo}")
        else:
            st.info(f"formato de saída não definido")
        st.divider()


        for col in df.columns:
            primeiro_valor = df[col].iloc[0] if len(df) > 0 else None
            
            st.markdown(f"**{col}** (exemplo: `{primeiro_valor}`)")
            
            # Adicionar campo para renomear coluna também aqui
            nome_novo = st.text_input(
                "Novo nome da coluna (opcional):",
                key=f"nome_single_{col}",
                placeholder=col
            )
            
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
                
                # Aplicar renomeação de colunas primeiro
                for col_original in df.columns:
                    nome_novo = st.session_state.get(f"nome_single_{col_original}", col_original)
                    if nome_novo and nome_novo != col_original:
                        df_converted.rename(columns={col_original: nome_novo}, inplace=True)
                
                for col, formato_escolhido in formatos_escolhidos.items():
                    # Ajustar nome da coluna se foi renomeado
                    col_atual = col
                    for col_original in df.columns:
                        nome_novo = st.session_state.get(f"nome_single_{col_original}", col_original)
                        if col_original == col and nome_novo and nome_novo != col_original:
                            col_atual = nome_novo
                            break
                    
                    if col_atual in df_converted.columns:
                        try:
                            if formato_escolhido == "int":
                                #Dar uma pensada aqui
                                df_converted[col_atual] = pd.to_numeric(df_converted[col_atual], errors='coerce')
                                df_converted[col_atual] = df_converted[col_atual].fillna(0).astype(int)
                            elif formato_escolhido == "float":
                                # E aqui
                                df_converted[col_atual] = pd.to_numeric(df_converted[col_atual], errors='coerce')
                                df_converted[col_atual] = df_converted[col_atual].fillna(0.0)
                            elif formato_escolhido == "str":
                                df_converted[col_atual] = df_converted[col_atual].astype(str)
                            elif formato_escolhido == "date":
                                df_converted[col_atual] = pd.to_datetime(df_converted[col_atual], errors='coerce')
                            
                            st.success(f"Convertido '{col_atual}' para {formato_escolhido}")
                        except Exception as e:
                            st.error(f"Erro ao converter '{col_atual}' para {formato_escolhido}: {e}")
                
                st.subheader("Dados convertidos:")
                st.dataframe(df_converted, width="stretch")
                
                if formato_tipo == ".csv":
                    df_converted.to_csv("converted_data.csv")
                    st.download_button(
                        label="Baixar CSV",
                        data=open("converted_data.csv", "rb"),
                        file_name="converted_data.csv",
                        mime="text/csv"
                    )
                else:
                    df_converted.to_excel("converted_data.xlsx")
                    st.download_button(
                        label="Baixar XLSX",
                        data=open("converted_data.xlsx", "rb"),
                        file_name="converted_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                st.subheader("Tipos finais:")
                tipos_final = {col: str(df_converted[col].dtype) for col in df_converted.columns}
                st.json(tipos_final)
            else:
                st.warning("Nenhum formato selecionado! Escolha o formato de pelo menos uma coluna.")
        
        edited_df = st.data_editor(df, num_rows="dynamic")
        st.data_editor(df, key="my_key", num_rows="dynamic")