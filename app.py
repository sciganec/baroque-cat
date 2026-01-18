import streamlit as st
import requests
import pandas as pd

# Конфігурація: Пане Архітектор, це налаштування вашого візуального простору
st.set_page_config(page_title="Baroque-Cat Lab", page_icon="🐈", layout="wide")

# Юнікод формули та Бароковий стиль
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background-color: #1c1c1c; border: 1px solid #d4af37; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐈 Baroque-Cat: Аналітична Резиденція")
st.sidebar.header("📜 Налаштування Ефіру")
api_key = st.sidebar.text_input("Google API Key", type="password")

# Ввід коду
user_code = st.text_input("Введіть 6-бітний код:", value="110110")

# Математичний блок (Unicode)
h11 = user_code.count('1')
h21 = user_code.count('0')
chi = 2 * (h11 - h21)

# Візуалізація
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Гексаграма")
    visual = ""
    for bit in reversed(user_code):
        line = "【 —————— 】" if bit == '1' else "【 —  — 】"
        st.markdown(f"### {line}")
        visual += line + "\n"

with col2:
    st.subheader("Топологічний зріз")
    st.write(f"Параметри многовиду:")
    st.markdown(f"**h¹¹ = {h11}**")
    st.markdown(f"**h²¹ = {h21}**")
    st.markdown(f"**χ = {chi}**")
    
    if st.button("Запитати Маркіза"):
        if api_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = f"Ти Маркіз Baroque-Cat. Проаналізуй гексаграму {user_code} (χ={chi}). Звертайся 'Вельмишановний Архітекторе'."
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except:
                st.error("Зв'язок перервано.")

# Таблиця даних у CSV (згідно з вашим правилом)
st.markdown("---")
df = pd.DataFrame([{
    "Binary": user_code,
    "h1_1": h11,
    "h2_1": h21,
    "Euler_Chi": chi,
    "Status": "Coagula" if chi > 0 else "Solve"
}])

st.markdown("### Табличні дані (CSV)")
st.write(df.to_csv(index=False)) # Відображення як текст

st.download_button("📥 Вивантажити CSV", df.to_csv(index=False), "report.csv", "text/csv")
