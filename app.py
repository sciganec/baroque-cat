import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# --- ТЕХНІЧНИЙ РЕЄСТР ЮНІКОДУ ТА ВЕРТИКАЛЕЙ ---
UNICODE_MAP = {
    "111111": ("䷀", "{AAAAAA}"), "000000": ("䷁", "{VVVVVV}"), "100010": ("䷂", "{AVVVAV}"),
    "010001": ("䷃", "{VAVVVA}"), "111010": ("䷄", "{AAAVAV}"), "010111": ("䷅", "{VAVAAA}"),
    "010000": ("䷆", "{VAVVVV}"), "000010": ("䷇", "{VVVVAV}"), "111011": ("䷈", "{AAAVAA}"),
    "110111": ("䷉", "{AAVAAA}"), "111000": ("䷊", "{AAAVVV}"), "000111": ("䷋", "{VVVAAA}"),
    "101111": ("䷌", "{AVAAAA}"), "111101": ("䷍", "{AAAAAV}"), "001000": ("䷎", "{VVAVVV}"),
    "000100": ("䷏", "{VVVAVV}"), "100110": ("䷐", "{AVVAAV}"), "011001": ("䷑", "{VAAVVA}"),
    "110000": ("䷒", "{AAVVVV}"), "000011": ("䷓", "{VVVVAA}"), "100101": ("䷔", "{AVVAVA}"),
    "101001": ("䷕", "{AVAVVA}"), "000001": ("䷖", "{VVVVVA}"), "100000": ("䷗", "{AVVVVV}"),
    "100111": ("䷘", "{AVVAAA}"), "111001": ("䷙", "{AAAVVA}"), "100001": ("䷚", "{AVVVVA}"),
    "011110": ("䷛", "{VAAAAV}"), "010010": ("䷜", "{VAVVAV}"), "101101": ("䷝", "{AVAAAA}"),
    "001110": ("䷞", "{VVAAAV}"), "011100": ("䷟", "{VAAAVV}"), "001111": ("䷠", "{VVAAAA}"),
    "111100": ("䷡", "{AAAAVV}"), "000101": ("䷢", "{VVVAVA}"), "101000": ("䷣", "{AVAVVV}"),
    "101011": ("䷤", "{AVAVAA}"), "110101": ("䷥", "{AAVAVA}"), "001010": ("䷦", "{VVAVAV}"),
    "010100": ("䷧", "{VAVAVV}"), "110001": ("䷨", "{AAVVVA}"), "100011": ("䷩", "{AVVVAA}"),
    "111110": ("䷪", "{AAAAAV}"), "011111": ("䷫", "{VAAAAA}"), "000110": ("䷬", "{VVVAAV}"),
    "011000": ("䷭", "{VAAVVV}"), "010110": ("䷮", "{VAVAAV}"), "011010": ("䷯", "{VAAVAV}"),
    "101110": ("䷰", "{AVAAVV}"), "011101": ("䷱", "{VAAAVA}"), "100100": ("䷲", "{AVVAVV}"),
    "001001": ("䷳", "{VVAVVA}"), "001011": ("䷴", "{VVAVAA}"), "110100": ("䷵", "{AAVAVV}"),
    "101100": ("䷶", "{AVAAVV}"), "001101": ("䷷", "{VVAAVA}"), "011011": ("䷸", "{VAAVAA}"),
    "110110": ("䷹", "{AAVAAV}"), "010011": ("䷺", "{VAVVAA}"), "110010": ("䷻", "{AAVVAV}"),
    "110011": ("䷼", "{AAVVAA}"), "001100": ("䷽", "{VVAAVV}"), "101010": ("䷾", "{AVAVAV}"),
    "010101": ("䷿", "{VAVAVA}")
}

# --- КОНФІГУРАЦІЯ ТА СТИЛЬ ---
st.set_page_config(page_title="Marquis Kotsky", page_icon="🐈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    .big-greeting { font-size: 1.4rem; text-align: center; padding: 40px 10px; font-family: 'Georgia', serif; }
    .hex-symbol { font-size: 8rem; text-align: center; color: #d4af37; margin: -10px 0; text-shadow: 0px 0px 15px #d4af3799; }
    div.stButton > button { 
        background-color: #d4af37; color: #0e1117; border-radius: 50px; 
        width: 100%; height: 4.5rem; font-size: 1.4rem !important; font-weight: bold; border: 2px solid #fff;
    }
    .stInfo { background-color: #1c1c1c; border: 1px solid #d4af37; color: #d4af37; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-greeting">Вітаємо у Резиденції, пане Архітектор!</div>', unsafe_allow_html=True)

if os.path.exists("marquis.png"):
    st.image("marquis.png", use_container_width=True)

# --- АЛГОРИТМ ---
now = datetime.now()
def get_bits(val, limit):
    q = min(3, val // (limit // 4 + 1))
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

current_hex = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)
hex_char, vector = UNICODE_MAP.get(current_hex, ("䷀", "{AAAAAA}"))

if st.button("⚜️ ПРИЙНЯТИ АУДІЄНЦІЮ"):
    if os.path.exists("vivaldi.mp3"):
        with open("vivaldi.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
    
    st.markdown(f'<div class="hex-symbol">{hex_char}</div>', unsafe_allow_html=True)
    
    api_key = st.secrets.get("GROQ_API_KEY")
    if api_key:
        prompt = (f"Ти Маркіз Коцький. Звертайся 'Панство'. Опиши стан {hex_char} (вектор {vector}) "
                  "бароковою мовою під музику Вівальді. Без цифр.")
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                headers={"Authorization": f"Bearer {api_key}"},
                                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
            st.info(res.json()['choices'][0]['message']['content'])
        except:
            st.error("Аудієнцію перервано.")

st.markdown(f'<center><small style="color:#2c2c2c">matrix: {current_hex} | vector: {vector}</small></center>', unsafe_allow_html=True)
