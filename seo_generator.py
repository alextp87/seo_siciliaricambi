
import streamlit as st
import pandas as pd
from openai import OpenAI
from collections import defaultdict

st.set_page_config(page_title="SiciliaRicambi SEO Generator (ChatGPT)", layout="wide")

st.title("🤖 SiciliaRicambi SEO Generator con ChatGPT")
st.write("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔐 Inserisci la tua API Key OpenAI", type="password")

uploaded_products = st.file_uploader("📦 Carica Products.csv", type=["csv"])
uploaded_functions = st.file_uploader("⚙️ Carica Funzioni.csv", type=["csv"])
model = st.selectbox("🧠 Seleziona il modello OpenAI", ["gpt-3.5-turbo", "gpt-4o"])

def genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, key):
    prompt = f"""Sei un copywriter SEO professionale. Genera una descrizione HTML di almeno 300 parole per un prodotto automobilistico.
Dati del prodotto:
- Nome: {nome}
- Marca del ricambio: {marca}
- Tipo: {tipo}
- Codice OE: {codice}
- Keyword principale: {keyword}

Usa un linguaggio professionale, includi almeno 3 volte la keyword e rendi la descrizione adatta per un sito ecommerce.
Includi punti elenco HTML, usa paragrafi ben strutturati e mantieni uno stile coerente."""

    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model=modello,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

if uploaded_products and uploaded_functions and api_key:
    products_df = pd.read_csv(uploaded_products, encoding='utf-8', sep=None, engine='python')
    funzioni_df = pd.read_csv(uploaded_functions, encoding='latin1', sep=None, engine='python')

    funzioni_grouped = defaultdict(dict)
    for _, row in funzioni_df.iterrows():
        pid = row['ID_Prodotto']
        funzione = str(row['Funzione']).strip()
        valore = str(row['Valore']).strip()
        funzioni_grouped[pid][funzione] = valore

    output_rows = []
    sql_rows = []

    for _, row in products_df.iterrows():
        pid = str(row.iloc[0]).strip()
        nome = str(row['Nome']).strip()
        funzioni_dict = funzioni_grouped.get(int(pid), {})
        marca = funzioni_dict.get('MARCA DEL RICAMBIO', '')
        tipo = funzioni_dict.get('Tipo', 'Ricambio auto')
        codice = funzioni_dict.get('Codice ricambio originale OE/OEM', '')

        keyword = f"{nome} {marca}".strip()
        meta_title = keyword[:60]
        meta_description = f"Acquista {keyword} originale, spedizione veloce e 2 anni di garanzia."[:156]

        descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, model, api_key)

        output_rows.append([pid, nome, meta_title, meta_description, keyword, descrizione_html])
        sql_rows.append(f"({pid}, '{keyword.replace("'", "''")}')")

    final_df = pd.DataFrame(output_rows, columns=[
        'ID_PRODOTTO','NOME_PRODOTTO','META_TITLE','META_DESCRIPTION','KEYWORD','DESCRIZIONE_HTML'
    ])
    st.download_button("⬇️ Scarica CSV ottimizzato", data=final_df.to_csv(sep=';', index=False, encoding='utf-8'), file_name="ets_seo_chatgpt.csv", mime="text/csv")

    sql_script = f"""
CREATE TABLE tmp_focus_keywords (
    id_product INT,
    key_phrase VARCHAR(191)
);

INSERT INTO tmp_focus_keywords (id_product, key_phrase) VALUES
{",".join(sql_rows)};

UPDATE ps_ets_seo_product AS seo
JOIN tmp_focus_keywords AS tmp
  ON seo.id_product = tmp.id_product
SET seo.key_phrase = tmp.key_phrase;

DROP TABLE tmp_focus_keywords;
"""
    st.download_button("⬇️ Scarica Script SQL", data=sql_script, file_name="import_keyphrase.sql", mime="text/plain")

    st.success("✅ File pronti e generati con ChatGPT!")
