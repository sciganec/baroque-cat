import streamlit as st
import requests
import pandas as pd

# Конфігурація резиденції
st.set_page_config(page_title="Baroque-Cat Groq Lab", page_icon="🐈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    .stMetric { border: 1px solid #d4af37; padding: 15px; border-radius: 10px; background: #1c1c1c; }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; }
    div.stButton > button { background-color: #1c1c1c; color: #d4af37; border: 2px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐈 Baroque-Cat: Резиденція (Groq Edition)")
st.sidebar.header("📜 Ключі до Ефіру")
# Замість api_key = st.sidebar.text_input(...) використовуйте це:

if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("Введіть ключ, якщо сейф порожній", type="password")

# Решта коду залишається такою ж, але тепер api_key буде підхоплюватися автоматично.

user_code = st.text_input("Введіть 6-бітний код матриці:", value="101010")

# Математика (Unicode)
h11 = user_code.count('1')
h21 = user_code.count('0')
chi = 2 * (h11 - h21)

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("🏛️ Структура")
    for bit in reversed(user_code):
        line = "【 ———————— 】" if bit == '1' else "【 ———    ——— 】"
        st.markdown(f"### {line}")

with col2:
    st.subheader("📐 Параметри")
    st.markdown(f"**h¹¹ = {h11} | h²¹ = {h21} | χ = {chi}**")
    st.latex(r"\chi = 2(h^{1,1} - h^{2,1})")

if st.button("Запитати Маркіза (через Groq)"):
    if not api_key:
        st.warning("Пане Архітектор, вставте ключ gsk_...")
    else:
        # Протокол Groq (сумісний з OpenAI)
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile", # Найкраща модель Groq
            "messages": [
                {"role": "system", "content": "Ти Маркіз Baroque-Cat, мудрий вчений-кіт. Звертайся 'Пане Архітектор'."},
                {"role": "user", "content": f"Проаналізуй гексаграму {user_code} (χ={chi})."}
            ]
        }
        
        try:
            res = requests.post(url, headers=headers, json=data)
            if res.status_code == 200:
                st.info(res.json()['choices'][0]['message']['content'])
            else:
                st.error(f"Помилка Groq: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Збій: {e}")

# Вивід CSV
st.markdown("---")
df = pd.DataFrame([{"Address": user_code, "h1_1": h11, "h2_1": h21, "Chi": chi}])
st.text("Таблиця даних (CSV):")
st.code(df.to_csv(index=False))
st.download_button("📥 Завантажити CSV", df.to_csv(index=False), "report.csv", "text/csv")
