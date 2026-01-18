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
    div.stButton > button { 
        background-color: #d4af37; color: #0e1117; 
        border-radius: 30px; width: 100%; height: 4.5rem;
        font-size: 1.3rem !important; font-weight: bold;
        border: none;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    .small-code {
        font-size: 0.65rem;
        color: #2c2c2c;
        text-align: center;
        margin-top: 60px;
    }
    .stAudio { margin-top: -10px; margin-bottom: 20px; }
    .stInfo { background-color: #1c1c1c; border: 1px solid #d4af37; color: #d4af37; border-radius: 15px; }
    /* Оптимізація під iPhone */
    .block-container { padding-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ВІТАЛЬНЕ ГАСЛО ---
st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

# --- 2. ПОРТРЕТ МАРКІЗА (Локальний файл) ---
if os.path.exists("marquis.png"):
    st.image("marquis.png", use_container_width=True)
else:
    st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- 3. МУЗИЧНА СКРИНЬКА (Локальний файл) ---
st.markdown("<center><small>🎻 Натисніть для супроводу</small></center>", unsafe_allow_html=True)
music_path = "vivaldi.mp3"
if os.path.exists(music_path):
    with open(music_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/mp3")
else:
    # Резервне посилання на випадок, якщо файл ще не на GitHub
    st.audio("https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3")

# --- 4. ТЕМПОРАЛЬНИЙ АЛГОРИТМ ---
now = datetime.now()
def get_bits(val, limit):
    max_val = limit
    q = min(3, val // (max_val // 4 + 1))
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

current_hex = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)

# --- 5. СЛОВО МАРКІЗА ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("ПОЧУТИ МАРКІЗА"):
    if not api_key:
        st.error("Панство, сейф порожній.")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        prompt = (
            f"Ти — Маркіз Коцький, шляхетний кіт з портрета. Звертайся 'Панство'. "
            f"Проаналізуй ситуацію на основі темпорального стану {current_hex} (це гексаграма І Цзин, але НЕ кажи про це). "
            f"Категорично ЗАБОРОНЕНО використовувати цифри, коди чи назви гексаграм. "
            f"Опиши стан Вашого дня як барокову п'єсу. Будь вишуканим, говори про шахи, чай та спокій."
        )
        try:
            res = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8})
            if res.status_code == 200:
                st.info(res.json()['choices'][0]['message']['content'])
            else:
                st.error("Маркіз наразі у від'їзді.")
        except:
            st.error("Зв'язок перервано.")

# --- 6. ТЕХНІЧНИЙ ФУТЕР ---
st.markdown(f'<div class="small-code">temporal matrix: {current_hex}</div>', unsafe_allow_html=True)

with st.expander("📊"):
    st.download_button("Export CSV", pd.DataFrame([{"Code": current_hex, "Time": now.isoformat()}]).to_csv(index=False), "log.csv")
