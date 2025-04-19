
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TED Utilidade", layout="wide")
st.title("TED Utilidade - Web App Cloud 🚀")
st.markdown("Bem-vinda, Tatissa! Seu painel completo TED está carregado aqui.")

menu = st.sidebar.radio("Navegação", ["Cadastro de Produtos", "Simular Encaixe", "Relatórios"])

# Carregar dados
dados_path = "dados/produtos.csv"
relatorios_path = "relatorios/relatorio_simulacao.pdf"

if menu == "Cadastro de Produtos":
    st.subheader("Cadastro de Produtos")
    if os.path.exists(dados_path):
        df = pd.read_csv(dados_path)
        st.dataframe(df)
    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        volume = st.number_input("Volume", min_value=0.0, step=0.1)
        peso = st.number_input("Peso", min_value=0.0, step=0.1)
        caixa = st.text_input("Caixa")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            novo = pd.DataFrame([[nome, volume, peso, caixa]], columns=["Produto", "Volume", "Peso", "Caixa"])
            if os.path.exists(dados_path):
                df = pd.read_csv(dados_path)
                df = pd.concat([df, novo], ignore_index=True)
            else:
                df = novo
            df.to_csv(dados_path, index=False)
            st.success("Produto cadastrado com sucesso!")

elif menu == "Simular Encaixe":
    st.subheader("Simular Encaixe de Produtos")
    if os.path.exists(dados_path):
        df = pd.read_csv(dados_path)
        st.dataframe(df)
        st.markdown("🔄 Simulação executada! (Esta é uma simulação demonstrativa)")
    else:
        st.warning("Nenhum produto cadastrado ainda.")

elif menu == "Relatórios":
    st.subheader("Relatórios Gerados")
    if os.path.exists(relatorios_path):
        with open(relatorios_path, "rb") as f:
            st.download_button("📄 Baixar relatório de simulação", f, file_name="relatorio_simulacao.pdf")
    else:
        st.info("Nenhum relatório gerado ainda.")
