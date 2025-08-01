
import streamlit as st
import pandas as pd
import openai
from utils import genera_descrizione_chatgpt, genera_keyphrase, genera_sql_update

st.set_page_config(page_title="SiciliaRicambi SEO Generator", layout="centered")
st.title("📦 SiciliaRicambi SEO Generator con ChatGPT")
st.markdown("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔐 Inserisci la tua API Key OpenAI", type="password")
uploaded_file = st.file_uploader("📂 Carica Products.csv", type=["csv"])
uploaded_funzioni = st.file_uploader("🧩 Carica Funzioni.csv", type=["csv"])
modello = st.selectbox("💬 Seleziona il modello OpenAI", ["gpt-3.5-turbo", "gpt-4o"])

if st.button("🚀 Avvia generazione SEO"):
    if not api_key or not uploaded_file or not uploaded_funzioni:
        st.error("Per favore carica tutti i file richiesti e inserisci la chiave API.")
    else:
        try:
            df_prodotti = pd.read_csv(uploaded_file)
            df_funzioni = pd.read_csv(uploaded_funzioni, encoding='latin1', sep=';', on_bad_lines='skip')  # FIX
            risultati = []
            for _, row in df_prodotti.iterrows():
                id_prodotto = row["ID"]
                nome = row["TITOLO"]
                marca = row["BRAND NAME"]
                tipo = row["Default Category Name"]
                codice = row["CODICE"]
                keyword = row.get("Keyword", "")
                funzioni = df_funzioni[df_funzioni["CODICE"] == codice]
                descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, api_key, funzioni)
                keyphrase = genera_keyphrase(nome, marca, tipo, codice)
                risultati.append((id_prodotto, nome, keyphrase, descrizione_html))
            df_result = pd.DataFrame(risultati, columns=["id_product", "Titolo", "Focus Keyphrase", "Descrizione HTML"])
            st.success("✅ Descrizioni generate con successo!")
            st.dataframe(df_result)
            csv_data = df_result.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Scarica CSV risultati", csv_data, file_name="descrizioni_seo.csv", mime="text/csv")
            sql_script = genera_sql_update(df_result)
            st.download_button("🧾 Scarica Script SQL", sql_script.encode("utf-8"), file_name="update_keyphrases.sql", mime="text/sql")
        except Exception as e:
            st.error(f"Errore durante la generazione SEO: {str(e)}")
