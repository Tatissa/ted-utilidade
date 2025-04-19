
import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="TED Utilidade", layout="wide")
st.title("TED Utilidade - Web App Cloud 🚀")
st.write("Bem-vinda, Tatissa! Seu painel completo TED está carregado aqui.")

# Menu lateral
menu = st.sidebar.radio("Navegação", ["Cadastro de Produtos", "Simular Encaixe", "Relatórios"])

# Base de dados inicial
df_path = "dados/produtos.csv"
produtos_df = pd.read_csv(df_path) if Path(df_path).exists() else pd.DataFrame(columns=["Produto", "Volume", "Peso", "Caixa"])

if menu == "Cadastro de Produtos":
    st.subheader("📦 Cadastro de Produtos")
    with st.form("cadastro_form"):
        nome = st.text_input("Nome do Produto")
        volume = st.number_input("Volume (cm³)", min_value=0)
        peso = st.number_input("Peso (kg)", min_value=0.0)
        caixa = st.text_input("Caixa Destinada")
        submitted = st.form_submit_button("Salvar")

        if submitted:
            novo = pd.DataFrame([[nome, volume, peso, caixa]], columns=["Produto", "Volume", "Peso", "Caixa"])
            produtos_df = pd.concat([produtos_df, novo], ignore_index=True)
            produtos_df.to_csv(df_path, index=False)
            st.success("Produto cadastrado com sucesso!")

    st.dataframe(produtos_df)

elif menu == "Simular Encaixe":
    st.subheader("🔄 Simular Encaixe de Produtos")
    st.table(produtos_df)
    st.info("📦 Simulação executada! (Esta é uma simulação demonstrativa)")

elif menu == "Relatórios":
    st.subheader("📄 Relatório de Simulação")
    if not produtos_df.empty:
        with st.spinner("Gerando relatório..."):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(200, 10, txt="Relatório de Simulação - TED Utilidade", ln=True, align='C')
            pdf.ln(10)
            for _, row in produtos_df.iterrows():
                linha = f"Produto: {row['Produto']}, Volume: {row['Volume']}, Peso: {row['Peso']}, Caixa: {row['Caixa']}"
                pdf.cell(200, 10, txt=linha, ln=True)
            output_path = "relatorios/relatorio_simulacao.pdf"
            pdf.output(output_path)
            with open(output_path, "rb") as file:
                st.success("Relatório gerado com sucesso!")
                st.download_button("📥 Baixar Relatório em PDF", file, "relatorio_simulacao.pdf", mime="application/pdf")
    else:
        st.warning("Nenhum dado disponível para gerar o relatório.")
