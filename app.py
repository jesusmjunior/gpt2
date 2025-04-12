import streamlit as st
import json
import os
from graphviz import Digraph
from datetime import datetime
import base64
from PIL import Image

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
json_path = "gpt_fluxo_normas.json"
if not os.path.exists(json_path):
    st.error(f"Arquivo {json_path} não encontrado.")
    st.stop()

with open(json_path, "r", encoding="utf-8") as f:
    catalogo = json.load(f)

# Renderizar fluxo visual
st.header(f"🔷 {catalogo['nome_do_gpt']}")
st.markdown(f"**Categoria:** {catalogo['categoria']}  ")
st.markdown(f"**Função Principal:** {catalogo['função_principal']}")

grafo = Digraph("Grafo GPT", format="png")
grafo.attr(rankdir='LR', size='10')
grafo.node("GPT", catalogo['nome_do_gpt'], shape='folder', style='filled', fillcolor='lightblue')

for bloco in catalogo['blocos_funcionais']:
    grafo.node(bloco['id'], bloco['texto'], shape='box', style='filled', fillcolor='lightgrey')

for origem, destino in catalogo['conexoes']:
    grafo.edge(origem, destino)

st.graphviz_chart(grafo)

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
