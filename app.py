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

# JSON atualizado
catalogo = {
  "nome_do_gpt": "GPT - Implementador de Normas Inteligentes",
  "categoria": "Automação com Inteligência Jurídica",
  "função_principal": "Auxiliar na disseminação normativa baseada em provimentos oficiais com ações de publicação, atualização e acompanhamento",
  "blocos_funcionais": [
    {
      "id": "start",
      "tipo": "inicio",
      "texto": "Início – Ativação do GPT com base em Provimento nº 10/2024"
    },
    {
      "id": "b1",
      "tipo": "ação",
      "texto": "1. Análise e Consolidação Técnica\n- Geração de parecer normativo\n- Estruturação do texto jurídico"
    },
    {
      "id": "b2",
      "tipo": "output",
      "texto": "2. Comunicação Oficial\n- Elaboração de post + ofício automatizado\n- Criação de conteúdos visuais e explicativos"
    },
    {
      "id": "b3",
      "tipo": "validação",
      "texto": "3. Atualização de Modelos\n- Inserção em roteiros de GPT Fiscalizador\n- Validação semântica das regras"
    },
    {
      "id": "b4",
      "tipo": "ação",
      "texto": "4. Acompanhamento e Adaptação\n- Análise dos prompts recebidos\n- Ajustes conforme feedback normativo"
    },
    {
      "id": "end",
      "tipo": "fim",
      "texto": "Encerramento – GPT pronto para replicação normativa inteligente"
    }
  ],
  "conexoes": [
    ["start", "b1"],
    ["b1", "b2"],
    ["b2", "b3"],
    ["b3", "b4"],
    ["b4", "end"]
  ]
}

# Renderizar fluxo visual
st.header(f"🔷 {catalogo['nome_do_gpt']}")
st.markdown(f"**Categoria:** {catalogo['categoria']}  ")
st.markdown(f"**Função Principal:** {catalogo['função_principal']}")

grafo = Digraph("Grafo GPT", format="png")
grafo.attr(rankdir='LR', size='10')
grafo.node("GPT", catalogo['nome_do_gpt'], shape='folder', style='filled', fillcolor='lightblue')

for bloco in catalogo['blocos_funcionais']:
    grafo.node(bloco['id'], bloco['texto'], shape='box', style='filled', fillcolor='lightgrey')
    if bloco['id'] != "GPT":
        grafo.edge("GPT" if bloco['id'] == "start" else None, bloco['id'])

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
