import streamlit as st
import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="RenovationsArt - Kalkulator", 
    page_icon="🏗️",
    layout="wide"
)

# --- FUNKCJA WYSYŁKI EMAIL ---
def send_email(klient_name, tresc_oferty):
    # DANE KONFIGURACYJNE (Wpisz swoje dane)
    sender_email = "TWOJ_EMAIL@gmail.com"
    receiver_email = "renovationsartstg@gmail.com"
    password = "TWOJE_HASLO_APLIKACJI" # W Gmailu musisz wygenerować "Hasło do aplikacji"

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
    except Exception as e:
        print(f"Błąd wysyłki: {e}")
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
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DANE I CENNIK ---
FIRMA = "RenovationsArt"
SOCIAL = "@renovations.art"
CENNIK = {
    "Stan Surowy": {
        "Wykop pod fundamenty (m3)": 75, "Wylanie ław (m2)": 140,
        "Murowanie nośne (m2)": 125, "Murowanie działowe (m2)": 62
    },
    "Wykończenia": {
        "Tynkowanie maszynowe (m2)": 46, "Gładź gipsowa (m2)": 52,
        "Malowanie 2x (m2)": 28, "Płytki standard (m2)": 135
    },
    "Instalacje": {
        "Punkt elektryczny (szt)": 110, "Punkt wod-kan (szt)": 175
    },
    "Wyburzenia": {
        "Skuwanie płytek (m2)": 55, "Wyburzanie ścian (m2)": 140
    }
}

# --- 3. PASEK BOCZNY ---
st.sidebar.title(SOCIAL)
st.sidebar.markdown(f"""
### 📞 Kontakt
**Telefon:** +48 601-403-157  
**E-mail:** renovationsartstg@gmail.com  
""")

# --- 4. STRONA GŁÓWNA ---
st.title(f"🏠 {FIRMA} - System Ofertowy")
klient = st.text_input("Nazwa Klienta / Inwestycji", placeholder="np. Jan Kowalski, Starogard")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

tabs = st.tabs(list(CENNIK.keys()))
for i, kategoria in enumerate(CENNIK.keys()):
    with tabs[i]:
        for usluga, cena in CENNIK[kategoria].items():
            c1, c2, c3 = st.columns([3, 1, 1])
            ilosc = c2.number_input("Ilość", min_value=0.0, step=1.0, key=f"{usluga}_{i}")
            wartosc = ilosc * cena
            c1.write(f"**{usluga}** ({cena} zł/j)")
            c3.write(f"{wartosc:,.2f} zł")
            if ilosc > 0:
                wybrane_uslugi.append({"Usługa": usluga, "Ilość": ilosc, "Wartość": wartosc})
                suma_netto += wartosc

# --- 5. PODSUMOWANIE I WYSYŁKA ---
if suma_netto > 0:
    st.divider()
    vat_rate = st.selectbox("Stawka VAT", [8, 23])
    suma_brutto = suma_netto * (1 + vat_rate/100)
    
    st.metric("Suma do zapłaty (Brutto)", f"{suma_brutto:,.2f} zł")

    if st.button("📄 Generuj ofertę i wyślij powiadomienie"):
        if not klient:
            st.error("Wpisz nazwę klienta!")
        else:
            # Tworzenie treści oferty
            raport = f"OFERTA DLA: {klient}\nData: {data_dzis}\n" + "="*30 + "\n"
            for item in wybrane_uslugi:
                raport += f"- {item['Usługa']}: {item['Ilość']} = {item['Wartość']:.2f} zł\n"
            raport += "="*30 + f"\nRAZEM BRUTTO: {suma_brutto:,.2f} zł"

            # WYSYŁKA EMAIL
            sukces = send_email(klient, raport)
            
            if sukces:
                st.success("✅ Oferta wygenerowana i wysłana na Twój e-mail!")
            else:
                st.warning("⚠️ Oferta wygenerowana, ale wystąpił błąd wysyłki e-mail (sprawdź konfigurację hasła).")
            
            st.text_area("Podgląd oferty:", raport, height=200)
            st.download_button("📥 Pobierz plik .txt", raport, file_name=f"Oferta_{klient}.txt")

# --- 6. PORTFOLIO ---
st.divider()
st.header("📸 Nasza Realizacja")
st.image("https://scontent.fktw4-1.fna.fbcdn.net/v/t39.30808-6/475454641_122127453680768335_3612053243163351315_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=127cfc&_nc_ohc=G6YV3TzX_S8Q7kNvgG_V7p6&_nc_zt=23&_nc_ht=scontent.fktw4-1.fna.fbcdn.net&oh=00_AYB_your_oh_here&oe=67C8D84D", use_container_width=True)
