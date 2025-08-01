import streamlit as st
import pandas as pd
import openai
from utils import genera_descrizione_chatgpt, genera_keyphrase, genera_sql_update

st.set_page_config(page_title="SiciliaRicambi SEO Generator", layout="centered")

st.title("🛠️ SiciliaRicambi SEO Generator con ChatGPT")
st.markdown("Genera descrizioni SEO dinamiche utilizzando l'intelligenza artificiale di OpenAI.")

api_key = st.text_input("🔐 Inserisci la tua API Key OpenAI", type="password")

uploaded_products = st.file_uploader("📂 Carica Products.csv", type=["csv"])
uploaded_funzioni = st.file_uploader("🍀 Carica Funzioni.csv", type=["csv"])

model = st.selectbox("💬 Seleziona il modello OpenAI", ["gpt-3.5-turbo", "gpt-4"])

show_query = st.button("📄 Mostra SQL per estrazione Funzioni da MySQL")

if show_query:
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
    p.id_product;""", language="sql")

if st.button("🚀 Avvia generazione SEO"):
    if not api_key or not uploaded_products or not uploaded_funzioni:
        st.error("Per favore, inserisci la tua API key e carica entrambi i file CSV.")
    else:
        try:
            df_products = pd.read_csv(uploaded_products, encoding='latin1')


            results = []
            for _, row in df_products.iterrows():
                id_prodotto = row['Product ID']
                nome = row['Nome']
                marca = row['Brand Name']
                tipo = row.get('Tipo', '') or ''
                codice = row.get('Riferimento', '')
                keyword = genera_keyphrase(nome, marca, tipo)
                descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, model, api_key)
                query_sql = genera_sql_update(id_prodotto, keyword)

                results.append({
                    "ID": id_prodotto,
                    "Titolo": nome,
                    "KeyPhrase": keyword,
                    "Descrizione HTML": descrizione_html,
                    "Query SQL": query_sql
                })

            df_output = pd.DataFrame(results)
            st.success("✅ Generazione completata!")
            st.download_button("💾 Scarica il risultato", df_output.to_csv(index=False).encode('utf-8'), file_name="descrizioni_seo.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Errore durante la generazione SEO: {e}")
