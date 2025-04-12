# -*- coding: utf-8 -*-
import streamlit as st
import json
import zipfile
import os
import tempfile

st.set_page_config(page_title="Validador de GPTs", layout="wide")
st.title("📦 Visualizador e Validador de GPTs Inteligentes")

# Upload do arquivo ZIP
uploaded_file = st.file_uploader("Selecione um arquivo .zip com os JSONs:", type=["zip"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
            json_files = [f for f in zip_ref.namelist() if f.endswith(".json")]

        selected_json = st.selectbox("📂 Escolha um arquivo JSON para visualizar:", json_files)

        if selected_json:
            json_path = os.path.join(tmpdir, selected_json)
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Verificação de estrutura mínima
                if not all(k in data for k in ["nome_do_gpt", "categoria", "blocos_funcionais", "conexoes"]):
                    st.error("❌ Estrutura JSON inválida. Esperado: nome_do_gpt, categoria, blocos_funcionais, conexoes.")
                else:
                    tab1, tab2, tab3 = st.tabs(["📄 Detalhes", "🧩 Blocos Funcionais", "🔗 Conexões"])

                    with tab1:
                        st.subheader("📘 Detalhes do GPT")
                        st.write(f"**Nome do GPT:** {data['nome_do_gpt']}")
                        st.write(f"**Categoria:** {data['categoria']}")

                    with tab2:
                        st.subheader("🔧 Blocos Funcionais")
                        for bloco in data["blocos_funcionais"]:
                            with st.expander(f"{bloco['id']} | {bloco['nome']} ({bloco['tipo']})"):
                                st.write(f"📄 **Descrição**: {bloco['descricao']}")
                                st.write("📊 **Fuzzy Scores**:")
                                st.json(bloco["fuzzy"])
                                st.write(f"🧮 **S(x):** `{bloco['S(x)']}`")

                    with tab3:
                        st.subheader("🔁 Conexões entre Blocos")
                        for origem, destino in data["conexoes"]:
                            st.markdown(f"`{origem}` ➡️ `{destino}`")

            except Exception as e:
                st.error(f"Erro ao processar o JSON: {str(e)}")
