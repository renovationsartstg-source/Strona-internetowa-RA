import streamlit as st
import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="RenovationsArt - Remonty i Wykończenia", 
    page_icon="🏗️",
    layout="wide"
)

# --- FUNKCJA WYSYŁKI EMAIL ---
def send_email(klient_name, tresc_oferty):
    sender_email = "renovationsartstg@gmail.com"
    receiver_email = "renovationsartstg@gmail.com"
    # TWOJE HASLO APLIKACJI ZOSTALO WKLEJONE PONIZEJ
    password = "tkfywgirajsedodx" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Nowa wycena: {klient_name}"

    msg.attach(MIMEText(tresc_oferty, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #ff8c00;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DANE FIRMY I CENNIK ---
FIRMA = "RenovationsArt"
SOCIAL = "@renovations.art"
CENNIK = {
    "Stan Surowy": {
        "Wykop pod fundamenty (m3)": 75, "Wylanie ław (m2)": 140,
        "Murowanie nośne (m2)": 125, "Murowanie działowe (m2)": 62,
        "Wykonanie stropu (m2)": 107, "Więźba dachowa (m2)": 77,
        "Pokrycie dachu (m2)": 100
    },
    "Wykończenia": {
        "Tynkowanie maszynowe (m2)": 46, "Gładź gipsowa (m2)": 52,
        "Malowanie 2x (m2)": 28, "Sufit podwieszany G-K (m2)": 135,
        "Płytki standard (m2)": 135, "Gres wielki format (m2)": 210,
        "Panele podłogowe (m2)": 62, "Montaż drzwi wew. (szt)": 525
    },
    "Instalacje": {
        "Punkt elektryczny (szt)": 110, "Punkt wod-kan (szt)": 175,
        "Ogrzewanie podłogowe (m2)": 307, "Biały montaż WC/Umyw. (szt)": 200,
        "Biały montaż Wanna/Kab. (szt)": 500
    },
    "Wyburzenia i Inne": {
        "Skuwanie płytek (m2)": 55, "Wyburzanie ścian (m2)": 140,
        "Prace dodatkowe (h)": 90
