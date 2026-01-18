import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# --- КОНФІГУРАЦІЯ ТА СТИЛЬ ---
st.set_page_config(page_title="Marquis Kotsky", page_icon="🐈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    h1, h2, h3, .big-text { 
        color: #d4af37 !important; 
        font-family: 'Georgia', serif; 
        text-align: center;
    }
    .big-greeting { 
        font-size: 1.5rem !important; 
        font-weight: bold; 
        text-align: center; 
        margin: 15px 0;
        line-height: 1.3;
        padding: 0 10px;
    }
    /* Кнопка: велика та зручна для iPhone */
    div.stButton > button { 
        background-color: #d4af37; color: #0e1117; 
        border-radius: 30px; width: 100%; height: 4.5rem;
        font-size: 1.3rem !important; font-weight: bold;
        border: none;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    .status-box {
        font-size: 1.3rem; border: 2px solid #d4af37;
        padding: 12px; border-radius: 20px;
        background: #1c1c1c; margin: 10px 0;
        text-align: center;
    }
    /* Виправлення відступів для мобільних */
    .block-container { padding: 1rem 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ВІТАЛЬНЕ ГАСЛО ---
st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

# --- 2. ПОРТРЕТ МАРКІЗА (Локальний файл) ---
image_path = "marquis.png"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    # Резервне посилання, якщо файл ще не завантажено
    st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- 3. МУЗИЧНИЙ ПЛЕЄР ---
st.markdown("<center><small>🎻 Натисніть Play для супроводу Вівальді</small></center>", unsafe_allow_html=True)
vivaldi_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3"
st.audio(vivaldi_url, format="audio/mp3")

# --- 4. АЛГОРИТМ RANDOM BC ---
now = datetime.now()
def get_bits(val, limit):
    q = min(3, val // (max_val // 4 + 1)) if (max_val := limit) else 0
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

auto_code = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)

st.markdown(f'<div class="status-box">Ефірний стан: <b>{auto_code}</b></div>', unsafe_allow_html=True)

# --- 5. ДІЯ ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("ПОЧУТИ МАРКІЗА"):
    if not api_key:
        st.error("Панство, ключ не знайдено в Secrets!")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        prompt = (
            f"Ти Маркіз Коцький, кіт-аристократ з портрета. Звертайся 'Панство'. "
            f"Опиши поточну життєву ситуацію для коду {auto_code}. "
            f"Не використовуй технічних термінів. Пиши вишукано, про спокій, чай, шахи та бароко."
        )
        try:
            res = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8})
            if res.status_code == 200:
                st.info(res.json()['choices'][0]['message']['content'])
            else:
                st.error("Маркіз зараз відпочиває.")
        except:
            st.error("Зв'язок з покоями перервано.")

# --- 6. НИЖНЯ ЧАСТИНА (CSV) ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📊 Архівні дані"):
    df = pd.DataFrame([{"Code": auto_code, "DateTime": now.strftime("%Y-%m-%d %H:%M")}])
    st.text(df.to_csv(index=False))
    st.download_button("Завантажити CSV", df.to_csv(index=False), "marquis_report.csv")
