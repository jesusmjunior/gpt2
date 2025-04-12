# === Streamlit App para Catalogar e Exibir MyGPTs (contexto: COGEX) ===
import streamlit as st
import json
import os
import pandas as pd
from graphviz import Digraph

def carregar_arquivo():
    st.sidebar.header("📂 Importar MyGPT")
    arquivos = [f for f in os.listdir() if f.endswith(".json")]
    arquivo_escolhido = st.sidebar.selectbox("Escolha um arquivo JSON", arquivos)
    if arquivo_escolhido:
        with open(arquivo_escolhido, "r", encoding="utf-8") as f:
            return json.load(f), arquivo_escolhido
    return None, None

def renderizar_fluxo(dados):
    st.header(f"🧠 {dados['nome_do_gpt']}")
    st.subheader(f"📚 Categoria: {dados['categoria']}")

    tabs = st.tabs(["📋 Lista de Blocos", "🔗 Conexões", "📈 Fuzzy α → θ"])

    with tabs[0]:
        for bloco in dados["blocos_funcionais"]:
            with st.expander(f"🔹 {bloco['nome']} ({bloco['tipo']})"):
                st.markdown(f"📝 **Descrição**: {bloco['descricao']}")
                st.markdown(f"💠 **Pertinência Semântica S(x)**: `{bloco['S(x)']}`")
                st.json(bloco['fuzzy'], expanded=False)

    with tabs[1]:
        st.subheader("🔗 Fluxo entre Blocos")
        g = Digraph("fluxo", format="png")
        g.attr(rankdir="LR", size="10")
        for bloco in dados["blocos_funcionais"]:
            g.node(bloco["id"], bloco["nome"])
        for origem, destino in dados["conexoes"]:
            g.edge(origem, destino)
        st.graphviz_chart(g)

    with tabs[2]:
        df_fuzzy = pd.DataFrame([
            {**b["fuzzy"], "Bloco": b["nome"], "S(x)": b["S(x)"]} 
            for b in dados["blocos_funcionais"]
        ])
        st.dataframe(df_fuzzy.set_index("Bloco"))

def exportar_json_semantico(dados, nome_arquivo):
    novo = {
        "gpt_nome": dados["nome_do_gpt"],
        "categoria": dados["categoria"],
        "blocos": dados["blocos_funcionais"],
        "conexoes": dados["conexoes"],
        "pontuacao_media": sum(b["S(x)"] for b in dados["blocos_funcionais"]) / len(dados["blocos_funcionais"])
    }
    nome_export = nome_arquivo.replace(".json", "_semantico.json")
    with open(nome_export, "w", encoding="utf-8") as f:
        json.dump(novo, f, indent=2, ensure_ascii=False)
    with open(nome_export, "rb") as f:
        st.download_button("📤 Baixar JSON Semântico", f, file_name=nome_export)

# === Execução ===
def main():
    st.set_page_config("MyGPT Catalogador COGEX", layout="wide")
    st.markdown("# 🤖 Catálogo de MyGPTs – COGEX")
    st.markdown("Sistema fuzzy de análise e exibição de GPTs personalizados com exportação semântica.")

    dados, nome_arquivo = carregar_arquivo()
    if dados:
        renderizar_fluxo(dados)
        exportar_json_semantico(dados, nome_arquivo)
    else:
        st.warning("Nenhum JSON carregado.")

if __name__ == "__main__":
    main()
