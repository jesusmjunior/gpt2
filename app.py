# === app.py - Catálogo e Visualização de MyGPTs com lógica fuzzy α → θ ===
import streamlit as st
import json
import os
import pandas as pd
from graphviz import Digraph

st.set_page_config("🧠 Catálogo de MyGPTs", layout="wide")

st.title("🧠 MyGPTs – COGEX")
st.markdown("Sistema de visualização fuzzy de blocos funcionais para GPTs personalizados")

# === Carregamento ===
arquivos = [f for f in os.listdir() if f.endswith(".json")]
arquivo_escolhido = st.sidebar.selectbox("📂 Selecione um MyGPT", arquivos)

if not arquivo_escolhido:
    st.warning("Nenhum arquivo selecionado.")
    st.stop()

with open(arquivo_escolhido, encoding='utf-8') as f:
    gpt_data = json.load(f)

# === Cabeçalho ===
st.header(f"📌 Nome: {gpt_data['nome_do_gpt']}")
st.subheader(f"📚 Categoria: {gpt_data['categoria']}")

# === Tabs: Blocos, Fluxo, Fuzzy ===
tabs = st.tabs(["📋 Blocos", "🔁 Fluxo", "📊 Fuzzy α → θ"])

with tabs[0]:
    for bloco in gpt_data["blocos_funcionais"]:
        with st.expander(f"🔹 {bloco['nome']} ({bloco['tipo']})"):
            st.markdown(f"📝 {bloco['descricao']}")
            st.write("🔬 Pertinência S(x):", bloco["S(x)"])
            st.json(bloco["fuzzy"])

with tabs[1]:
    st.subheader("🔗 Fluxo de Blocos")
    graph = Digraph("fluxo", format="png")
    graph.attr(rankdir="LR")
    for b in gpt_data["blocos_funcionais"]:
        graph.node(b["id"], f"{b['nome']}")
    for c in gpt_data["conexoes"]:
        graph.edge(c[0], c[1])
    st.graphviz_chart(graph)

with tabs[2]:
    df_fuzzy = pd.DataFrame([
        {**b["fuzzy"], "Bloco": b["nome"], "S(x)": b["S(x)"]} for b in gpt_data["blocos_funcionais"]
    ])
    st.dataframe(df_fuzzy.set_index("Bloco"))

# === Exportação JSON Técnico ===
st.markdown("---")
st.subheader("📤 Exportar MyGPT com pontuação α → θ")
if st.button("🔽 Exportar JSON Semântico"):
    export_data = {
        "nome_do_gpt": gpt_data["nome_do_gpt"],
        "categoria": gpt_data["categoria"],
        "media_S(x)": sum(b["S(x)"] for b in gpt_data["blocos_funcionais"]) / len(gpt_data["blocos_funcionais"]),
        "blocos": gpt_data["blocos_funcionais"],
        "conexoes": gpt_data["conexoes"]
    }
    export_file = f"{gpt_data['nome_do_gpt'].replace(' ', '_')}_semantico.json"
    with open(export_file, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    with open(export_file, "rb") as f:
        st.download_button("📥 Baixar JSON", f, file_name=export_file)
