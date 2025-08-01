import openai

def genera_keyphrase(nome, marca, tipo, codice):
    parole = [nome, codice, marca]
    if tipo:
        parole.insert(1, tipo)
    return " ".join(parole).upper()

def genera_descrizione_chatgpt(nome, marca, tipo, codice, keyphrase, modello, api_key):
    openai.api_key = api_key
    prompt = f"""Scrivi una descrizione HTML di almeno 300 parole per un ricambio auto. Includi la frase chiave: {keyphrase}. Il ricambio è:
- Nome: {nome}
- Marca: {marca}
- Tipo: {tipo}
- Codice: {codice}

Aggiungi che tutti i ricambi sono garantiti 2 anni, spediti lo stesso giorno lavorativo e disponibili su Siciliaricambi. Inserisci link interni (alla home) e un link esterno utile (Wikipedia, eBay, ecc)."""
    response = openai.ChatCompletion.create(
        model=modello,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

def genera_sql_update(df):
    righe = []
    for _, r in df.iterrows():
        riga = f"UPDATE ps_ets_seo_product SET key_phrase = '{r['focus_keyphrase'].replace("'", "\\'")}' WHERE id_product = {r['id_product']};"
        righe.append(riga)
    return "\n".join(righe)