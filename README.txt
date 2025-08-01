# SiciliaRicambi SEO Generator

Uno strumento automatizzato per generare descrizioni prodotto, meta title, meta description e keyphrase ottimizzate per il modulo ETS SEO di PrestaShop.

## ✅ Requisiti
- Python 3.8+
- Librerie: `streamlit`, `pandas`

Installa i requisiti con:
```
pip install -r requirements.txt
```

## 📂 File richiesti

### 1. Products.csv
- Contiene:
  - `ID_Prodotto` (colonna 1)
  - `Nome` (nome del prodotto)

### 2. Funzioni.csv
- Contiene:
  - `ID_Prodotto`
  - `Funzione`
  - `Valore`

## 🚀 Come si usa

1. Avvia il tool:
```bash
streamlit run seo_generator.py
```

2. Carica `Products.csv` e `Funzioni.csv`

3. Scegli la modalità SEO

4. Scarica:
   - `ets_seo_products_optimized.csv`
   - `import_keyphrase.sql`

## 🛠️ Import in PrestaShop

### CSV
- Importa `ets_seo_products_optimized.csv` nel modulo ETS SEO mappando:
  - Nome prodotto
  - Meta title
  - Meta description
  - Keyphrase
  - Descrizione

### SQL
- Esegui `import_keyphrase.sql` nel tuo MySQL

