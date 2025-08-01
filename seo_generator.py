
import streamlit as st
import pandas as pd
from utils import genera_descrizione_chatgpt, genera_keyphrase, genera_sql_update

st.set_page_config(page_title="SEO con ChatGPT", layout="centered")

st.title("con ChatGPT")
st.write("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔑 Inserisci la tua API Key OpenAI", type="password")

products_file = st.file_uploader("📂 Carica il file Products.csv", type=["csv"])
funzioni_file = st.file_uploader("📂 Carica il file Funzioni.csv", type=["csv"])

modello = st.selectbox("📉 Scegli il modello OpenAI", ["gpt-3.5-turbo", "gpt-4", "gpt-4o"])

if st.button("📄 Mostra query SQL per estrarre le funzioni"):
    st.code("""
SELECT
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
    p.id_product;
    """)

if st.button("🚀 Avvia generazione SEO") and api_key and products_file and funzioni_file:
    try:
        df_products = pd.read_csv(products_file, sep=';', encoding='utf-8')
        df_funzioni = pd.read_csv(funzioni_file, sep=';', encoding='utf-8')
        results = []

        for _, row in df_products.iterrows():
            id_prodotto = row['Product ID']
            nome = row['Nome']
            marca = row['Brand Name']
            tipo = row.get('TIPO', '') or ''
            codice = row['Riferimento']

            funzioni_prodotto = df_funzioni[df_funzioni['ID Prodotto'] == id_prodotto]
            descrizione = genera_descrizione_chatgpt(api_key, nome, marca, tipo, codice, funzioni_prodotto, modello)
            keyphrase = genera_keyphrase(api_key, nome, marca, tipo, codice)
            sql = genera_sql_update(id_prodotto, descrizione, keyphrase)

            results.append(sql)

        st.success(f"✅ Generazione completata. Sono state generate {len(results)} query.")
        st.code("\n\n".join(results))

    except Exception as e:
        st.error(f"Errore durante la generazione SEO: {e}")
