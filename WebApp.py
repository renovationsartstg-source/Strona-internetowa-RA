import streamlit as st
import datetime
import pandas as pd

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="RenovationsArt - Remonty i Wykończenia", 
    page_icon="🏗️",
    layout="wide"
)

# --- STYLE CSS (KOLORYSTYKA BUDOWLANA) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #ff8c00;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
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
        "Prace dodatkowe (h)": 90, "Utylizacja gruzu (szt)": 250
    }
}

# --- 3. PASEK BOCZNY ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3523/3523887.png", width=100)
st.sidebar.title(SOCIAL)
st.sidebar.markdown(f"""
### 📞 Kontakt
**Telefon:** +48 601-403-157  
**E-mail:** renovationsartstg@gmail.com  
**Lokalizacja:** Starogard Gdański i okolice (50km)  

---
*Gwarantujemy terminowość i czystość na budowie.*
""")

# --- 4. STRONA GŁÓWNA ---
st.title(f"🏠 {FIRMA} - Solidne Remonty i Budowa")
st.write("Witamy! Specjalizujemy się w kompleksowych wykończeniach wnętrz oraz stanach surowych. Skorzystaj z kalkulatora poniżej, aby otrzymać wstępną wycenę.")

col_a, col_b, col_c = st.columns(3)
col_a.success("✅ **Bezpyłowe gładzie**")
col_b.success("✅ **Gwarancja 24 m-ce**")
col_c.success("✅ **Czystość po pracy**")

st.divider()

# --- 5. KALKULATOR ---
st.header("🧮 Kalkulator darmowej wyceny")
klient = st.text_input("Nazwa Klienta / Adres inwestycji", placeholder="np. Mieszkanie ul. Polna")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

tabs = st.tabs(["🧱 Stan Surowy", "✨ Wykończenia", "🚰 Instalacje", "🔨 Wyburzenia"])

for i, kategoria in enumerate(CENNIK.keys()):
    with tabs[i]:
        for usluga, cena in CENNIK[kategoria].items():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{usluga}**")
                st.caption(f"Cena: {cena} zł/jedn.")
            with c2:
                ilosc = st.number_input("Ilość", min_value=0.0, step=1.0, key=f"{usluga}_{i}")
            with c3:
                wartosc = ilosc * cena
                st.write(f"Wartość: **{wartosc:,.2f} zł**")
            
            if ilosc > 0:
                wybrane_uslugi.append({
                    "Kategoria": kategoria,
                    "Usługa": usluga,
                    "Ilość": ilosc,
                    "Cena jedn. (zł)": cena,
                    "Wartość (zł)": wartosc
                })
                suma_netto += wartosc
        st.divider()

# --- 6. PODSUMOWANIE I GENEROWANIE RAPORTU ---
if suma_netto > 0:
    st.subheader("📊 Podsumowanie Twojej wyceny")
    vat_rate = st.selectbox("Stawka VAT", [8, 23], help="8% dla osób prywatnych, 23% dla firm")
    
    suma_vat = suma_netto * (vat_rate / 100)
    suma_brutto = suma_netto + suma_vat

    c_n, c_v, c_b = st.columns(3)
    c_n.metric("Suma Netto", f"{suma_netto:,.2f} zł")
    c_v.metric(f"VAT {vat_rate}%", f"{suma_vat:,.2f} zł")
    c_b.metric("DO ZAPŁATY (Brutto)", f"{suma_brutto:,.2f} zł")

    if st.button("📄 Przygotuj profesjonalną ofertę"):
        if not klient:
            st.error("Wpisz nazwę klienta lub adres inwestycji!")
        else:
            df = pd.DataFrame(wybrane_uslugi)
            st.markdown(f"### Oferta dla: {klient}")
            st.table(df[["Usługa", "Ilość", "Cena jedn. (zł)", "Wartość (zł)"]])
            
            # POPRAWIONA LINIA 116 -
