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
    }
    /* Кнопка: адаптована під iPhone */
    div.stButton > button { 
        background-color: #d4af37; color: #0e1117; 
        border-radius: 30px; width: 100%; height: 4rem;
        font-size: 1.2rem !important; font-weight: bold;
        border: none;
    }
    .small-code {
        font-size: 0.7rem;
        color: #444;
        text-align: center;
        margin-top: 50px;
    }
    .stInfo { background-color: #1c1c1c; border: 1px solid #d4af37; color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ВІТАЛЬНЕ ГАСЛО ---
st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

# --- 2. ПОРТРЕТ МАРКІЗА (marquis.png на GitHub) ---
image_path = "marquis.png"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    # Тимчасовий резерв, доки файл не завантажено
    st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- 3. МУЗИЧНИЙ СУПРОВІД ---
st.markdown("<center><small>🎻 Музична скринька: Антоніо Вівальді</small></center>", unsafe_allow_html=True)
vivaldi_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3"
st.audio(vivaldi_url, format="audio/mp3")

# --- 4. ТЕМПОРАЛЬНИЙ АЛГОРИТМ (І Цзин) ---
now = datetime.now()
def get_bits(val, limit):
    q = min(3, val // (limit // 4 + 1))
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

# Код генерується непомітно для користувача
current_hexagram_code = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)

# --- 5. ДІЯ МАРКІЗА ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("ПОЧУТИ МАРКІЗА"):
    if not api_key:
        st.error("Панство, ключ відсутній у сейфі.")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        
        # Маркіз знає код, але не називає його. Він аналізує його як гексаграму І Цзин.
        prompt = (
            f"Ти — Маркіз Коцький, витончений аристократ. Звертайся до користувача виключно українським словом 'Панство'. "
            f"Проаналізуй поточний момент часу, який відповідає гексаграмі І Цзин з бінарним значенням {current_hexagram_code}. "
            f"У ТЕКСТІ ВІДПОВІДІ КАТЕГОРИЧНО ЗАБОРОНЕНО згадувати цифри, коди, біти, гексаграми чи І Цзин. "
            f"Опиши стан буття, дай мудру пораду щодо чаювання, шахів чи споглядання саду. "
            f"Твоя мова має бути пишною, бароковою та заспокійливою."
        )
        
        try:
            res = requests.post(url, headers=headers, json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8
            })
            if res.status_code == 200:
                st.info(res.json()['choices'][0]['message']['content'])
            else:
                st.error("Маркіз наразі не може прийняти Панство.")
        except:
            st.error("Зв'язок із палацом перервано.")

# --- 6. ТЕХНІЧНИЙ НИЗ (ДРІБНИЙ ШРИФТ) ---
st.markdown(f'<div class="small-code">temporal matrix state: {current_hexagram_code}</div>', unsafe_allow_html=True)

with st.expander("📊"):
    st.download_button("Export CSV", pd.DataFrame([{"Code": current_hexagram_code}]).to_csv(index=False), "report.csv")
