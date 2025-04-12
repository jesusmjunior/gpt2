# === app.py - Compatível com Streamlit Cloud + Exportação HTML ===
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
tabs = st.tabs(["📋 Blocos", "🔁 Fluxo", "📊 Fuzzy α → θ", "📄 Exportar HTML"])

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
<html lang="pt-br"><head><meta charset="UTF-8" />
<title>MyGPT – Catalogação</title>
<style>
body {{ font-family: 'Roboto', sans-serif; padding: 2cm; max-width: 21cm; margin: auto; }}
h1 {{ font-size: 24px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
.bloco {{ margin-bottom: 1em; padding: 1em; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.inicio {{ background: #d5f5e3; border-left: 5px solid #2ecc71; }}
.ação {{ background: #d6eaf8; border-left: 5px solid #3498db; }}
.output {{ background: #fdedec; border-left: 5px solid #e74c3c; }}
.validação {{ background: #fef9e7; border-left: 5px solid #f1c40f; }}
.fim {{ background: #fadbd8; border-left: 5px solid #c0392b; }}
.fuzzy {{ font-size: 13px; color: #555; margin-top: 5px; }}
</style></head><body>
<h1>🧠 MyGPT – Catalogação</h1>
<h3>📚 Categoria: {gpt["categoria"]}</h3>
{blocos_html}
<section><h4>📈 Fluxo:</h4><p>{fluxo_txt}</p></section>
<footer><p style="font-size:12px;color:#888;">Gerado automaticamente – Plataforma COGEX</p></footer>
</body></html>"""

    html_code = gerar_html(gpt_data)
    st.download_button("📥 Baixar HTML Institucional", data=html_code, file_name="catalogo_mygpt.html", mime="text/html")
    st.code(html_code, language="html")

# === Exportação JSON Técnico (padrão) ===
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
