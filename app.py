import streamlit as st
import requests
import pandas as pd

# --- КОНФІГУРАЦІЯ РЕЗИДЕНЦІЇ ---
st.set_page_config(page_title="Baroque-Cat Residence", page_icon="🐈", layout="centered")

# --- СТИЛІЗАЦІЯ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; text-align: center; }
    div.stButton > button { 
        background-color: #1c1c1c; color: #d4af37; border: 2px solid #d4af37; 
        border-radius: 20px; width: 100%; height: 3em; font-weight: bold;
    }
    .stInfo { background-color: #1c1c1c; color: #d4af37; border: 1px solid #d4af37; border-radius: 10px; }
    /* Стилізація CSV вікна */
    code { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Резиденція Маркіза Baroque-Cat")

# --- СЕЙФ КЛЮЧІВ ---
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input("Groq API Key:", type="password")

# --- ВВІД ПАРАМЕТРІВ ---
user_code = st.text_input("Введіть 6-бітний код матриці:", value="110110")

# Перевірка вводу
if len(user_code) != 6 or not set(user_code).issubset({'0', '1'}):
    st.error("Помилка: код має складатися рівно з 6 бітів (0 або 1).")
    st.stop()

# --- МАТЕМАТИКА (UNICODE) ---
h11 = user_code.count('1')
h21 = user_code.count('0')
chi = 2 * (h11 - h21)

# Візуалізація гексаграми
st.markdown("### Структура Ефіру")
for bit in reversed(user_code):
    line = "【 ———————— 】" if bit == '1' else "【 ———    ——— 】"
    st.markdown(f"### {line}")

st.markdown(f"<center><b>h¹¹ = {h11} | h²¹ = {h21} | χ = {chi}</b></center>", unsafe_allow_html=True)

# --- ГОЛОВНА ДІЯ ---
if st.button("Запитати поради у Маркіза (Vivaldi Play)"):
    if not api_key:
        st.error("Ключ не знайдено! Перевірте Secrets або введіть його вручну.")
    else:
        # Музика (Весна Вівальді)
        vivaldi_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3"
        st.markdown(f'<audio src="{vivaldi_url}" autoplay loop></audio>', unsafe_allow_html=True)
        
        # Запит до Groq з оновленим зверненням
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        
        prompt = (
            f"Ти — Маркіз Baroque-Cat, витончений вчений-кіт. Твій стиль — розкішне бароко, мова пишна та метафорична. "
            f"Звертайся до користувача виключно як 'Панство'. Проаналізуй код {user_code} "
            f"(h11={h11}, h21={h21}, chi={chi}) як величну архітектурну та музичну композицію. "
            f"Твоя порада має стосуватися гармонії простору та душі."
        )
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.85
        }

        with st.spinner("Маркіз гострить золоте перо під звуки скрипок..."):
            try:
                res = requests.post(url, headers=headers, json=data)
                if res.status_code == 200:
                    answer = res.json()['choices'][0]['message']['content']
                    st.info(f"🐈 **Маркіз каже:**\n\n{answer}")
                else:
                    st.error(f"Помилка API ({res.status_code}): {res.text}")
            except Exception as e:
                st.error(f"Критичний збій зв'язку: {e}")

# --- ЕКСПОРТ CSV ---
st.markdown("---")
st.subheader("📊 Звіт у форматі CSV")
df = pd.DataFrame([{
    "Address": user_code, 
    "h1_1": h11, 
    "h2_1": h21, 
    "Euler_Chi": chi,
    "Formula": "χ = 2(h¹¹ - h²¹)"
}])

# Відображення CSV тексту
st.code(df.to_csv(index=False))

# Кнопка завантаження
st.download_button(
    label="📥 Завантажити CSV", 
    data=df.to_csv(index=False), 
    file_name=f"report_{user_code}.csv", 
    mime="text/csv"
)

st.markdown("<br><center><small>Резиденція Маркіза • 2026 • Панство, простір підвладний вашій думці</small></center>", unsafe_allow_html=True)
