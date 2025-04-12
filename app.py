import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
from datetime import datetime
import pandas as pd
import base64
import re
# ===== P(p): Main Application Process =====
def main_application():
"""
P(p): Core application process orchestrating the entire GPT catalog flow
Contains: UI Rendering, GPT Data Processing, Export Functions
"""
# R(r): Application Requirements
configure_app_settings()
# S(s): Header Subsequence
render_institutional_header()
# S(s): Navigation Subsequence
selected_gpt = process_navigation_selection()
if not selected_gpt:
return
# S(s): GPT Rendering Subsequence
gpt_data = process_gpt_rendering(selected_gpt)
if not gpt_data:
return
# S(s): Export Subsequence
process_export_options(gpt_data, selected_gpt)
# S(s): Support Subsequence
render_support_elements()
# ===== T(a): Configuration Tasks =====
def configure_app_settings():
"""
T(a): Sets up application configuration and styling
"""
st.set_page_config(
page_title="Catálogo de GPTs - Sistema de Gerenciamento",
layout="centered",
initial_sidebar_state="collapsed"
)
# Apply semantic styling with fuzzy classifiers
st.markdown("""
<style>
.main {
max-width: 950px;
margin: auto;
padding-top: 1.5rem;
}
.stApp {
background-color: #f8f9fa;
}
h1, h2, h3 {
color: #2c3e50;
font-family: 'Arial', sans-serif;
}
.header-container {
background-color: #f0f2f6;
padding: 1.5rem;
border-radius: 10px;
margin-bottom: 1.5rem;
box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.node-box {
padding: 1rem;
border-radius: 8px;
margin-bottom: 1rem;
box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}
.node-ia { background-color: #d5f5e3; border-left: 5px solid #2ecc71; }
.node-juridico { background-color: #d6eaf8; border-left: 5px solid #3498db; }
.node-escritorio { background-color: #fef9e7; border-left: 5px solid #f1c40f; }
.node-programacao { background-color: #fdedec; border-left: 5px solid #e74c3c; }
.node-pessoal { background-color: #f2f3f4; border-left: 5px solid #7f8c8d; }
.node-diversos { background-color: #fadbd8; border-left: 5px solid #c0392b; }
.gpt-btn {
background-color: #000000;
color: white;
padding: 0.5rem 1rem;
border-radius: 5px;
text-align: center;
font-weight: bold;
}
.stButton>button {
background-color: #3498db;
color: white;
font-weight: bold;
}
.gpt-details-box {
background-color: #fff;
padding: 1rem;
border-radius: 5px;
border-left: 5px solid #34495e;
}
.floating-assistant {
position: fixed;
right: 20px;
bottom: 20px;
background: white;
padding: 10px;
border-radius: 50%;
box-shadow: 0 2px 10px rgba(0,0,0,0.2);
z-index: 1000;
}
.speech-bubble {
position: absolute;
right: 80px;
bottom: 40px;
background: #3498db;
color: white;
padding: 10px;
border-radius: 10px;
width: 150px;
text-align: center;
}
.speech-bubble a {
color: white;
text-decoration: none;
}
.placa-gpt {
text-align: center;
font-size: 12px;
font-weight: bold;
margin-top: 5px;
color: #2c3e50;
}
.legend-item {
display: flex;
align-items: center;
margin-bottom: 8px;
}
.legend-color {
width: 16px;
height: 16px;
border-radius: 3px;
margin-right: 8px;
}
.connection-diagram {
margin-top: 1rem;
padding: 1rem;
background: #f7f7f7;
border-radius: 8px;
}
.fuzzy-score {
margin-top: 1rem;
padding: 0.5rem;
font-size: 0.9rem;
border-radius: 5px;
background: #edf2f7;
}
.module-tag {
display: inline-block;
padding: 2px 6px;
background: #e2e8f0;
border-radius: 4px;
font-size: 0.8rem;
margin-right: 5px;
color: #2d3748;
}
.gpt-id {
font-weight: bold;
color: #2c3e50;
font-size: 0.9rem;
}
.feature-tag {
display: inline-block;
padding: 3px 8px;
background: #e2e8f0;
border-radius: 15px;
font-size: 0.75rem;
margin-right: 5px;
margin-bottom: 5px;
color: #2d3748;
}
.action-button {
margin-top: 10px;
display: inline-block;
padding: 5px 10px;
background: #3498db;
color: white;
border-radius: 5px;
text-decoration: none;
font-size: 0.9rem;
cursor: pointer;
}
.stats-container {
display: flex;
justify-content: space-between;
background: #f8f9fa;
padding: 10px;
border-radius: 5px;
margin-bottom: 15px;
}
.stat-box {
text-align: center;
padding: 10px;
border-radius: 5px;
background: white;
box-shadow: 0 1px 3px rgba(0,0,0,0.1);
flex: 1;
margin: 0 5px;
}
.stat-number {
font-size: 1.5rem;
font-weight: bold;
color: #3498db;
}
.stat-label {
font-size: 0.8rem;
color: #7f8c8d;
}
</style>
""", unsafe_allow_html=True)
# ===== T(a): Header Rendering =====
def render_institutional_header():
"""
T(a): Creates the institutional header with logo and title
"""
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_logo, col_texto = st.columns([1, 3])
with col_logo:
# Check if logo exists, otherwise use placeholder
if os.path.exists("gptlogo.png"):
st.image(Image.open("gptlogo.png"), width=150)
else:
st.markdown("🤖 **GPT CATALOG**")
with col_texto:
st.markdown("### **SISTEMA DE CATALOGAÇÃO E GERENCIAMENTO DE GPTs**")
st.markdown("#### Catálogo Inteligente com Framework Semântico")
st.markdown("<small>Versão 1.0 - Framework de Classificação Avançada</small>",
unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
# Add dashboard stats
st.markdown('<div class="stats-container">', unsafe_allow_html=True)
# Statistics boxes - these would be dynamically populated in a real app
stats = [
{"number": "42", "label": "GPTs Cadastrados"},
{"number": "6", "label": "Categorias"},
{"number": "83%", "label": "Taxa de Uso"},
{"number": "12", "label": "Criados este mês"}
]
for stat in stats:
st.markdown(f"""
<div class="stat-box">
<div class="stat-number">{stat['number']}</div>
<div class="stat-label">{stat['label']}</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
# ===== T(a): Navigation Tasks =====
def process_navigation_selection():
"""
T(a): Processes user navigation and GPT selection
Returns: Selected GPT or None
"""
st.markdown("### 📂 Navegação e Pesquisa de GPTs")
# Create tabs for different selection methods
tab_browse, tab_search, tab_categories = st.tabs(["Todos GPTs", "Pesquisa Avançada",
"Categorias"])
with tab_browse:
arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json") and f.startswith("gpt_")])
if not arquivos_json:
st.warning("Nenhum arquivo de GPT encontrado no diretório atual.")
return None
gpt_selecionado = st.selectbox(
"📁 Selecione um GPT:",
arquivos_json,
format_func=lambda x: extract_gpt_name(x)
)
with tab_search:
busca = st.text_input("🔍 Pesquisa por palavras-chave:", "").lower()
if busca:
arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json") and
f.startswith("gpt_")])
arquivos_filtrados = [
f for f in arquivos_json
if busca in f.lower() or
search_in_json_content(f, busca)
]
if arquivos_filtrados:
gpt_selecionado = st.selectbox(
f"📁 GPTs correspondentes ({len(arquivos_filtrados)}):",
arquivos_filtrados,
format_func=lambda x: extract_gpt_name(x)
)
else:
st.warning("Nenhum GPT corresponde à busca.")
return None
with tab_categories:
categorias = ["Jurídico", "Inteligência Artificial", "Programação", "Escritório", "Pessoal",
"Diversos"]
categoria_selecionada = st.selectbox("Escolha uma categoria:", categorias)
# Simulando filtragem por categoria
arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json") and f.startswith("gpt_")])
arquivos_filtrados = [f for f in arquivos_json if categoria_em_arquivo(f,
categoria_selecionada)]
if arquivos_filtrados:
gpt_selecionado = st.selectbox(
f"📁 GPTs na categoria {categoria_selecionada} ({len(arquivos_filtrados)}):",
arquivos_filtrados,
format_func=lambda x: extract_gpt_name(x)
)
else:
st.info(f"Nenhum GPT encontrado na categoria {categoria_selecionada}.")
return None
return gpt_selecionado
# ===== T(a): GPT Name Extraction =====
def extract_gpt_name(filename):
"""
T(a): Extracts a friendly name from GPT filename
"""
try:
with open(filename, encoding='utf-8') as f:
data = json.load(f)
return data.get("nome_do_gpt", filename.replace(".json", "").replace("gpt_", ""))
except:
return filename.replace(".json", "").replace("gpt_", "")
# ===== T(a): Category Check =====
def categoria_em_arquivo(filename, categoria):
"""
T(a): Checks if a file belongs to a category
"""
try:
with open(filename, encoding='utf-8') as f:
data = json.load(f)
return data.get("categoria", "").lower() == categoria.lower()
except:
return False
# ===== T(a): JSON Content Search =====
def search_in_json_content(filename, query):
"""
T(a): Searches for query within JSON file content
Returns: Boolean indicating if query was found
"""
try:
with open(filename, encoding='utf-8') as f:
data = json.load(f)
content_str = json.dumps(data, ensure_ascii=False).lower()
return query in content_str
except:
return False
# ===== S(s): GPT Rendering Subsequence =====
def process_gpt_rendering(selected_gpt):
"""
S(s): Processes and renders the selected GPT
Returns: GPT data or None on error
"""
try:
# T(a): Load and validate GPT data
with open(selected_gpt, encoding='utf-8') as f:
dados = json.load(f)
if not "nome_do_gpt" in dados:
st.error("O arquivo JSON selecionado não contém a estrutura necessária para um GPT.")
return None
# T(a): Display GPT metadata
st.markdown(f"## 🤖 {dados.get('nome_do_gpt', 'GPT sem nome')}")
# Display category tag
categoria = dados.get("categoria", "Sem categoria")
categoria_class = categoria.lower().replace(" ", "_").replace("ência",
"encia").replace("ção", "cao")
st.markdown(f'<div class="node-box node-{categoria_class}">',
unsafe_allow_html=True)
st.markdown(f"**Categoria:** {categoria}", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
# T(a): Render visualization tabs
tab_details, tab_blocks, tab_actions = st.tabs(["Detalhes", "Blocos Funcionais", "Ações"])
with tab_details:
render_gpt_details(dados)
with tab_blocks:
render_functional_blocks(dados)
with tab_actions:
render_action_buttons(dados)
# Return data for export functions
return {
"dados": dados,
"categoria": categoria
}
except Exception as e:
st.error(f"❌ Erro ao carregar ou renderizar o GPT: {str(e)}")
return None
# ===== T(a): GPT Details Rendering =====
def render_gpt_details(dados):
"""
T(a): Renders detailed information about the GPT
"""
st.subheader("📋 Informações Detalhadas")
# Simulating additional fields that might be in a fuller implementation
descricao = "GPT institucional com lógica fuzzy aplicada para modelagem normativa"
if "blocos_funcionais" in dados and len(dados["blocos_funcionais"]) > 0:
if "descricao" in dados["blocos_funcionais"][0]:
descricao = dados["blocos_funcionais"][0]["descricao"]
st.markdown(f"**Descrição:** {descricao}")
# Tags simulation - would be attributes in real data
st.markdown("**Tags:**")
tags = ["Modelagem", "Jurídico", "Automatização", "Inteligência", "Framework"]
tags_html = ""
for tag in tags:
tags_html += f'<span class="feature-tag">{tag}</span>'
st.markdown(tags_html, unsafe_allow_html=True)
# Usage statistics simulation
st.markdown("### 📊 Estatísticas de Uso")
col1, col2, col3 = st.columns(3)
with col1:
st.metric("Usos Totais", "147")
with col2:
st.metric("Taxa de Sucesso", "92%")
with col3:
st.metric("Último Uso", "2 dias atrás")
# Last updates
st.markdown("### 🔄 Últimas Atualizações")
st.markdown("""
- **12/04/2025**: Atualização de parâmetros fuzzy
- **04/04/2025**: Correção de bugs na geração de documentos
- **28/03/2025**: Inclusão de novos modelos normativos
""")
# Integration information
st.markdown("### 🔌 Integrações")
st.markdown("Este GPT pode ser integrado com:")
st.markdown("""
- Sistema de Gestão de Documentos
- Plataforma Jurídica
- API de Processamento de Linguagem Natural
""")
# ===== T(a): Functional Blocks Rendering =====
def render_functional_blocks(dados):
"""
T(a): Renders functional blocks of the GPT
"""
st.subheader("⚙️ Blocos Funcionais")
if "blocos_funcionais" not in dados or not dados["blocos_funcionais"]:
st.info("Este GPT não possui blocos funcionais definidos.")
return
for bloco in dados["blocos_funcionais"]:
bloco_id = bloco.get("id", "b?")
bloco_nome = bloco.get("nome", "Bloco sem nome")
bloco_tipo = bloco.get("tipo", "indefinido")
bloco_descricao = bloco.get("descricao", "Sem descrição")
st.markdown(f'<div class="node-box node-programacao">', unsafe_allow_html=True)
st.markdown(f'<span class="gpt-id">{bloco_id}</span> • <span
class="module-tag">{bloco_tipo.upper()}</span>', unsafe_allow_html=True)
st.markdown(f"**{bloco_nome}**")
st.markdown(bloco_descricao)
# Display fuzzy parameters if available
if "fuzzy" in bloco:
fuzzy = bloco["fuzzy"]
st.markdown('<div class="fuzzy-score">', unsafe_allow_html=True)
st.markdown("**Parâmetros Fuzzy:**")
cols = st.columns(3)
fuzzy_params = list(fuzzy.items())
for i, (param, value) in enumerate(fuzzy_params):
with cols[i % 3]:
st.markdown(f"**{param}:** {value}")
# Display S(x) if available
if "S(x)" in bloco:
st.markdown(f"**S(x):** {bloco['S(x)']}")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
# Display connections if available
if "conexoes" in dados and dados["conexoes"]:
st.markdown("### 🔄 Fluxo de Conexões")
# Create a graphviz diagram for connections
fluxo = Digraph('Conexões', format='png')
fluxo.attr(
rankdir='TB',
size='8,8',
nodesep='0.7',
ranksep='0.6',
fontname='Arial',
bgcolor='white'
)
# Add nodes and edges
for conexao in dados["conexoes"]:
if len(conexao) >= 2:
origem, destino = conexao
# Add nodes
fluxo.node(origem, origem, shape="box", style="rounded,filled",
fillcolor="#d6eaf8")
fluxo.node(destino, destino, shape="box", style="rounded,filled",
fillcolor="#d6eaf8")
# Add edge
fluxo.edge(origem, destino)
# Display the graph
st.graphviz_chart(fluxo, use_container_width=True)
# ===== T(a): Action Buttons Rendering =====
def render_action_buttons(dados):
"""
T(a): Renders action buttons for GPT
"""
st.subheader("🚀 Ações Rápidas")
# Create columns for buttons
col1, col2, col3 = st.columns(3)
with col1:
st.button("📝 Editar GPT", key="edit_gpt")
st.button("📊 Ver Análises", key="view_stats")
with col2:
st.button("▶️ Executar GPT", key="run_gpt")
st.button("📤 Compartilhar", key="share_gpt")
with col3:
st.button("🔄 Atualizar Parâmetros", key="update_params")
st.button("📋 Clonar GPT", key="clone_gpt")
# Integration code section
st.markdown("### 💻 Código de Integração")
integration_code = """
import openai
# API configuration for this GPT
client = openai.OpenAI(api_key="your_api_key")
# Execute GPT with custom parameters
response = client.chat.completions.create(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a specialized GPT for process automation."},
{"role": "user", "content": "Generate a process flow for document validation."}
],
temperature=0.7,
max_tokens=500
)
print(response.choices[0].message.content)
"""
st.code(integration_code, language="python")
# ===== S(s): Export Options Subsequence =====
def process_export_options(gpt_data, selected_gpt):
"""
S(s): Process and provides export options
"""
st.markdown("---")
st.subheader("📤 Opções de Exportação")
export_col1, export_col2 = st.columns(2)
with export_col1:
if st.button("📄 Exportar como HTML (Documentação)"):
export_html_documentation(gpt_data, selected_gpt)
with export_col2:
if st.button("📊 Exportar como JSON Técnico"):
export_technical_json(gpt_data, selected_gpt)
# ===== T(a): HTML Export =====
def export_html_documentation(gpt_data, selected_gpt):
"""
T(a): Exports GPT as HTML documentation
"""
dados = gpt_data["dados"]
categoria = gpt_data["categoria"]
# Generate enhanced HTML with semantic structures
html_export = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>{dados['nome_do_gpt']} - Documentação</title>
<style>
@import
url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap
');
body {{
font-family: 'Roboto', Arial, sans-serif;
max-width: 21cm;
min-height: 29.7cm;
margin: 1cm auto;
background: #fff;
padding: 2cm;
color: #2c3e50;
box-shadow: 0 0 10px rgba(0,0,0,0.1);
}}
header {{
text-align: center;
border-bottom: 2px solid #3498db;
margin-bottom: 1.5cm;
padding-bottom: 1cm;
}}
header img {{ width: 150px; }}
h1 {{ font-size: 24px; margin: 10px 0 0 0; color: #2c3e50; }}
h2 {{ font-size: 20px; color: #2c3e50; margin-top: 0.5cm; }}
h3 {{ font-size: 18px; color: #34495e; }}
.categoria {{
background: #eef2f7;
padding: 15px;
margin-bottom: 1cm;
border-radius: 8px;
border-left: 5px solid #3498db;
}}
.colunas {{ display: flex; gap: 1.5cm; }}
.col1 {{ flex: 2; }}
.col2 {{ flex: 1; }}
.box {{
padding: 15px;
border-radius: 8px;
margin-bottom: 0.8cm;
box-shadow: 0 1px 3px rgba(0,0,0,0.1);
position: relative;
}}
.box-id {{
position: absolute;
top: -10px;
left: 10px;
background: white;
padding: 2px 8px;
border-radius: 10px;
font-size: 12px;
font-weight: bold;
box-shadow: 0 1px 2px rgba(0,0,0,0.1);
color: #34495e;
}}
.ia {{ background: #d5f5e3; border-left: 5px solid #2ecc71; }}
.juridico {{ background: #d6eaf8; border-left: 5px solid #3498db; }}
.escritorio {{ background: #fef9e7; border-left: 5px solid #f1c40f; }}
.programacao {{ background: #fdedec; border-left: 5px solid #e74c3c; }}
.pessoal {{ background: #f2f3f4; border-left: 5px solid #7f8c8d; }}
.diversos {{ background: #fadbd8; border-left: 5px solid #c0392b; }}
.details-box {{
background: #f8f9fa;
padding: 15px;
border-radius: 8px;
border-left: 5px solid #34495e;
margin-bottom: 1cm;
}}
.feature-tag {{
display: inline-block;
padding: 3px 8px;
background: #eef2f7;
border-radius: 15px;
font-size: 0.8rem;
margin-right: 5px;
margin-bottom: 5px;
color: #34495e;
}}
.category-tag {{
display: inline-block;
padding: 3px 8px;
background: #eef2f7;
border-radius: 12px;
font-size: 12px;
margin-left: 8px;
color: #34495e;
}}
.legend {{
margin-top: 1cm;
background: #f8f9fa;
padding: 15px;
border-radius: 8px;
}}
.legend-item {{
display: flex;
align-items: center;
margin-bottom: 10px;
}}
.legend-color {{
width: 18px;
height: 18px;
border-radius: 3px;
margin-right: 10px;
}}
footer {{
text-align: center;
font-size: 12px;
color: #7f8c8d;
margin-top: 1.5cm;
border-top: 1px solid #eee;
padding-top: 0.5cm;
}}
.fuzzy-module {{
border: 1px dashed #bdc3c7;
padding: 5px 10px;
margin-top: 5px;
font-size: 12px;
border-radius: 5px;
color: #7f8c8d;
}}
.code-box {{
background: #f8f9fa;
padding: 15px;
border-radius: 5px;
border-left: 3px solid #3498db;
font-family: monospace;
font-size: 14px;
overflow-x: auto;
}}
</style>
</head>
<body>
<header>
<img src="data:image/png;base64,{get_image_base64('gptlogo.png')}" alt="GPT
Logo">
<h1>SISTEMA DE CATALOGAÇÃO DE GPTs</h1>
<h2>{dados['nome_do_gpt']}</h2>
</header>
<div class="categoria"><strong>Categoria:</strong> {categoria}</div>
<div class="details-box">
<h3>📝 Descrição e Detalhes</h3>
"""
# Add description
descricao = "GPT institucional com lógica fuzzy aplicada para modelagem normativa"
if "blocos_funcionais" in dados and len(dados["blocos_funcionais"]) > 0:
if "descricao" in dados["blocos_funcionais"][0]:
descricao = dados["blocos_funcionais"][0]["descricao"]
html_export += f"<p>{descricao}</p>"
