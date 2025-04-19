
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="TED Utilidade - Web App Cloud 🚀", layout="wide")

st.title("TED Utilidade - Web App Cloud 🚀")
st.markdown("Bem-vinda, Tatissa! Seu painel completo TED está carregado aqui.")

# Pastas
Path("dados").mkdir(exist_ok=True)
Path("relatorios").mkdir(exist_ok=True)
Path("simulacoes").mkdir(exist_ok=True)

# Arquivo de produtos
produtos_path = Path("dados/produtos.csv")
produtos_df = pd.read_csv(produtos_path) if produtos_path.exists() else pd.DataFrame(columns=["Produto", "Volume", "Peso", "Caixa"])

# Simulação
st.header("📦 Simular Encaixe de Produtos")
st.table(produtos_df)

# Simulação fictícia
simulacao_df = produtos_df.copy()
simulacao_df["Caixa"] = "Caixa 1"
st.success("📦 Simulação executada! (Esta é uma simulação demonstrativa)")

# Função para salvar simulação
def salvar_simulacao(simulacao_df, nome_simulacao):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{nome_simulacao}_{timestamp}.csv"
    caminho_arquivo = Path("simulacoes") / nome_arquivo
    simulacao_df.to_csv(caminho_arquivo, index=False)
    return caminho_arquivo

# Interface para salvar simulação
with st.expander("💾 Salvar esta Simulação"):
    nome_simulacao = st.text_input("Nome da Simulação", "simulacao_ted")
    if st.button("Salvar Simulação"):
        caminho = salvar_simulacao(simulacao_df, nome_simulacao)
        st.success(f"Simulação salva como: {caminho.name}")
