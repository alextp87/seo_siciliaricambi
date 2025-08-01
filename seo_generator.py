
import streamlit as st
import pandas as pd
from collections import defaultdict

st.set_page_config(page_title="SiciliaRicambi SEO Generator", layout="wide")

st.title("🚀 SiciliaRicambi SEO Generator")
st.write("Genera descrizioni, meta title, meta description e script SQL per ETS SEO")

uploaded_products = st.file_uploader("Carica Products.csv", type=["csv"])
uploaded_functions = st.file_uploader("Carica Funzioni.csv", type=["csv"])

mode = st.radio("Modalità generazione descrizioni", ["ETS SEO (senza link)", "Google SEO (con link)"])

def genera_descrizione(nome, marca, tipo, codice, keyword, mode):
    keyphrase = keyword
    descrizione = f"""
<p>{keyphrase} è un ricambio auto di qualità progettato per offrire affidabilità e durata nel tempo. 
Realizzato con materiali resistenti, è indicato per chi desidera mantenere il proprio veicolo in condizioni ottimali.</p>

<p>Questo {tipo.lower()} originale {marca} è compatibile con i veicoli indicati e corrisponde al codice OEM {codice}. 
La nostra keyphrase principale {keyphrase} appare più volte per evidenziare la pertinenza SEO.</p>

<ul>
<li>Prodotto originale e testato per garantire massima compatibilità.</li>
<li>Resistente all’usura, ideale per manutenzione o sostituzione.</li>
<li>Coperto da 2 anni di garanzia ufficiale.</li>
<li>Spedizione rapida in tutta Italia.</li>
</ul>

<p>{keyphrase} è la soluzione perfetta per chi vuole mantenere prestazioni e sicurezza.
L'installazione consigliata è presso officine specializzate, seguendo le istruzioni del costruttore.</p>

<p>Controlla sempre la corrispondenza del codice OEM {codice} prima dell'acquisto.
Scegliendo {keyphrase} garantisci compatibilità, durata e tranquillità nella guida.</p>
"""
    if mode == "Google SEO (con link)":
        descrizione += f'<p>Scopri di più sui ricambi auto su <a href="https://it.wikipedia.org/wiki/Autoveicolo" target="_blank">Wikipedia</a>.</p>'
    return descrizione.strip()

if uploaded_products and uploaded_functions:
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
        meta_description = f"Acquista {keyword} originale, spedizione veloce e 2 anni di garanzia."
        meta_description = meta_description[:156]

        descrizione_html = genera_descrizione(nome, marca, tipo, codice, keyword, mode)

        output_rows.append([pid, nome, meta_title, meta_description, keyword, descrizione_html])
        sql_rows.append(f"({pid}, '{keyword.replace("'", "''")}')")

    final_df = pd.DataFrame(output_rows, columns=[
        'ID_PRODOTTO','NOME_PRODOTTO','META_TITLE','META_DESCRIPTION','KEYWORD','DESCRIZIONE_HTML'
    ])
    st.download_button("⬇️ Scarica CSV ottimizzato", data=final_df.to_csv(sep=';', index=False, encoding='utf-8'), file_name="ets_seo_products_optimized.csv", mime="text/csv")

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

SELECT id_product, key_phrase FROM ps_ets_seo_product WHERE key_phrase IS NOT NULL LIMIT 20;

DROP TABLE tmp_focus_keywords;
"""
    st.download_button("⬇️ Scarica Script SQL", data=sql_script, file_name="import_keyphrase.sql", mime="text/plain")

    st.success("✅ CSV e Script SQL pronti!")
