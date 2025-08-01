
import streamlit as st
import pandas as pd
import openai
from utils import (
    genera_descrizione_chatgpt,
    genera_keyphrase,
    genera_sql_update,
)

st.set_page_config(page_title="SiciliaRicambi SEO Generator con ChatGPT", layout="centered")

st.title("🚗 SiciliaRicambi SEO Generator con ChatGPT")
st.markdown("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔐 Inserisci la tua API Key OpenAI", type="password")

uploaded_products = st.file_uploader("📂 Carica Products.csv", type="csv")
uploaded_funzioni = st.file_uploader("⚙️ Carica Funzioni.csv", type="csv")

modello = st.selectbox("🧠 Seleziona il modello OpenAI", ["gpt-3.5-turbo", "gpt-4"])

if st.button("🚀 Avvia generazione SEO"):
    if not api_key or not uploaded_products or not uploaded_funzioni:
        st.error("Carica tutti i file richiesti e inserisci la tua API Key.")
    else:
        df_prodotti = pd.read_csv(uploaded_products)
        df_funzioni = pd.read_csv(uploaded_funzioni, encoding='latin1')  # FIX APPLICATO

        descrizioni = []
        keyphrases = []

        for idx, row in df_prodotti.iterrows():
            nome = row.get("nome_prodotto", "")
            codice = row.get("codice_prodotto", "")
            marca = row.get("brand_name", "")
            tipo = row.get("default_category_name", "")

            keyword = genera_keyphrase(nome, marca, tipo, codice)
            descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, api_key)

            descrizioni.append(descrizione_html)
            keyphrases.append(keyword)

        df_prodotti["descrizione_html"] = descrizioni
        df_prodotti["key_phrase"] = keyphrases

        st.success("✅ Descrizioni SEO generate con successo!")
        st.download_button("📥 Scarica Descrizioni CSV", df_prodotti.to_csv(index=False).encode("utf-8"), "descrizioni_seo.csv", "text/csv")

        sql = genera_sql_update(df_prodotti[["id_product", "key_phrase"]])
        st.download_button("🧩 Scarica Query SQL", sql.encode("utf-8"), "update_keyphrases.sql", "text/sql")
