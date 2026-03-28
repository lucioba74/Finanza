import streamlit as st
import yfinance as yf
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Dashboard Finanziaria Luciano", layout="wide")
st.title("📈 Analisi Asset Finanziari")

# Sidebar per le impostazioni
st.sidebar.header("Parametri")
periodo = st.sidebar.selectbox("Seleziona Periodo", ["1mo", "6mo", "1y", "5y", "max"])

# Lista degli Asset che ti interessano
assets = {
    "NVIDIA (NVDA)": "NVDA",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Oro (Gold)": "GC=F",
    "S&P 500": "^GSPC"
}

# Creazione delle colonne per i grafici
col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period=periodo)
    
    # Scegliamo in quale colonna mettere il grafico
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        st.subheader(name)
        # Calcolo variazione percentuale
        chiusura = data['Close']
        variazione = ((chiusura.iloc[-1] - chiusura.iloc[0]) / chiusura.iloc[0]) * 100
        
        st.metric("Prezzo Attuale", f"{chiusura.iloc[-1]:.2f}", f"{variazione:.2f}%")
        st.line_chart(chiusura)

st.write("---")
st.caption("Dati aggiornati in tempo reale tramite Yahoo Finance")
