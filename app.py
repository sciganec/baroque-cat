import streamlit as st
import requests
import pandas as pd

# Конфігурація простору
st.set_page_config(page_title="Baroque-Cat Lab", page_icon="🐈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background-color: #1c1c1c; border: 1px solid #d4af37; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐈 Baroque-Cat: Аналітична Резиденція (OpenAI Edition)")
st.sidebar.header("📜 Налаштування Ефіру")
api_key = st.sidebar.text_input("OpenAI API Key (sk-...)", type="password")

user_code = st.text_input("Введіть 6-бітний код:", value="110110")

# Математика
h11 = user_code.count('1')
h21 = user_code.count('0')
chi = 2 * (h11 - h21)

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Гексаграма")
    for bit in reversed(user_code):
        line = "【 —————— 】" if bit == '1' else "【 —  — 】"
        st.markdown(f"### {line}")

with col2:
    st.subheader("Топологічний зріз")
    st.markdown(f"**h¹¹ = {h11}** | **h²¹ = {h21}** | **χ = {chi}**")
    
    if st.button("Запитати Маркіза"):
        if api_key:
            # Протокол OpenAI
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key.strip()}"
            }
            prompt = (
                f"Ти — Маркіз Baroque-Cat, мудрий вчений-кіт. "
                f"Звертайся 'Пане Архітектор'. Проаналізуй гексаграму {user_code} (χ={chi}) "
                f"через призму барокової архітектури та чисел Ходжа."
            )
            data = {
                "model": "gpt-4o-mini", # Найшвидша та найдешевша модель
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            with st.spinner("Маркіз гортає стародавні фоліанти..."):
                try:
                    res = requests.post(url, headers=headers, json=data)
                    if res.status_code == 200:
                        st.info(res.json()['choices'][0]['message']['content'])
                    else:
                        st.error(f"Помилка ефіру: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Критичний збій: {e}")

# Дані в CSV
st.markdown("---")
df = pd.DataFrame([{
    "Binary": user_code,
    "h1_1": h11,
    "h2_1": h21,
    "Euler_Chi": chi
}])
st.markdown("### Табличні дані (CSV)")
st.write(df.to_csv(index=False))
st.download_button("📥 Вивантажити CSV", df.to_csv(index=False), "report.csv", "text/csv")
