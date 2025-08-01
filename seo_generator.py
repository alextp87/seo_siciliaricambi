import streamlit as st
import pandas as pd
import openai
from utils import (
    genera_descrizione_chatgpt,
    genera_keyphrase,
    genera_sql_update
)

st.set_page_config(page_title="SEO Generator - SiciliaRicambi", layout="centered")

st.title("🧠 SEO Generator per SiciliaRicambi")

api_key = st.text_input("🔑 API Key OpenAI", type="password")
modello = st.selectbox("🤖 Modello da usare", ["gpt-4", "gpt-3.5-turbo"])


uploaded_products = st.file_uploader("📦 Carica il file Products.csv", type="csv")
uploaded_funzioni = st.file_uploader("⚙️ Carica il file FUNZIONI.csv", type="csv")

if uploaded_products and uploaded_funzioni and api_key:
    df_products = pd.read_csv(uploaded_products, encoding='utf-8', delimiter=';')
    df_funzioni = pd.read_csv(uploaded_funzioni, encoding='latin1', delimiter=';')

    results = []
    for _, row in df_products.iterrows():
        id_prodotto = row['ID']
        nome = row['NOME']
        marca = row['BRAND NAME']
        tipo = row.get('TIPO', '') or ''
        codice = row['CODICE']
        keyword = genera_keyphrase(nome, marca, tipo, codice)
        descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, api_key)
        results.append({
            'id_product': id_prodotto,
            'focus_keyphrase': keyword,
            'descrizione_html': descrizione_html
        })

    df_result = pd.DataFrame(results)
    st.success("✅ Generazione completata!")

    csv = df_result.to_csv(index=False, sep=';', encoding='utf-8')
    st.download_button("⬇️ Scarica CSV con Keyphrase e Descrizioni", csv, file_name="seo_output.csv", mime="text/csv")

    sql_script = genera_sql_update(df_result)
    st.download_button("🗄️ Scarica Script SQL per Keyphrase", sql_script, file_name="importa_keyphrase.sql")

if st.button("📤 Mostra query SQL per esportare le FUNZIONI da PrestaShop"):
    st.code("""SELECT
    p.id_product AS 'ID Prodotto',
    pl.name AS 'Nome Prodotto',
    f.id_feature AS 'ID Funzione',
    fl.name AS 'Nome Funzione',
    fv.id_feature_value AS 'ID Valore Funzione',
    fvl.value AS 'Valore Funzione'
FROM
    ps_product p
JOIN
    ps_product_lang pl ON p.id_product = pl.id_product
JOIN
    ps_feature_product fp ON p.id_product = fp.id_product
JOIN
    ps_feature f ON fp.id_feature = f.id_feature
JOIN
    ps_feature_lang fl ON f.id_feature = fl.id_feature
JOIN
    ps_feature_value fv ON fp.id_feature_value = fv.id_feature_value
JOIN
    ps_feature_value_lang fvl ON fv.id_feature_value = fvl.id_feature_value
ORDER BY
    p.id_product;""", language='sql')