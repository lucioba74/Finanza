import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd

# 1. Configurazione Estetica Professionale
st.set_page_config(page_title="Luciano Finance Pro", layout="wide", initial_sidebar_state="expanded")

# CSS Personalizzato per un look moderno
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Luciano Financial Intelligence")

# 2. Configurazione IA con l'ultimo modello disponibile
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Errore API Key: Verificala nei Secrets di Streamlit.")

# 3. Funzione Recupero Dati Robusta (Gestisce i Weekend)
@st.cache_data(ttl=3600)
def get_data(ticker, period):
    try:
        df = yf.Ticker(ticker).history(period=period)
        if df.empty: return None
        return df
    except:
        return None

# 4. Sidebar Avanzata
with st.sidebar:
    st.header("⚙️ Pannello di Controllo")
    periodo = st.select_slider("Orizzonte Temporale", options=["1mo", "3mo", "6mo", "1y", "5y", "max"], value="1y")
    st.divider()
    user_question = st.text_area("🧠 Chiedi all'Analista AI", placeholder="Esempio: Nvidia è sopravvalutata?")
    st.caption("L'IA analizzerà il contesto macroeconomico del 2026.")

# 5. Dashboard Asset
assets = {"NVIDIA": "NVDA", "BITCOIN": "BTC-USD", "ORO": "GC=F", "S&P 500": "^GSPC"}
cols = st.columns(len(assets))

for i, (name, ticker) in enumerate(assets.items()):
    data = get_data(ticker, periodo)
    with cols[i]:
        if data is not None:
            price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else price
            delta = ((price - prev_price) / prev_price) * 100
            
            st.metric(label=name, value=f"{price:,.2f}", delta=f"{delta:.2f}%")
            st.line_chart(data['Close'], height=150)
        else:
            st.warning(f"Dati {name} non disp.")

# 6. Analisi IA Evoluta
if user_question:
    st.divider()
    with st.spinner("Analisi in corso..."):
        try:
            prompt = f"Analisi per Luciano: {user_question}. Considera il contesto dei mercati attuali e i rischi geopolitici."
            response = model.generate_content(prompt)
            st.markdown(f"### 🤖 Responso Intelligence\n{response.text}")
        except Exception as e:
            st.error("L'IA è momentaneamente occupata. Riprova tra un istante.")
