# === app.py - Catálogo de MyGPTs ADM. JESUS MARTINS ===
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config("🧠 Catálogo de MyGPTs", layout="wide")

st.title("🧠 MY GPTS – ADM. JESUS MARTINS")
st.markdown("Sistema de visualização de blocos funcionais fuzzy com exportação institucional")

# === Carregamento JSON ===
arquivos = [f for f in os.listdir() if f.endswith(".json")]
arquivo_escolhido = st.sidebar.selectbox("📂 Selecione um MyGPT", arquivos)

if not arquivo_escolhido:
    st.warning("Nenhum arquivo selecionado.")
    st.stop()

with open(arquivo_escolhido, encoding='utf-8') as f:
    gpt_data = json.load(f)

# === Cabeçalho do App ===
st.header(f"📌 Nome: {gpt_data['nome_do_gpt']}")
st.subheader(f"📚 Categoria: {gpt_data['categoria']}")

# === TABS ===
tabs = st.tabs(["📋 Blocos", "🔁 Fluxo", "📊 Fuzzy α → θ", "📄 Exportar HTML"])

# === BLOCOS ===
with tabs[0]:
    for bloco in gpt_data["blocos_funcionais"]:
        with st.expander(f"🔹 {bloco['nome']} ({bloco['tipo']})"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**🆔 ID do Bloco:** `{bloco['id']}`")
                st.markdown(f"**🔖 Tipo:** `{bloco['tipo']}`")
                st.markdown(f"**📝 Descrição:** {bloco['descricao']}")
                st.markdown(f"**🎯 Pertinência S(x):** `{bloco['S(x)']}`")
            with col2:
                st.markdown("**📊 Parâmetros Fuzzy α → θ**")
                fuzzy_data = pd.DataFrame(
                    [{"Parâmetro": k, "Valor": v} for k, v in bloco["fuzzy"].items()]
                )
                st.table(fuzzy_data.set_index("Parâmetro"))

# === FLUXO ===
with tabs[1]:
    st.subheader("🔗 Fluxo de Blocos")

    dot_source = "digraph fluxo {\n  rankdir=LR;\n"
    for b in gpt_data["blocos_funcionais"]:
        dot_source += f'  {b["id"]} [label="{b["nome"]}"];\n'
    for origem, destino in gpt_data["conexoes"]:
        dot_source += f"  {origem} -> {destino};\n"
    dot_source += "}\n"

    st.graphviz_chart(dot_source)

# === FUZZY α → θ ===
with tabs[2]:
    df_fuzzy = pd.DataFrame([
        {**b["fuzzy"], "Bloco": b["nome"], "S(x)": b["S(x)"]} for b in gpt_data["blocos_funcionais"]
    ])
    st.dataframe(df_fuzzy.set_index("Bloco"))

# === EXPORTAÇÃO HTML INSTITUCIONAL ===
with tabs[3]:
    def gerar_html(gpt):
        def bloco_html(b):
            return f"""
      <div class='bloco'>
        <strong>🔹 {b['nome']} ({b['tipo']})</strong>
        <div class='descricao'>📝 {b['descricao']}</div>
        <div class='fuzzy'>
          🆔 ID: <code>{b['id']}</code><br/>
          🎯 S(x): <b>{b['S(x)']}</b><br/>
          <span>α: {b['fuzzy']['α']}</span>
          <span>β: {b['fuzzy']['β']}</span>
          <span>γ: {b['fuzzy']['γ']}</span>
          <span>δ: {b['fuzzy']['δ']}</span>
          <span>ε: {b['fuzzy']['ε']}</span>
          <span>θ: {b['fuzzy']['θ']}</span>
        </div>
      </div>"""

        blocos_html = "\n".join([bloco_html(b) for b in gpt["blocos_funcionais"]])
        fluxo_txt = " → ".join([b["nome"] for b in gpt["blocos_funcionais"]])
        media = pd.DataFrame([b["fuzzy"] for b in gpt["blocos_funcionais"]]).mean().round(2)
        media_s = round(sum(b["S(x)"] for b in gpt["blocos_funcionais"]) / len(gpt["blocos_funcionais"]), 2)

        return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <title>🧠 MY GPTS – Catálogo Institucional</title>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      margin: 2.5cm;
      background: #ffffff;
      color: #2c3e50;
      line-height: 1.6;
    }}
    header {{
      border-bottom: 4px solid #2e86de;
      padding-bottom: 15px;
      margin-bottom: 30px;
    }}
    .logo {{
      font-weight: bold;
      font-size: 22px;
      color: #154360;
    }}
    .subtitulo {{
      font-size: 14px;
      color: #5d6d7e;
      margin-top: 4px;
    }}
    h1 {{
      font-size: 28px;
      color: #1b2631;
    }}
    h2 {{
      font-size: 20px;
      margin-top: 40px;
      color: #273746;
    }}
    .bloco {{
      border-left: 6px solid #3498db;
      background: #f8f9f9;
      padding: 16px;
      margin-bottom: 20px;
      border-radius: 8px;
    }}
    .bloco strong {{
      font-size: 17px;
      color: #1f618d;
    }}
    .descricao {{
      font-weight: bold;
      margin-top: 6px;
    }}
    .fuzzy {{
      margin-top: 10px;
      font-size: 13px;
      color: #444;
      padding-left: 10px;
    }}
    .fuzzy span {{
      display: inline-block;
      min-width: 60px;
    }}
    footer {{
      margin-top: 50px;
      font-size: 11px;
      text-align: center;
      color: #7f8c8d;
      border-top: 1px solid #ccc;
      padding-top: 15px;
    }}
    .fluxo {{
      background: #f0f3f4;
      padding: 10px;
      border-left: 4px solid #2e86de;
      border-radius: 5px;
    }}
    .tabela {{
      margin-top: 15px;
      border-collapse: collapse;
      width: 100%;
    }}
    .tabela th, .tabela td {{
      border: 1px solid #bbb;
      padding: 6px 12px;
      text-align: center;
    }}
    .tabela th {{
      background: #d6eaf8;
    }}
  </style>
</head>
<body>
  <header>
    <div class="logo">ADM. JESUS MARTINS</div>
    <div class="subtitulo">Plataforma Institucional de Catalogação de MyGPTs</div>
  </header>

  <h1>🧠 MyGPT: {gpt['nome_do_gpt']}</h1>
  <h2>📚 Categoria: {gpt['categoria']}</h2>

  {blocos_html}

  <h2>📈 Fluxo entre Blocos</h2>
  <div class="fluxo">{fluxo_txt}</div>

  <h2>📊 Média α → θ</h2>
  <table class="tabela">
    <tr><th>α</th><th>β</th><th>γ</th><th>δ</th><th>ε</th><th>θ</th><th>S(x)</th></tr>
    <tr>
      <td>{media['α']}</td><td>{media['β']}</td><td>{media['γ']}</td><td>{media['δ']}</td>
      <td>{media['ε']}</td><td>{media['θ']}</td><td><b>{media_s}</b></td>
    </tr>
  </table>

  <footer>
    Documento institucional gerado por MY GPTS – ADM. JESUS MARTINS<br>
    {datetime.now().strftime("%d/%m/%Y %H:%M")}
  </footer>
</body>
</html>"""

    html_code = gerar_html(gpt_data)
    st.download_button("📥 Baixar HTML Institucional", data=html_code, file_name="catalogo_mygpt.html", mime="text/html")

# === EXPORTAÇÃO JSON SEMÂNTICO ===
st.markdown("---")
st.subheader("📤 Exportar JSON Semântico")
if st.button("🔽 Baixar JSON"):
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
        st.download_button("📥 Baixar JSON", f, file_name=nome_export)
