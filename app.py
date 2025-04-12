import streamlit as st
import json
import os
from graphviz import Digraph
from datetime import datetime
import base64
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="📲 MY GPTs — Catálogo Interativo",
    layout="wide"
)

# Cabeçalho com logomarca
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("mygpts.png"):
        st.image("mygpts.png", width=100)
    else:
        st.markdown("📲")

with col2:
    st.title("📲 MY GPTs — Catálogo Interativo de Inteligências Pessoais")
    st.markdown("""
    Organizado por Ramos de Atividade (S(s))  
    Cada GPT é uma Entidade Funcional (T(a)) com:

    - Nome (núcleo nominal/verbal)  
    - Pertencimento lógico-fuzzy (γ)  
    - Breve descrição funcional
    """)

# Carregar JSON externo
json_path = "GPT_002.json"
if not os.path.exists(json_path):
    st.error(f"Arquivo {json_path} não encontrado.")
    st.stop()

with open(json_path, "r", encoding="utf-8") as f:
    catalogo = json.load(f)

# Renderizar tabs
st.header(f"🔷 {catalogo['nome_do_gpt']}")
st.markdown(f"**Categoria:** {catalogo['categoria']}  ")
st.markdown(f"**Função Principal:** {catalogo['função_principal']}")

tab1, tab2, tab3 = st.tabs(["🔗 Fluxograma", "📋 Lista de Blocos", "📊 Matriz de Conexões"])

# === TAB 1: FLUXOGRAMA ===
with tab1:
    grafo = Digraph("Grafo GPT", format="png")
    grafo.attr(rankdir='TB', size='8')
    tipo_cor = {
        "inicio": "#d5f5e3",
        "ação": "#d6eaf8",
        "output": "#fdedec",
        "validação": "#fef9e7",
        "fim": "#fadbd8"
    }
    for bloco in catalogo['blocos_funcionais']:
        cor = tipo_cor.get(bloco['tipo'], '#f2f2f2')
        grafo.node(bloco['id'], bloco['texto'], shape='box', style='filled', fillcolor=cor)
    for origem, destino in catalogo['conexoes']:
        grafo.edge(origem, destino)
    st.graphviz_chart(grafo, use_container_width=True)

# === TAB 2: LISTAGEM ===
with tab2:
    for bloco in catalogo['blocos_funcionais']:
        st.markdown(f"**{bloco['id'].upper()} — {bloco['tipo'].capitalize()}**")
        st.markdown(bloco['texto'].replace("\n", "<br>"), unsafe_allow_html=True)
        st.markdown("---")

# === TAB 3: MATRIZ DE CONEXÕES ===
with tab3:
    blocos = [b['id'] for b in catalogo['blocos_funcionais']]
    matriz = []
    for origem in blocos:
        linha = {"De/Para": origem}
        for destino in blocos:
            linha[destino] = "✅" if [origem, destino] in catalogo['conexoes'] else ""
        matriz.append(linha)
    df = pd.DataFrame(matriz)
    st.dataframe(df, use_container_width=True)

# Exportação JSON e HTML
st.download_button(
    label="📥 Baixar JSON Técnico",
    data=json.dumps(catalogo, ensure_ascii=False, indent=2),
    file_name="gpt_fluxo_normas.json",
    mime="application/json"
)

def exportar_html():
    html = f"<html><head><meta charset='utf-8'><title>{catalogo['nome_do_gpt']}</title></head><body>"
    html += f"<h1>{catalogo['nome_do_gpt']}</h1>"
    html += f"<h3>Categoria: {catalogo['categoria']}</h3>"
    html += f"<p>{catalogo['função_principal']}</p><hr>"
    for bloco in catalogo['blocos_funcionais']:
        html += f"<h4>{bloco['id'].upper()} — {bloco['tipo'].capitalize()}</h4><pre>{bloco['texto']}</pre><hr>"
    html += "</body></html>"
    return html

st.download_button(
    label="📄 Exportar HTML Institucional",
    data=exportar_html(),
    file_name="gpt_fluxo_normas.html",
    mime="text/html"
)

st.markdown("""
---
📌 Powered by Lógica Modular Fuzzy α → θ  
🧩 T(a) → S(s) → P(p) com pesos γ (pertencimento semântico)  
📤 Desenvolvido para gestão e visualização dos seus GPTs pessoais
""")
