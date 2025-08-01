import streamlit as st
import pandas as pd
from utils import genera_descrizione_chatgpt, genera_keyphrase, genera_sql_update

st.set_page_config(page_title="SEO Generator - SiciliaRicambi", layout="wide")

st.title("🔧 Generatore SEO per SiciliaRicambi")

uploaded_products = st.file_uploader("Carica il file Products.csv", type=["csv"])
uploaded_funzioni = st.file_uploader("Carica il file Funzioni.csv", type=["csv"])

modello = st.selectbox("Scegli il modello OpenAI", ["gpt-4", "gpt-3.5-turbo"])
api_key = st.text_input("Inserisci la tua API Key OpenAI", type="password")

if uploaded_products and uploaded_funzioni and api_key:
    try:
try:
    df_products = pd.read_csv(uploaded_products, encoding='utf-8')
except UnicodeDecodeError:
    df_products = pd.read_csv(uploaded_products, encoding='latin1')
    except Exception:

    try:
        df_funzioni = pd.read_csv(uploaded_funzioni, encoding="utf-8", sep=";")
    except Exception:
        df_funzioni = pd.read_csv(uploaded_funzioni, encoding="latin1", sep=";")

    results = []

    for _, row in df_products.iterrows():
        try:
            id_prodotto = row["Product ID"]
            nome = row["Nome"]
            marca = row["Brand Name"]
            tipo = row.get("Tipo", "") or ""
            codice = row["Riferimento"]

            funzioni = df_funzioni[df_funzioni["ID Prodotto"] == id_prodotto]
            keyword = genera_keyphrase(nome, marca, tipo, codice, funzioni)
            descrizione_html = genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, api_key)
            results.append({"ID Prodotto": id_prodotto, "Titolo": nome, "Focus Keyphrase": keyword, "Descrizione HTML": descrizione_html})
        except Exception as e:
            st.error(f"Errore durante la generazione SEO: {e}")

    if results:
        df_result = pd.DataFrame(results)
        st.success("✅ Generazione completata!")
        st.dataframe(df_result)

        csv = df_result.to_csv(index=False, sep=";").encode("utf-8")
        st.download_button("📥 Scarica Descrizioni SEO", csv, "descrizioni_seo.csv", "text/csv")

        # Genera anche lo script SQL
        sql_script = genera_sql_update(df_result)
        st.download_button("📥 Scarica Script SQL", sql_script.encode("utf-8"), "update_keyphrases.sql", "text/sql")

# Mostra query SQL di esportazione da PrestaShop
with st.expander("📤 Query per esportare le funzioni dal database MySQL"):
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
    p.id_product;
""", language="sql")