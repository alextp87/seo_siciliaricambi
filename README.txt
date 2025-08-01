# SiciliaRicambi SEO Generator (con ChatGPT)

## Requisiti
- Python 3.8+
- Librerie: streamlit, pandas, openai, python-dotenv

## Avvio
1. Inserisci la tua API key nel file `.env`:
   ```
   OPENAI_API_KEY=sk-xxxxxx
   ```

2. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

3. Avvia il tool:
   ```
   streamlit run seo_generator.py
   ```

## Input
- `Products.csv` con: ID_Prodotto, Nome
- `Funzioni.csv` con: ID_Prodotto, Funzione, Valore

## Output
- CSV ottimizzato per ETS SEO
- SQL per keyphrase nel DB
