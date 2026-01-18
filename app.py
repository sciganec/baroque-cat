import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- КОНФІГУРАЦІЯ ТА МОБІЛЬНА АДАПТАЦІЯ ---
st.set_page_config(page_title="Marquis Kotsky", page_icon="🐈", layout="centered")

st.markdown("""
    <style>
    /* Основний фон та колір золота */
    .stApp { background-color: #0e1117; color: #d4af37; }
    
    /* Оптимізація тексту під iPhone */
    h1, h2, h3 { 
        color: #d4af37 !important; 
        font-family: 'Georgia', serif; 
        text-align: center;
        line-height: 1.2 !important;
    }
    .big-greeting { 
        font-size: 1.4rem !important; 
        font-weight: bold; 
        text-align: center; 
        padding: 10px;
        margin-bottom: 10px;
    }
    .status-box {
        font-size: 1.2rem;
        border: 1px solid #d4af37;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        background: #1c1c1c;
    }
    
    /* Кнопка на весь екран */
    div.stButton > button { 
        background-color: #d4af37; 
        color: #0e1117; 
        border: none; 
        border-radius: 25px; 
        width: 100%; 
        height: 3.5rem;
        font-size: 1.1rem !important;
        font-weight: bold;
    }
    
    /* Ховаємо зайві елементи Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Контейнер для зображення */
    .stImage > img {
        border-radius: 20px;
        border: 2px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВІТАЛЬНЕ ГАСЛО ТА ПОРТРЕТ ---
st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- АЛГОРИТМ ЧАСОВОЇ МАТРИЦІ (Random BC) ---
now = datetime.now()

def get_quarter_bits(value, max_val):
    # Вираховуємо четверть (0, 1, 2, 3)
    quarter = min(3, value // (max_val // 4 + 1))
    mapping = {0: "10", 1: "11", 2: "01", 3: "00"}
    return mapping.get(quarter, "00")

# b1b2 - година (0-23)
b1b2 = get_quarter_bits(now.hour, 24)
# b3b4 - день тижня (0-6)
b3b4 = get_quarter_bits(now.weekday(), 7)
# b5b6 - тиждень місяця (1-31 день)
b5b6 = get_quarter_bits(now.day - 1, 31)

auto_code = b1b2 + b3b4 + b5b6

# --- ВІЗУАЛІЗАЦІЯ ДЛЯ ТЕЛЕФОНУ ---
st.markdown(f'<div class="status-box">Ефірний стан: <b>{auto_code}</b></div>', unsafe_allow_html=True)

# Малюємо стан у рядок (без колонок, щоб не "пливло" на iPhone)
line_visual = ""
for bit in auto_code:
    line_visual += " — " if bit == '1' else " - - "
st.markdown(f"### {line_visual}")

st.markdown("<br>", unsafe_allow_html=True)

# --- ЛОГІКА МАРКІЗА КОЦЬКОГО ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("Послухати Маркіза (Vivaldi Play)"):
    if not api_key:
        st.error("Панство, ключ не знайдено!")
    else:
        # Музика (Весна Вівальді)
        vivaldi_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3"
        st.audio(vivaldi_url, format="audio/mp3", autoplay=True)
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        
        prompt = (
            f"Ти — Маркіз Коцький, витончений аристократ-кіт. "
            f"Звертайся 'Панство'. Опиши поточну життєву ситуацію для коду {auto_code}. "
            f"Не використовуй технічних слів. Говори про погоду в душі, шахи, чай та барокову гармонію."
        )
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8
        }

        with st.spinner("Маркіз Коцький готує відповідь..."):
            try:
                res = requests.post(url, headers=headers, json=data)
                if res.status_code == 200:
                    st.info(res.json()['choices'][0]['message']['content'])
                else:
                    st.error("Маркіз наразі зайнятий чаєм.")
            except:
                st.error("Збій у системі.")

# --- НИЖНЯ ПАНЕЛЬ (РУЧНИЙ ВВІД) ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("⚙️ Ручне налаштування та CSV"):
    manual_code = st.text_input("Введіть 6 цифр:", value=auto_code)
    df = pd.DataFrame([{"Code": manual_code, "Time": now.strftime("%Y-%m-%d %H:%M")}])
    st.code(df.to_csv(index=False))
    st.download_button("Завантажити CSV", df.to_csv(index=False), "report.csv")
