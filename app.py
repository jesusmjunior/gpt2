# === app.py - Catálogo de MyGPTs ADM. JESUS MARTINS ===
import streamlit as st
import json
import os
import pandas as pd

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
            st.markdown(f"📝 {bloco['descricao']}")
            st.write("🔬 Pertinência S(x):", bloco["S(x)"])
            st.json(bloco["fuzzy"])

# === FLUXO ===
with tabs[1]:
    st.subheader("🔗 Fluxo de Blocos")
    dot_source = "digraph fluxo {\nrankdir=LR;\n"
    for b in gpt_data["blocos_funcionais"]:
        dot_source += f'{b["id"]} [label="{b["nome"]}"];\n'
    for origem, destino in gpt_data["conexoes"]:
        dot_source += f"{origem} -> {destino};\n"
    dot_source += "}"
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
            <div class="bloco {b['tipo']}" data-id="{b['id']}">
              <strong>{b['nome']}</strong>
              <p>{b['descricao']}</p>
              <div class="fuzzy">S(x): {b['S(x)']} | α: {b['fuzzy']['α']} | β: {b['fuzzy']['β']} | γ: {b['fuzzy']['γ']} | δ: {b['fuzzy']['δ']} | ε: {b['fuzzy']['ε']} | θ: {b['fuzzy']['θ']}</div>
            </div>"""

        blocos_html = "\n".join([bloco_html(b) for b in gpt["blocos_funcionais"]])
        fluxo_txt = " → ".join([gpt["blocos_funcionais"][0]["nome"]] +
                               [b["nome"] for b in gpt["blocos_funcionais"][1:]])

        return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <title>MY GPTS – Catalogação</title>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      margin: 2cm;
      background: #fff;
      color: #2c3e50;
    }}
    header {{
      border-bottom: 3px solid #2e86de;
      margin-bottom: 2em;
    }}
    .logo {{
      font-weight: bold;
      font-size: 20px;
      color: #154360;
    }}
    .institucional {{
      font-size: 14px;
      margin-top: 5px;
      color: #2c3e50;
    }}
    h1 {{
      font-size: 22px;
      margin-top: 1.5em;
    }}
    .bloco {{
      padding: 1em;
      margin-top: 1em;
      border-left: 5px solid #3498db;
      background: #ecf0f1;
      border-radius: 6px;
    }}
    .bloco span.tipo {{
      font-weight: bold;
      color: #2980b9;
    }}
    .fuzzy {{
      font-size: 13px;
      margin-top: 5px;
      color: #555;
    }}
    .legenda, .metrica {{
      margin-top: 2em;
    }}
    footer {{
      margin-top: 3cm;
      font-size: 11px;
      color: #7f8c8d;
      border-top: 1px solid #ccc;
      padding-top: 0.5cm;
      text-align: center;
    }}
  </style>
</head>
<body>
  <header>
    <div class="logo">ADM. JESUS MARTINS</div>
    <div class="institucional">
      MY GPTS – Catálogo de Blocos Funcionais Inteligentes<br>
      Gerado a partir de modelos JSON estruturados
    </div>
  </header>

  <h1>📋 Fluxo de Processo</h1>
  {blocos_html}
  <section class="legenda">
    <h2>📈 Fluxo entre Blocos</h2>
    <p>{fluxo_txt}</p>
  </section>

  <footer>
    Relatório gerado automaticamente por MY GPTS – Plataforma ADM. JESUS MARTINS<br>
    Data: 12/04/2025
  </footer>
</body>
</html>"""

    html_code = gerar_html(gpt_data)
    st.download_button("📥 Baixar HTML Institucional", data=html_code, file_name="catalogo_mygpt.html", mime="text/html")
    st.code(html_code, language="html")

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
