import streamlit as st
import yfinance as yf
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="Luciano Finance AI", layout="wide")
st.title("🚀 Dashboard Finanziaria con IA")

# Recupero Chiave API dai Secrets di Streamlit
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Configura la GOOGLE_API_KEY nei Secrets di Streamlit!")

# Sidebar - Impostazioni
st.sidebar.header("Analisi Asset")
periodo = st.sidebar.selectbox("Periodo", ["1mo", "6mo", "1y", "5y"])
user_question = st.sidebar.text_input("Chiedi all'IA (es: Analizza Nvidia)")

# Visualizzazione Asset
assets = {"NVIDIA": "NVDA", "Bitcoin": "BTC-USD", "Oro": "GC=F", "S&P 500": "^GSPC"}
col1, col2 = st.columns(2)

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period=periodo)
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        if not data.empty:
            st.subheader(f"{name}")
            st.metric("Prezzo", f"{data['Close'].iloc[-1]:.2f}")
            st.line_chart(data['Close'])

# Sezione IA
if user_question:
    st.write("---")
    st.subheader("🤖 Responso dell'Intelligenza Artificiale")
    with st.spinner('L\'IA sta analizzando...'):
        response = model.generate_content(f"Agisci come esperto finanziario. {user_question}")
        st.info(response.text)
