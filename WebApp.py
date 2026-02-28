import streamlit as st
import datetime
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="RenovationsArt - Remonty i Wykończenia", 
    page_icon="🏗️",
    layout="wide"
)

# --- 2. DANE FIRMY I CENNIK ---
FIRMA = "RenovationsArt"
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
        "Prace dodatkowe (h)": 90, "Utylizacja gruzu (szt)": 250
    }
}

# --- 3. PASEK BOCZNY (NAPRAWIONY BŁĄD SKŁADNI) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4336/4336544.png", width=100)
st.sidebar.title("RenovationsArt") # Poprawione: dodano cudzysłów
st.sidebar.markdown("""
### 📞 Kontakt
**Instagram:** [@renovations.art](https://facebook.pl)  
**Telefon:** +48 601-403-157 
**E-mail:** renovationsartstg@gmail.com 

---
*Działamy na terenie Starogardu Gdańskiego i okolic 50km.*
""")

# --- 4. STRONA GŁÓWNA ---
st.title(f"🏠 {FIRMA} - System Ofertowy")
st.write("Witaj! Wybierz zakres prac, aby otrzymać błyskawiczną wycenę swojej inwestycji.")

# Sekcja atutów
c1, c2, c3 = st.columns(3)
c1.info("🛠️ **Profesjonalny sprzęt**")
c2.info("📅 **Terminowość**")
c3.info("📝 **Umowa i Gwarancja**")

st.divider()

# --- 5. FORMULARZ I KALKULATOR ---
klient = st.text_input("Nazwa Klienta / Inwestycji", placeholder="np. Remont mieszkania ul. Jasna")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

tabs = st.tabs(["🧱 Stan Surowy", "✨ Wykończenia", "🚰 Instalacje", "🔨 Wyburzenia"])

for i, kategoria in enumerate(CENNIK.keys()):
    with tabs[i]:
        for usluga, cena in CENNIK[kategoria].items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{usluga}**")
                st.caption(f"Cena: {cena} zł")
            with col2:
                # Unikalny klucz zapobiega błędom Streamlit
                ilosc = st.number_input("Ilość", min_value=0.0, step=1.0, key=f"input_{usluga}_{i}")
            with col3:
                wartosc = ilosc * cena
                st.write(f"Suma: **{wartosc:,.2f}** zł")
            
            if ilosc > 0:
                wybrane_uslugi.append({
                    "Usługa": usluga,
                    "Ilość": ilosc,
                    "Cena jedn.": f"{cena} zł",
                    "Wartość": wartosc
                })
                suma_netto += wartosc
        st.divider()

# --- 6. PODSUMOWANIE I POBIERANIE ---
if suma_netto > 0:
    st.sidebar.header("💰 Twoja Wycena")
    vat_rate = st.sidebar.radio("Stawka VAT", [8, 23], index=0)
    
    suma_vat = suma_netto * (vat_rate / 100)
    suma_brutto = suma_netto + suma_vat

    st.sidebar.write(f"Netto: {suma_netto:,.2f} zł")
    st.sidebar.write(f"VAT: {suma_vat:,.2f} zł")
    st.sidebar.subheader(f"Razem: {suma_brutto:,.2f} zł")

    if st.button("🚀 Generuj gotowy dokument"):
        if not klient:
            st.warning("Uzupełnij nazwę klienta na górze strony!")
        else:
            raport = f"WYCENA DLA: {klient}\nDATA: {data_dzis}\n" + "-"*30 + "\n"
            for item in wybrane_uslugi:
                raport += f"{item['Usługa']} | {item['Ilość']} x {item['Cena jedn.']} = {item['Wartość']:.2f} zł\n"
            raport += "-"*30 + f"\nDO ZAPŁATY BRUTTO: {suma_brutto:,.2f} zł"
            
            st.text_area("Podgląd PDF/TXT", raport, height=200)
            st.download_button("Pobierz plik tekstowy", raport, file_name=f"Wycena_{klient}.txt")
else:
    st.info("Dodaj ilości przy wybranych usługach, aby zobaczyć podsumowanie.")

