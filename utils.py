
import openai
import pandas as pd

def genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, model, api_key):
    openai.api_key = api_key
    prompt = f"""
Sei un esperto di e-commerce automotive. Genera una descrizione ottimizzata SEO in HTML per il seguente prodotto:

- Nome prodotto: {nome}
- Marca veicolo: {marca}
- Tipo: {tipo}
- Codice: {codice}
- Keyword principale: {keyword}

La descrizione deve essere in HTML, fluida, dettagliata e con tono professionale.
Deve includere:
- la marca del ricambio
- la garanzia di 2 anni
- la spedizione veloce
- un link interno a https://www.siciliaricambi.com
- un link esterno informativo

Inizia subito con la descrizione, non serve ripetere le informazioni.
"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Sei un esperto copywriter e SEO specializzato in ricambi auto."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

def genera_keyphrase(nome, tipo, marca):
    keyword = f"{nome} {tipo} per {marca}".lower()
    keyword = keyword.replace("  ", " ").strip()
    return keyword

def genera_sql_update(id_prodotto, keyphrase):
    escaped_keyphrase = keyphrase.replace("'", "\'")
    query = f"UPDATE ps_product_lang SET meta_keywords = '{escaped_keyphrase}' WHERE id_product = {id_prodotto} AND id_lang = 4;"
    return query
