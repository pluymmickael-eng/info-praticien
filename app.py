import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- CONFIGURATION ---
st.set_page_config(page_title="Info-Praticien", page_icon="🛡️", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        # On lit le fichier PROPRE (le CSV), pas le fichier brut
        df = pd.read_csv("base_praticiens_clean.csv")
        df = df.fillna("") # On remplit les vides
        return df
    except FileNotFoundError:
        return None

df = load_data()

# --- VÉRIFICATION ---
if df is None:
    st.error("⚠️ Fichier 'base_praticiens_clean.csv' introuvable sur GitHub !")
    st.stop()

# --- INTERFACE ---
st.sidebar.title("🛡️ Info-Praticien")
ville = st.sidebar.text_input("📍 Ville", "")
metiers = st.sidebar.multiselect("🎓 Profession", options=sorted(df['Profession'].unique()))
mot_cle = st.sidebar.text_input("💡 Spécialité (ex: EMDR)", "")

# --- FILTRES ---
df_filtre = df.copy()
if metiers:
    df_filtre = df_filtre[df_filtre['Profession'].isin(metiers)]
if ville:
    df_filtre = df_filtre[df_filtre['Ville'].str.contains(ville, case=False, na=False)]
if mot_cle:
    mask = df_filtre['Profession'].str.contains(mot_cle, case=False, na=False) | \
           df_filtre['SavoirFaire'].str.contains(mot_cle, case=False, na=False)
    df_filtre = df_filtre[mask]

# --- RÉSULTATS ---
st.title(f"🔍 {len(df_filtre)} Praticiens trouvés")
st.write("Ceci est une version démo.")

# On affiche les 20 premiers résultats pour tester
for index, row in df_filtre.head(20).iterrows():
    with st.expander(f"{row['Nom']} {row['Prenom']} - {row['Profession']}"):
        st.write(f"📍 {row['CodePostal']} {row['Ville']}")
        st.write(f"🏠 {row['AdresseComplete']}")
        st.caption(f"Savoir-faire : {row['SavoirFaire']}")
