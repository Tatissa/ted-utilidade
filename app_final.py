
import streamlit as st
import pandas as pd
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="TED Utilidade", layout="wide")
st.title("TED Utilidade - Web App Cloud 🚀")

# Pastas e arquivos
Path("dados").mkdir(exist_ok=True)
Path("relatorios").mkdir(exist_ok=True)
Path("simulacoes").mkdir(exist_ok=True)
produtos_path = Path("dados/produtos.csv")
produtos_df = pd.read_csv(produtos_path) if produtos_path.exists() else pd.DataFrame(columns=["Produto", "Volume", "Peso", "Caixa"])

# Menu lateral
menu = st.sidebar.radio("Navegação", ["📥 Cadastro de Produtos", "📦 Simular Encaixe", "📄 Relatórios"])

# Função para salvar simulação
def salvar_simulacao(simulacao_df, nome_simulacao):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{nome_simulacao}_{timestamp}.csv"
    caminho_arquivo = Path("simulacoes") / nome_arquivo
    simulacao_df.to_csv(caminho_arquivo, index=False)
    return caminho_arquivo

# Página de Cadastro
if menu == "📥 Cadastro de Produtos":
    st.subheader("Cadastro de Produtos")
    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        volume = st.number_input("Volume (cm³)", min_value=0)
        peso = st.number_input("Peso (kg)", min_value=0.0)
        caixa = st.text_input("Caixa")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            novo = pd.DataFrame([[nome, volume, peso, caixa]], columns=["Produto", "Volume", "Peso", "Caixa"])
            produtos_df = pd.concat([produtos_df, novo], ignore_index=True)
            produtos_df.to_csv(produtos_path, index=False)
            st.success("Produto cadastrado com sucesso!")
    st.dataframe(produtos_df)

# Página de Simulação
elif menu == "📦 Simular Encaixe":
    st.subheader("Simulação de Encaixe")
    if not produtos_df.empty:
        simulacao_df = produtos_df.copy()
        simulacao_df["Caixa"] = "Caixa 1"  # Simulação fictícia
        st.dataframe(simulacao_df)

        with st.expander("💾 Salvar esta Simulação"):
            nome_simulacao = st.text_input("Nome da Simulação", "simulacao_ted")
            if st.button("Salvar Simulação"):
                caminho = salvar_simulacao(simulacao_df, nome_simulacao)
                st.success(f"Simulação salva como: {caminho.name}")
    else:
        st.warning("Nenhum produto cadastrado para simular.")

# Página de Relatórios
elif menu == "📄 Relatórios":
    st.subheader("Gerar Relatório PDF")
    if not produtos_df.empty:
        if st.button("Gerar Relatório"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(200, 10, txt="Relatório de Produtos Cadastrados", ln=True, align='C')
            pdf.ln(10)
            for _, row in produtos_df.iterrows():
                linha = f"Produto: {row['Produto']}, Volume: {row['Volume']}, Peso: {row['Peso']}, Caixa: {row['Caixa']}"
                pdf.cell(200, 10, txt=linha, ln=True)
            relatorio_path = Path("relatorios/relatorio_simulacao.pdf")
            pdf.output(str(relatorio_path))
            with open(relatorio_path, "rb") as file:
                st.download_button("📥 Baixar Relatório em PDF", file, file_name="relatorio_simulacao.pdf", mime="application/pdf")
    else:
        st.info("Nenhum produto cadastrado para gerar relatório.")
