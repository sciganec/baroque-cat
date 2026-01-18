import streamlit as st
import requests
import pandas as pd

# --- КОНФІГУРАЦІЯ ПРОСТОРУ ---
st.set_page_config(
    page_title="Baroque-Cat Residence",
    page_icon="🐈",
    layout="centered"
)

# --- ЕСТЕТИКА ТА СТИЛЬ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    .stMetric { border: 1px solid #d4af37; padding: 15px; border-radius: 10px; background: #1c1c1c; }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; text-align: center; }
    div.stButton > button { 
        background-color: #1c1c1c; 
        color: #d4af37; 
        border: 2px solid #d4af37; 
        width: 100%;
        border-radius: 20px;
        transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #ffffff; color: #ffffff; }
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Baroque-Cat: Аналітична Резиденція")

# --- РОБОТА З КЛЮЧАМИ (СЕЙФ) ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.sidebar.warning("Ключ не знайдено в Secrets.")
    api_key = st.sidebar.text_input("Введіть Groq API Key вручну:", type="password")

# --- ВВІД ДАНИХ ---
user_code = st.text_input("Введіть 6-бітний код матриці (напр. 110110):", value="110110")

# Перевірка вводу
if len(user_code) != 6 or not set(user_code).issubset({'0', '1'}):
    st.error("Пане Архітектор, код має складатися рівно з 6 бітів (0 або 1).")
    st.stop()

# --- МАТЕМАТИЧНИЙ АПАРАТ (UNICODE) ---
h11 = user_code.count('1')
h21 = user_code.count('0')
chi = 2 * (h11 - h21)

# --- ВІЗУАЛІЗАЦІЯ ---
col_hex, col_math = st.columns([1, 1])

with col_hex:
    st.subheader("Гексаграма")
    # Малюємо гексаграму знизу вгору (традиційно)
    for bit in reversed(user_code):
        line = "【 ———————— 】" if bit == '1' else "【 ———    ——— 】"
        st.markdown(f"### {line}")

with col_math:
    st.subheader("Топологія")
    st.markdown(f"**Число Ходжа h¹¹:** `{h11}`")
    st.markdown(f"**Число Ходжа h²¹:** `{h21}`")
    st.markdown(f"**Ейлерова характеристика χ:** `{chi}`")
    st.markdown(f"**Формула:** χ = 2(h¹¹ - h²¹)")

st.markdown("---")

# --- ІНТЕЛЕКТ МАРКІЗА (КРАСНОМОВНА ВЕРСІЯ) ---
if st.button("Активувати роздуми Маркіза"):
    if not api_key:
        st.error("Пане Архітектор, сейф із ключами порожній!")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        prompt = (
            f"Ти — Маркіз Baroque-Cat, витончений вчений-кіт, майстер барокової риторики. "
            f"Твій стиль — інтелектуальний бенкет. Звертайся 'Вельмишановне Панство'. "
            f"Дай розлогий аналіз коду {user_code} (h11={h11}, h21={h21}, chi={chi}). "
            f"Порівняй числа Ходжа з елементами палацу, а Ейлерову характеристику — з душею простору."
        )
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.85, # Додаємо вогню красномовства
            "max_tokens": 1000
        }
        
        with st.spinner("Маркіз занурює перо у золоте чорнило..."):
            try:
                res = requests.post(url, headers=headers, json=data)
                if res.status_code == 200:
                    answer = res.json()['choices'][0]['message']['content']
                    st.markdown(f"### 🐾 Слово Маркіза:\n{answer}")
                else:
                    st.error(f"Ефір обурений! Код помилки: {res.status_code}")
            except Exception as e:
                st.error(f"Критичний збій у залах: {e}")

# --- ЗВІТНІСТЬ CSV ---
st.markdown("---")
data_row = {
    "Address": user_code,
    "h1_1": h11,
    "h2_1": h21,
    "Euler_Chi": chi,
    "Formula": "chi = 2 * (h11 - h21)"
}
df = pd.DataFrame([data_row])

st.subheader("📊 Табличні дані (CSV)")
csv_output = df.to_csv(index=False)
st.text(csv_output)

st.download_button(
    label="📥 Завантажити CSV звіт",
    data=csv_output,
    file_name=f"marquis_report_{user_code}.csv",
    mime="text/csv"
)

st.markdown("<br><center><small>Резиденція Маркіза • 2026 • Пане Архітектор, простір підвладний вам</small></center>", unsafe_allow_html=True)
