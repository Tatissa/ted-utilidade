
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Criação automática das pastas se não existirem
Path("simulacoes").mkdir(exist_ok=True)
Path("dados").mkdir(exist_ok=True)
Path("relatorios").mkdir(exist_ok=True)

# Layout
st.set_page_config(page_title="TED Utilidade", layout="wide")
st.title("🚀 TED Utilidade - Web App Cloud")

menu = st.sidebar.radio("Navegação", ["Cadastro de Produtos", "Simular Encaixe", "Relatórios"])

# Cadastro
if menu == "Cadastro de Produtos":
    st.subheader("📦 Cadastro de Produtos")
    uploaded_file = st.file_uploader("Selecione um arquivo CSV com os produtos", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.to_csv("produtos.csv", index=False)
        st.success("Arquivo salvo com sucesso.")
    if Path("produtos.csv").exists():
        st.write("📄 Produtos cadastrados:")
        st.dataframe(pd.read_csv("produtos.csv"))

# Simulação
elif menu == "Simular Encaixe":
    st.subheader("📦 Simulação de Encaixe de Produtos")
    df_path = Path("produtos.csv")
    produtos_df = pd.read_csv(df_path) if df_path.exists() else pd.DataFrame(columns=["Produto", "Volume", "Peso"])

    if not produtos_df.empty:
        produtos_df["Caixa"] = "Caixa 1"
        st.dataframe(produtos_df)
        st.success("📦 Simulação executada!")

        with st.expander("💾 Salvar esta Simulação"):
            nome_simulacao = st.text_input("Nome da Simulação", value="simulacao_ted")
            if st.button("Salvar Simulação"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"{nome_simulacao}_{timestamp}.csv"
                produtos_df.to_csv(f"simulacoes/{nome_arquivo}", index=False)
                st.success(f"Simulação salva como: {nome_arquivo}")

# Relatórios
elif menu == "Relatórios":
    st.subheader("📑 Relatório de Simulação")
    arquivos = sorted(Path("simulacoes").glob("*.csv"), reverse=True)
    if arquivos:
        op = st.selectbox("Escolha uma simulação", arquivos)
        df = pd.read_csv(op)
        st.dataframe(df)
        st.download_button("📥 Baixar Relatório CSV", df.to_csv(index=False), file_name=op.name, mime="text/csv")
    else:
        st.info("Nenhuma simulação disponível.")
