import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# --- ТЕХНІЧНИЙ РЕЄСТР ЮНІКОДУ ТА ВЕРТИКАЛЕЙ ---
# Фундамент розрахунків базується на станах, описаних у манускриптах 
UNICODE_MAP = {
    "000000": ("䷁", "{VVVVVV; IT IT IT; N N N}"),
    "000001": ("䷖", "{VVVVVA; IT IT YU; N N W}"),
    "000010": ("䷇", "{VVVVAV; IT IT ME; NNE}"),
    "000011": ("䷳", "{VVVVAA; IT IT WE; N N S}"),
    "000100": ("䷏", "{VVVAVV; IT YU IT; N W N}"),
    "000101": ("䷢", "{VVVAVA; IT YU YU; N W W}"),
    "000110": ("䷬", "{VVVAAV; IT YU ME; N WE}"),
    "000111": ("䷋", "{VVVAAA; IT YU WE; N W S}"),
    "001000": ("䷎", "{VVAVVV; IT ME IT; NEN}"),
    "001001": ("䷳", "{VVAVVA; IT ME YU; NEW}"),
    "001010": ("䷦", "{VVAVAV; IT ME ME; NE E}"),
    "001011": ("䷴", "{VVAVAA; IT ME WE; NE S}"),
    "001100": ("䷽", "{VVAAVV; IT WE IT; N S N}"),
    "001101": ("䷵", "{VVAAVA; IT WE YU; N S W}"),
    "001110": ("䷞", "{VVAAAV; IT WE ME; N SE}"),
    "001111": ("䷠", "{VVAAAA; IT WE WE; N S S}"),
    "010000": ("䷆", "{VAVVVV; YU IT IT; W N N}"),
    "010001": ("䷃", "{VAVVVA; YU IT YU; W N W}"),
    "010010": ("䷜", "{VAVVAV; YU IT ME; W N E}"),
    "010011": ("䷺", "{VAVVAA; YU IT WE; W N S}"),
    "010100": ("䷧", "{VAVAVV; YU YU IT; W W N}"),
    "010101": ("䷿", "{VAVAVA; YU YU YU; W W W}"),
    "010110": ("䷮", "{VAVAAV; YU YU ME; W W E}"),
    "010111": ("䷅", "{VAVAAA; YU YU WE; W W S}"),
    "011000": ("䷭", "{VAAVVV; YU ME IT; WEN}"),
    "011001": ("䷑", "{VAAVVA; YU ME YU; WE W}"),
    "011010": ("䷯", "{VAAVAV; YU ME ME; WE E}"),
    "011011": ("䷸", "{VAAVAA; YU ME WE; WE S}"),
    "011100": ("䷟", "{VAAAVV; YU WE IT; W S N}"),
    "011101": ("䷱", "{VAAAVA; YU WE YU; W S W}"),
    "011110": ("䷛", "{VAAAAV; YU WE ME; W S E}"),
    "011111": ("䷫", "{VAAAAA; YU WE WE; W S S}"),
    "100000": ("䷗", "{AVVVVV; ME IT IT; EN N}"),
    "100001": ("䷚", "{AVVVVA; ME IT YU; EN W}"),
    "100010": ("䷂", "{AVVVAV; ME IT ME; EN E}"),
    "100011": ("䷩", "{AVVVAA; ME IT WE; EN S}"),
    "100100": ("䷲", "{AVVAVV; ME YU IT; E W N}"),
    "100101": ("䷔", "{AVVAVA; ME YU YU; E W W}"),
    "100110": ("䷐", "{AVVAAV; ME YU ME; E W E}"),
    "100111": ("䷘", "{AVVAAA; ME YU WE; E W S}"),
    "101000": ("䷣", "{AVAVVV; ME ME IT; E EN}"),
    "101001": ("䷕", "{AVAVVA; ME ME YU; E E W}"),
    "101010": ("䷾", "{AVAVAV; ME ME ME; E E E}"),
    "101011": ("䷤", "{AVAVAA; ME ME WE; E E S}"),
    "101100": ("䷶", "{AVAAVV; ME WE IT; E S N}"),
    "101101": ("䷝", "{AVAAVA; ME WE YU; E S W}"),
    "101110": ("䷰", "{AVAAAV; ME WE ME; E SE}"),
    "101111": ("䷌", "{AVAAAA; ME WE WE; E S S}"),
    "110000": ("䷒", "{AAVVVV; WE IT IT; S N N}"),
    "110001": ("䷨", "{AAVVVA; WE IT YU; S N W}"),
    "110010": ("䷻", "{AAVVAV; WE IT ME; S NE}"),
    "110011": ("䷼", "{AAVVAA; WE IT WE; S N S}"),
    "110100": ("䷵", "{AAVAVV; WE YU IT; S W N}"),
    "110101": ("䷄", "{AAVAVA; WE YU YU; S W W}"),
    "110110": ("䷹", "{AAVAAV; WE YU ME; S W E}"),
    "110111": ("䷉", "{AAVAAA; WE YU WE; S W S}"),
    "111000": ("䷊", "{AAAVVV; WE ME IT; SEN}"),
    "111001": ("䷙", "{AAAVVA; WE ME YU; SE W}"),
    "111010": ("䷄", "{AAAVAV; WE ME ME; SEE}"),
    "111011": ("䷈", "{AAAVAA; WE ME WE; SE S}"),
    "111100": ("䷡", "{AAAAVV; WE WE IT; S S N}"),
    "111101": ("䷍", "{AAAAVA; WE WE YU; S S W}"),
    "111110": ("䷪", "{AAAAAV; WE WE ME; S SE}"),
    "111111": ("䷀", "{AAAAAA; WE WE WE; S S S}")
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

st.markdown('<div class="big-greeting">Вельмишановне Панство, вельми радий вітати Вас у резиденціях маркіза Коцького!</div>', unsafe_allow_html=True)

if os.path.exists("marquis.png"):
    st.image("marquis.png", use_container_width=True)

# --- АЛГОРИТМ ---
now = datetime.now()
def get_bits(val, limit):
    q = min(3, val // (limit // 4 + 1))
    return {0: "10", 1: "11", 2: "01", 3: "00"}.get(q, "00")

current_hex_bits = get_bits(now.hour, 24) + get_bits(now.weekday(), 7) + get_bits(now.day - 1, 31)
hex_char, vector = UNICODE_MAP.get(current_hex_bits, ("䷀", "{AAAAAA; WE WE WE; S S S}"))

if st.button("⚜️ ПРИЙНЯТИ АУДІЄНЦІЮ"):
    if os.path.exists("vivaldi.mp3"):
        with open("vivaldi.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
    
    st.markdown(f'<div class="hex-symbol">{hex_char}</div>', unsafe_allow_html=True)
    
    api_key = st.secrets.get("GROQ_API_KEY")
    if api_key:
        # Промпт вимагає базувати відповідь на стані символу, але забороняє вживати слово "гексаграма"
        prompt = (f"Ти Маркіз Коцький. Звертайся 'шановне Панство'. "
                  f"Твоя відповідь має повністю базуватися на філософському стані цього символу {hex_char} "
                  f"та його векторному вимірі {vector}, проте ти МАЄШ УНИКАТИ слова 'гексаграма'. "
                  f"Говори вишуканою бароковою мовою, натхненною Вівальді. Опиши плин часу та дух моменту. Без цифр.")
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                headers={"Authorization": f"Bearer {api_key}"},
                                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
            st.info(res.json()['choices'][0]['message']['content'])
        except:
            st.error("Аудієнцію перервано.")

st.markdown(f'<center><small style="color:#2c2c2c">matrix: {current_hex_bits} | vector: {vector}</small></center>', unsafe_allow_html=True)
