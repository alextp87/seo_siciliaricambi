
import re
from openai import OpenAI

def normalizza_testo(testo):
    if not isinstance(testo, str):
        return ""
    testo = testo.strip().lower()
    testo = re.sub(r'[^\w\s-]', '', testo)
    testo = re.sub(r'[-\s]+', ' ', testo)
    return testo

def genera_keyphrase(nome_prodotto, marca, codice):
    return f"{nome_prodotto} {marca} {codice}".strip()

def crea_meta_title(nome_prodotto):
    base = nome_prodotto.strip().upper()
    if len(base) > 65:
        return base[:62] + "..."
    return base

def crea_meta_description(nome_prodotto, marca):
    return f"Scopri {nome_prodotto} per {marca}. Disponibile con spedizione immediata e 2 anni di garanzia."

def valida_valore(valore):
    return str(valore).strip() if valore else ""

def genera_descrizione_chatgpt(nome, marca, tipo, codice, keyword, modello, api_key, funzioni=None):
    client = OpenAI(api_key=api_key)

    prompt = f"""
Sei un esperto SEO nel settore ricambi auto. Scrivi una descrizione HTML ottimizzata per un ricambio con le seguenti informazioni:

- Nome prodotto: {nome}
- Marca veicolo: {marca}
- Tipo: {tipo}
- Codice OEM: {codice}
- Keyword target: {keyword}
- Funzioni aggiuntive: {funzioni.to_dict('records')[0] if funzioni is not None and not funzioni.empty else "Nessuna"}

La descrizione deve contenere:
- Almeno 300 parole
- Il codice prodotto e il marchio in evidenza
- Un link interno a https://www.siciliaricambi.com
- Un link esterno utile (es: Wikipedia o sito tecnico generico)
- 2 anni di garanzia e spedizione immediata
- Struttura in HTML con <p> e <ul> chiari
- Frase chiave principale ripetuta 3 volte nel testo

Scrivi la descrizione in modo chiaro e professionale, senza link esterni espliciti nel codice.
"""

    response = client.chat.completions.create(
        model=modello,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1400
    )

    return response.choices[0].message.content

def genera_sql_update(tabella="ps_ets_seo_product", campo="key_phrase", id_field="id_product", temp_table="tmp_focus_keywords"):
    return f"""
UPDATE {tabella} AS seo
JOIN {temp_table} AS tmp ON seo.{id_field} = tmp.{id_field}
SET seo.{campo} = tmp.{campo};
"""
