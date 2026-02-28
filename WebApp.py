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

# --- 3. PASEK BOCZNY (NAWIGACJA I KONTAKT) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4336/4336544.png", width=100) # Ikona logo
st.sidebar.title(@renovations.art)
st.sidebar.markdown("""
### 📞 Kontakt
**Telefon:** +48 601-403-157  
**E-mail:** renovationsartstg@gmail.com  
**Lokalizacja:** Starogard Gdański i okolice (50km)  

---
*Gwarantujemy terminowość i czystość na budowie.*
""")

# --- 4. STRONA GŁÓWNA - WIZYTÓWKA ---
st.title(f"🏠 {@renovations.art} - Solidne Remonty i Budowa")
st.write("Witamy na naszej stronie! Specjalizujemy się w kompleksowych wykończeniach wnętrz oraz stanach surowych. Skorzystaj z naszego kalkulatora poniżej, aby otrzymać wstępną wycenę.")

# Sekcja "Dlaczego my" w kolumnach
col_a, col_b, col_c = st.columns(3)
col_a.success("✅ **Bezpyłowe gładzie**")
col_b.success("✅ **Gwarancja 24 m-ce**")
col_c.success("✅ **Czystość po pracy**")

st.divider()

# --- 5. KALKULATOR OFERTOWY ---
st.header("🧮 Kalkulator darmowej wyceny")
klient = st.text_input("Nazwa Klienta / Adres inwestycji", placeholder="np. Mieszkanie ul. Polna")
data_dzis = datetime.date.today().strftime("%d-%m-%Y")

wybrane_uslugi = []
suma_netto = 0

# Interfejs zakładek z ikonami
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
                st.write("Wartość")
                st.write(f"{ilosc * cena:,.2f} zł")
            
            if ilosc > 0:
                wartosc = ilosc * cena
                wybrane_uslugi.append({"Usługa": usluga, "Ilość": ilosc, "Cena jedn.": f"{cena} zł", "Wartość": wartosc})
                suma_netto += wartosc
        st.divider()

# --- 6. PODSUMOWANIE FINANSOWE ---
if suma_netto > 0:
    st.subheader("Podsumowanie Twojej wyceny")
    vat_rate = st.selectbox("Stawka VAT", [8, 23], help="8% dla osób prywatnych, 23% dla firm")
    
    suma_vat = suma_netto * (vat_rate / 100)
    suma_brutto = suma_netto + suma_vat

    c_n, c_v, c_b = st.columns(3)
    c_n.metric("Suma Netto", f"{suma_netto:,.2f} zł")
    c_v.metric(f"VAT {vat_rate}%", f"{suma_vat:,.2f} zł")
    c_b.metric("DO ZAPŁATY (Brutto)", f"{suma_brutto:,.2f} zł")

    # Przycisk generowania
    if st.button("📄 Przygotuj gotową ofertę PDF/TXT"):
        if not klient:
            st.error("Wpisz nazwę klienta lub adres inwestycji na górze strony!")
        else:
            raport = f"OFERTA: {FIRMA}\nDLA: {klient}\nDATA: {data_dzis}\n" + "="*30 + "\n"
            for item in wybrane_uslugi:
                raport += f"- {item['Usługa']}: {item['Ilość']} x {item['Cena jedn.']} = {item['Wartość']:.2f} zł\n