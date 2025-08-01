
import streamlit as st
import pandas as pd
import openai
import csv

from utils import (
    genera_descrizione_chatgpt,
    genera_keyphrase,
    genera_sql_update,
)

st.set_page_config(page_title="SiciliaRicambi SEO Generator", layout="centered")

st.title("🚗 SiciliaRicambi SEO Generator con ChatGPT")
st.markdown("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔐 Inserisci la tua API Key OpenAI", type="password")

uploaded_products = st.file_uploader("📂 Carica Products.csv", type="csv")
uploaded_funzioni = st.file_uploader("🧩 Carica Funzioni.csv", type="csv")

modello = st.selectbox("🤖 Seleziona il modello OpenAI", ["gpt-3.5-turbo", "gpt-4o"])

genera = st.button("🎯 Avvia generazione SEO")

if genera:
    if uploaded_products is not None and uploaded_funzioni is not None and api_key:
        openai.api_key = api_key
        df_products = pd.read_csv(uploaded_products)
        df_funzioni = pd.read_csv(uploaded_funzioni)

        descrizioni_html = []
        keyphrases = []
        sql_statements = []

        st.info("⏳ Generazione in corso...")

        for idx, row in df_products.iterrows():
            nome = row.get("NOME PRODOTTO", "")
            codice = row.get("CODICE", "")
            marca = row.get("BRAND NAME", "")
            tipo = row.get("Default Category Name", "")
            keyword = row.get("KEYWORD", "")

            funzioni = df_funzioni[df_funzioni["CODICE"] == codice]

            descrizione_html = genera_descrizione_chatgpt(
                nome, marca, tipo, codice, keyword, modello, api_key, funzioni
            )
            keyphrase = genera_keyphrase(nome, codice, marca, tipo)

            descrizioni_html.append(descrizione_html)
            keyphrases.append(keyphrase)
            sql_statements.append(genera_sql_update(row["ID_PRODOTTO"], keyphrase))

            st.success(f"✅ Completato: {codice}")

        df_products["DESCRIZIONE HTML"] = descrizioni_html
        df_products["KEYPHRASE"] = keyphrases

        df_products.to_csv("seo_output.csv", sep=";", index=False)

        with open("keyphrase_update.sql", "w") as f:
            for statement in sql_statements:
                f.write(statement + "\n")

        with open("seo_output.csv", "rb") as f:
            st.download_button("⬇️ Scarica SEO Output CSV", f, file_name="seo_output.csv", mime="text/csv")

        with open("keyphrase_update.sql", "rb") as f:
            st.download_button("⬇️ Scarica SQL Update", f, file_name="keyphrase_update.sql", mime="text/sql")

    else:
        st.warning("⚠️ Assicurati di caricare entrambi i file e di inserire la tua API Key.")
