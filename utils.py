
def genera_descrizione_chatgpt(api_key, nome, marca, tipo, codice, funzioni_df, modello):
    return f"<p>Descrizione fittizia per {nome} - {marca} - {codice}.</p>"

def genera_keyphrase(api_key, nome, marca, tipo, codice):
    return f"{nome} {marca} {codice}"

def genera_sql_update(id_prodotto, descrizione, keyphrase):
    return f"UPDATE ps_product_lang SET description = '{descrizione}', meta_keywords = '{keyphrase}' WHERE id_product = {id_prodotto};"
