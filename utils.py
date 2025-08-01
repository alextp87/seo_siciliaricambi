import re

def normalizza_testo(testo):
    """Rimuove spazi, caratteri speciali e converte in lowercase"""
    if not isinstance(testo, str):
        return ""
    testo = testo.strip().lower()
    testo = re.sub(r'[^\w\s-]', '', testo)
    testo = re.sub(r'[-\s]+', ' ', testo)
    return testo

def crea_keyphrase(nome_prodotto, marca, codice):
    """Genera una keyphrase SEO unendo nome, marca e codice"""
    return f"{nome_prodotto} {marca} {codice}".strip()

def crea_meta_title(nome_prodotto):
    """Genera un meta title sintetico e ottimizzato"""
    base = nome_prodotto.strip().upper()
    if len(base) > 65:
        return base[:62] + "..."
    return base

def crea_meta_description(nome_prodotto, marca):
    """Genera una meta description SEO-friendly"""
    return f"Scopri {nome_prodotto} per {marca}. Disponibile con spedizione immediata e 2 anni di garanzia."

def valida_valore(valore):
    """Restituisce una stringa valida o vuota"""
    return str(valore).strip() if valore else ""
