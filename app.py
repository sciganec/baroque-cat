import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# --- КОНФІГУРАЦІЯ ТА МОБІЛЬНИЙ ДИЗАЙН ---
st.set_page_config(page_title="Marquis Kotsky", page_icon="🐈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    
    /* Виправлене та адаптоване гасло */
    .big-greeting { 
        font-size: 1.4rem !important; 
        font-weight: bold; 
        text-align: center; 
        padding: 40px 15px 20px 15px; /* Більший відступ зверху */
        line-height: 1.4;
        font-family: 'Georgia', serif;
        min-height: 100px;
    }

    /* Головна іконка-кнопка */
    div.stButton > button { 
        background-color: #d4af37; color: #0e1117; 
        border-radius: 50px; width: 100%; height: 5rem;
        font-size: 1.5rem !important; font-weight: bold;
        border: 2px solid #ffffff;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.5);
        transition: 0.3s;
    }
    div.stButton > button:active { transform: scale(0.98); }

    .small-code {
        font-size: 0.6rem; color: #2c2c2c;
        text-align: center; margin-top: 80px; font-family: monospace;
    }
    
    /* Оптимізація відступів контейнера */
    .block-container { padding-top: 0rem !important; }
    .stImage { margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ВІТАЛЬНЕ ГАСЛО ---
st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

# --- 2. ПОРТРЕТ МАРКІЗА ---
image_path = "marquis.png"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- 3. ТЕМПОРАЛЬНИЙ АЛГОРИТМ ---
now = datetime.now()
def get_bits(val, limit):
    q = min(3, val // (limit // 4 + 1))
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

current_hex = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)

# --- 4. ГОЛОВНА ДІЯ: ПРИЙНЯТИ АУДІЄНЦІЮ ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("⚜️ ПРИЙНЯТИ АУДІЄНЦІЮ"):
    # Активація музики (тихо)
    music_path = "vivaldi.mp3"
    if os.path.exists(music_path):
        with open(music_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    else:
        # Резерв
        st.audio("https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3", autoplay=True)

    if not api_key:
        st.error("Панство, сейф із ключами порожній.")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        prompt = (
            f"Ти — Маркіз Коцький, шляхетний кіт. Звертайся до користувача 'Панство'. "
            f"Проаналізуй стан буття для темпорального коду {current_hex}. "
            f"У ТЕКСТІ НЕ ПОВИННО БУТИ цифр, кодів чи згадок про І Цзин. "
            f"Говори вишукано про чай, шахи, затишок та барокову музику, що зараз лунає."
        )
        
        with st.spinner("Маркіз відкладає шахову фігуру..."):
            try:
                res = requests.post(url, headers=headers, json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8
                })
                if res.status_code == 200:
                    st.info(res.json()['choices'][0]['message']['content'])
                else:
                    st.error("Маркіз наразі не може відповісти.")
            except:
                st.error("Зв'язок із палацом перервано.")

# --- 5. ТЕХНІЧНИЙ НИЗ ---
st.markdown(f'<div class="small-code">matrix: {current_hex}</div>', unsafe_allow_html=True)
