
import streamlit as st
import pandas as pd
from utils import genera_descrizione_chatgpt, genera_keyphrase, genera_sql_update

st.set_page_config(layout="wide")

st.title("🔧 SiciliaRicambi - SEO Generator")

uploaded_file = st.file_uploader("📥 Carica il file prodotti (CSV)", type="csv")
uploaded_funzioni = st.file_uploader("📥 Carica il file delle funzioni (CSV)", type="csv")

if uploaded_file is not None and uploaded_funzioni is not None:
    try:
        df_products = pd.read_csv(uploaded_file, encoding='latin1')
        df_funzioni = pd.read_csv(uploaded_funzioni, encoding='latin1')
    except Exception as e:
        st.error(f"Errore durante il caricamento dei file CSV: {e}")
        st.stop()

    results = []
    for _, row in df_products.iterrows():
        try:
            id_prodotto = row['Product ID']
            nome = row['Nome']
            marca = row['Brand Name']
            tipo = row.get('TIPO', '') or ''
            codice = row['Riferimento']
            funzioni = df_funzioni[df_funzioni['ID Prodotto'] == id_prodotto]
            descrizione = genera_descrizione_chatgpt(nome, marca, tipo, codice, funzioni)
            keyphrase = genera_keyphrase(nome, marca)
            query = genera_sql_update(id_prodotto, descrizione, keyphrase)
            results.append({
                'ID': id_prodotto,
                'Titolo': nome,
                'Keyword': keyphrase,
                'Descrizione HTML': descrizione,
                'Query SQL': query
            })
        except Exception as e:
            st.error(f"Errore durante la generazione SEO: {e}")
            st.stop()

    df_results = pd.DataFrame(results)
    st.success("✅ Generazione completata.")
    st.dataframe(df_results)

    csv = df_results.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("📤 Scarica risultati CSV", csv, "seo_results.csv", "text/csv")

    if st.button("📄 Mostra Query SQL per esportare le funzioni"):
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
