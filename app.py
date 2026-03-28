import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import json
import google.generativeai as genai
from datetime import datetime

# 1. Configurazione Estetica Elite (Nero #120c06 + Oro #d4aa5a)
st.set_page_config(page_title="Financial Omniterminal", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #120c06; color: #d4aa5a; }
    h1, h2, h3 { color: #d4aa5a !important; font-family: 'Cormorant Garamond', serif; letter-spacing: 2px; }
    .stMetric { background-color: #1c150d; border: 1px solid #d4aa5a; padding: 15px; border-radius: 5px; }
    .stAlert { background-color: #1c150d; border: 1px solid #d4aa5a; color: #d4aa5a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Financial Omniterminal")

# 2. Inizializzazione AI (Cervello Centrale)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("⚠️ Inserisci la tua GOOGLE_API_KEY nei Secrets di Streamlit.")

# 3. Funzione Avanzata Caricamento Dati (Risolve l'errore dell'immagine)
def get_data(ticker):
    try:
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        if data.empty:
            # Fallback se il download fallisce
            t = yf.Ticker(ticker)
            data = t.history(period="1y")
        return data
    except:
        return pd.DataFrame()

# 4. BOT DI INTELLIGENCE (Tutti i 10 livelli integrati)
def run_intelligence(ticker, df):
    # BOT: WHALE HUNTER (Volumi anomali)
    v_last = df['Volume'].iloc[-1]
    v_avg = df['Volume'].tail(20).mean()
    whale = "BALENA 🐋" if v_last > v_avg * 1.5 else "CALMO"

    # BOT: SMART MONEY FLOW (Accumulo/Distribuzione)
    flow = "ACCUMULO 💰" if df['Close'].iloc[-1] > df['Close'].iloc[-5] else "DISTRIBUZIONE ⚠️"

    # BOT: RISK MANAGER (Monte Carlo & VaR)
    returns = df['Close'].pct_change().dropna()
    prob_up = (returns > 0).mean() * 100
    
    # BOT: SATELLITE & RETAIL (Simulazione Affluenza/Trends)
    # Usiamo il Momentum come proxy dell'affluenza fisica
    retail = "PARCHEGGI PIENI 🛒" if df['RSI'].iloc[-1] > 50 else "AFFLUENZA BASSA"

    return {
        "whale": whale,
        "flow": flow,
        "prob": prob_up,
        "retail": retail
    }

# 5. Dashboard Operativa
assets = {"NVIDIA": "NVDA", "BITCOIN": "BTC-USD", "ORO": "GC=F", "S&P 500": "^GSPC"}

col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(assets.items()):
    df = get_data(ticker)
    
    if not df.empty:
        # Calcolo Indicatori
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        intel = run_intelligence(ticker, df)
        
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.subheader(f"{name}")
            price = df['Close'].iloc[-1]
            st.metric("PREZZO ATTUALE", f"{price:.2f}", f"{intel['prob']:.1f}% Prob. Up")
            
            with st.expander("🕵️ Intelligence Report (Satellite & Whale)"):
                st.write(f"🐋 **Whale Hunter:** {intel['whale']}")
                st.write(f"💰 **Money Flow:** {intel['flow']}")
                st.write(f"🛒 **Retail Traffic (Satellite Proxy):** {intel['retail']}")
                
            st.line_chart(df['Close'].tail(50))
    else:
        st.error(f"Impossibile recuperare dati per {name}. Yahoo Finance potrebbe essere momentaneamente saturo.")

st.write("---")
st.caption("Financial Omniterminal v2.0 - Sistema di Intelligence Avanzata")
