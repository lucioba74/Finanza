import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Dashboard Luciano", layout="wide")
st.title("📈 Analisi Mercati Luciano")

# Lista Asset
assets = {"NVIDIA": "NVDA", "Bitcoin": "BTC-USD", "Oro": "GC=F", "S&P 500": "^GSPC"}

st.sidebar.header("Impostazioni")
periodo = st.sidebar.selectbox("Periodo", ["1mo", "6mo", "1y", "5y"])

col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(assets.items()):
    try:
        data = yf.Ticker(ticker).history(period=periodo)
        if not data.empty:
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.subheader(name)
                # Calcolo sicuro del prezzo e variazione
                current_price = data['Close'].iloc[-1]
                st.metric(name, f"{current_price:.2f}")
                st.line_chart(data['Close'])
    except Exception as e:
        st.error(f"Errore su {name}: Mercato chiuso o dati non pronti.")

st.caption("Dati Yahoo Finance - Nota: I mercati sono chiusi nel weekend.")
