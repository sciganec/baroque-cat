import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import calendar

# --- КОНФІГУРАЦІЯ ТА СТИЛЬ ---
st.set_page_config(page_title="Baroque-Cat Residence", page_icon="🐈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #d4af37; }
    h1, h2, h3, p { color: #d4af37 !important; font-family: 'Georgia', serif; text-align: center; }
    div.stButton > button { 
        background-color: #1c1c1c; color: #d4af37; border: 2px solid #d4af37; 
        border-radius: 20px; width: 100%; font-weight: bold;
    }
    .stInfo { background-color: #1c1c1c; border: 1px solid #d4af37; border-radius: 10px; }
    /* Оптимізація під iPhone */
    @media (max-width: 640px) {
        h1 { font-size: 1.5rem !important; }
        .block-container { padding: 1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВІТАЛЬНЕ СЛОВО ТА ПОРТРЕТ ---
st.markdown("### Вельмишановне Панство, я вельми радий вітати Вас у моїх резиденціях!")
st.image("https://r2.erweima.ai/i/EE753FD2-1D8C-4D0E-868C-7A77851A0534.PNG", use_container_width=True)

# --- АЛГОРИТМ ЧАСОВОЇ МАТРИЦІ (Random BC) ---
now = datetime.now()

def get_quarter_bits(value, max_val):
    quarter = (value - 1) // (max_val // 4 + 1)
    mapping = {0: "10", 1: "11", 2: "01", 3: "00"}
    return mapping.get(quarter, "00")

# b1b2 - година дня (24 години)
b1b2 = get_quarter_bits(now.hour + 1, 24)
# b3b4 - день тижня (7 днів)
b3b4 = get_quarter_bits(now.weekday() + 1, 7)
# b5b6 - тиждень місяця (прибл. 31 день)
b5b6 = get_quarter_bits(now.day, 31)

auto_code = b1b2 + b3b4 + b5b6

# --- ВІЗУАЛІЗАЦІЯ СИТУАЦІЇ ---
st.markdown(f"**Поточний ефірний стан:** `{auto_code}`")

# Вивід "малюнку" ситуації
cols = st.columns(6)
for i, bit in enumerate(auto_code):
    line = "—" if bit == '1' else "- -"
    cols[i].markdown(f"**{line}**")

# --- ЛОГІКА МАРКІЗА ---
api_key = st.secrets.get("GROQ_API_KEY")

if st.button("Послухати Маркіза під Вівальді"):
    if not api_key:
        st.error("Панство, ключ не знайдено!")
    else:
        # Музика
        vivaldi_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Vivaldi_Spring_mvt_1_Allegro_-_John_Harrison_with_the_Wichita_State_University_Chamber_Players.mp3"
        st.audio(vivaldi_url, format="audio/mp3", autoplay=True)
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key.strip()}", "Content-Type": "application/json"}
        
        prompt = (
            f"Ти — Маркіз Baroque-Cat на портреті (кіт у вбранні 17 ст., з чаєм та шахами). "
            f"Твій стиль — пишне бароко. Звертайся 'Панство'. "
            f"Опиши поточну життєву ситуацію для коду {auto_code}. "
            f"НЕ згадуй слова 'гексаграма', 'бінарний код' або 'многовиди'. "
            f"Говори про гармонію, хід часу, світські події та стан душі."
        )
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8
        }

        with st.spinner("Маркіз відставляє чашку чаю..."):
            try:
                res = requests.post(url, headers=headers, json=data)
                if res.status_code == 200:
                    st.info(res.json()['choices'][0]['message']['content'])
                else:
                    st.error("Ефір тимчасово заблоковано.")
            except:
                st.error("Збій у покоях.")

# --- ТЕХНІЧНИЙ ПІДВАЛ (ВВІД ВНИЗУ) ---
st.markdown("---")
with st.expander("⚙️ Ручне коригування матриці (для Панства)"):
    manual_code = st.text_input("Ввести значення вручну:", value=auto_code)
    h11 = manual_code.count('1')
    h21 = manual_code.count('0')
    chi = 2 * (h11 - h21)
    
    # CSV вивід
    df = pd.DataFrame([{"Address": manual_code, "h1_1": h11, "h2_1": h21, "Chi": chi}])
    st.code(df.to_csv(index=False))
    st.download_button("📥 Завантажити CSV", df.to_csv(index=False), "report.csv")
