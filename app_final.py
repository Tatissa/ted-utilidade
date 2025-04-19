
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Criação automática de pastas
Path("dados").mkdir(exist_ok=True)
Path("relatorios").mkdir(exist_ok=True)
Path("simulacoes").mkdir(exist_ok=True)

# Layout e menu
st.set_page_config(page_title="TED Utilidade", layout="wide")
st.title("🚀 TED Utilidade - Web App")

menu = st.sidebar.radio("Navegação", [
    "Cadastro de Produtos", 
    "Cadastro de Embalagens",
    "Simular Encaixe", 
    "Simulações Salvas", 
    "Relatórios"
])

produtos_path = Path("dados/produtos.csv")
caixas_path = Path("dados/caixas.csv")

# Página de Cadastro de Produtos
if menu == "Cadastro de Produtos":
    st.subheader("📦 Cadastro de Produtos")
    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        comp = st.number_input("Comprimento (mm)", min_value=0)
        larg = st.number_input("Largura (mm)", min_value=0)
        alt = st.number_input("Altura (mm)", min_value=0)
        peso = st.number_input("Peso (kg)", min_value=0.0)
        submitted = st.form_submit_button("Salvar")
        if submitted:
            novo = pd.DataFrame([[nome, comp, larg, alt, peso]], 
                                columns=["Produto", "Comprimento", "Largura", "Altura", "Peso"])
            df = pd.read_csv(produtos_path) if produtos_path.exists() else pd.DataFrame(columns=novo.columns)
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(produtos_path, index=False)
            st.success("Produto cadastrado com sucesso!")
    if produtos_path.exists():
        st.dataframe(pd.read_csv(produtos_path))

# Página de Cadastro de Embalagens
elif menu == "Cadastro de Embalagens":
    st.subheader("📦 Cadastro de Embalagens (Caixas)")
    with st.form("form_caixa"):
        nome = st.text_input("Nome da Embalagem")
        comp = st.number_input("Comprimento (mm)", min_value=0)
        larg = st.number_input("Largura (mm)", min_value=0)
        alt = st.number_input("Altura (mm)", min_value=0)
        peso_max = st.number_input("Peso Máximo (kg)", min_value=0.0)
        submitted = st.form_submit_button("Salvar")
        if submitted:
            novo = pd.DataFrame([[nome, comp, larg, alt, peso_max]], 
                                columns=["Nome", "Comprimento", "Largura", "Altura", "Peso Máximo"])
            df = pd.read_csv(caixas_path) if caixas_path.exists() else pd.DataFrame(columns=novo.columns)
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(caixas_path, index=False)
            st.success("Embalagem cadastrada com sucesso!")
    if caixas_path.exists():
        st.dataframe(pd.read_csv(caixas_path))

# Simulação
elif menu == "Simular Encaixe":
    st.subheader("📦 Simulação de Encaixe")
    if produtos_path.exists() and caixas_path.exists():
        produtos_df = pd.read_csv(produtos_path)
        caixas_df = pd.read_csv(caixas_path)
        caixa_escolhida = st.selectbox("Selecione a Embalagem", caixas_df["Nome"].unique())
        caixa_info = caixas_df[caixas_df["Nome"] == caixa_escolhida].iloc[0]
        st.write(f"Dimensões da Caixa: {caixa_info['Comprimento']} x {caixa_info['Largura']} x {caixa_info['Altura']} mm")
        st.write(f"Peso Máximo: {caixa_info['Peso Máximo']} kg")

        qtds = {}
        for _, row in produtos_df.iterrows():
            qtds[row['Produto']] = st.number_input(f"{row['Produto']} - Quantidade", min_value=0, value=0)

        sim_df = produtos_df.copy()
        sim_df["Quantidade"] = sim_df["Produto"].map(qtds)
        sim_df = sim_df[sim_df["Quantidade"] > 0]
        st.write("📋 Produtos para simulação:")
        st.dataframe(sim_df)

        if not sim_df.empty and st.button("Salvar Simulação"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"simulacao_{timestamp}.csv"
            sim_df.to_csv(f"simulacoes/{nome_arquivo}", index=False)
            st.success(f"Simulação salva como: {nome_arquivo}")
    else:
        st.warning("Cadastre produtos e embalagens antes de simular.")

# Página de Simulações Salvas
elif menu == "Simulações Salvas":
    st.subheader("📁 Simulações Salvas")
    simul_files = sorted(Path("simulacoes").glob("*.csv"), reverse=True)
    if simul_files:
        for file in simul_files:
            with st.expander(file.name):
                df = pd.read_csv(file)
                st.dataframe(df)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🗑️ Excluir {file.name}"):
                        file.unlink()
                        st.warning(f"{file.name} excluído.")
                        st.experimental_rerun()
                with col2:
                    if st.button(f"📋 Duplicar {file.name}"):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        novo_nome = f"{file.stem}_copia_{timestamp}.csv"
                        Path(f"simulacoes/{novo_nome}").write_text(file.read_text())
                        st.success(f"{file.name} duplicado como {novo_nome}")
                        st.experimental_rerun()
    else:
        st.info("Nenhuma simulação encontrada.")

# Página de Relatórios
elif menu == "Relatórios":
    st.subheader("📄 Relatórios")
    simul_files = sorted(Path("simulacoes").glob("*.csv"), reverse=True)
    if simul_files:
        arquivo = st.selectbox("Selecione uma simulação", simul_files)
        df = pd.read_csv(arquivo)
        st.dataframe(df)
        st.download_button("📥 Baixar Relatório CSV", data=df.to_csv(index=False), file_name=arquivo.name)
    else:
        st.info("Nenhuma simulação disponível.")
