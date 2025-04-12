# === app.py - Compatível com Streamlit Cloud ===
import streamlit as st
import json
import os
import pandas as pd

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

# === Tabs ===
tabs = st.tabs(["📋 Blocos", "🔁 Fluxo", "📊 Fuzzy α → θ"])

with tabs[0]:
    for bloco in gpt_data["blocos_funcionais"]:
        with st.expander(f"🔹 {bloco['nome']} ({bloco['tipo']})"):
            st.markdown(f"📝 {bloco['descricao']}")
            st.write("🔬 Pertinência S(x):", bloco["S(x)"])
            st.json(bloco["fuzzy"])

with tabs[1]:
    st.subheader("🔗 Fluxo de Blocos")
    dot_source = "digraph fluxo {\nrankdir=LR;\n"
    for b in gpt_data["blocos_funcionais"]:
        dot_source += f'{b["id"]} [label="{b["nome"]}"];\n'
    for origem, destino in gpt_data["conexoes"]:
        dot_source += f"{origem} -> {destino};\n"
    dot_source += "}"
    st.graphviz_chart(dot_source)

with tabs[2]:
    df_fuzzy = pd.DataFrame([
        {**b["fuzzy"], "Bloco": b["nome"], "S(x)": b["S(x)"]} for b in gpt_data["blocos_funcionais"]
    ])
    st.dataframe(df_fuzzy.set_index("Bloco"))

# === Exportação ===
st.markdown("---")
st.subheader("📤 Exportar JSON Semântico")
if st.button("🔽 Baixar"):
    export_data = {
        "nome_do_gpt": gpt_data["nome_do_gpt"],
        "categoria": gpt_data["categoria"],
        "media_S(x)": sum(b["S(x)"] for b in gpt_data["blocos_funcionais"]) / len(gpt_data["blocos_funcionais"]),
        "blocos": gpt_data["blocos_funcionais"],
        "conexoes": gpt_data["conexoes"]
    }
    nome_export = f"{gpt_data['nome_do_gpt'].replace(' ', '_')}_semantico.json"
    with open(nome_export, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    with open(nome_export, "rb") as f:
        st.download_button("📥 Baixar Arquivo", f, file_name=nome_export)
