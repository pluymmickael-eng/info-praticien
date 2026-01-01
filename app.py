import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- CONFIGURATION ---
st.set_page_config(page_title="Info-Praticien", page_icon="🛡️", layout="wide")

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    try:
        # On essaie de lire avec différents séparateurs au cas où
        try:
            df = pd.read_csv("base_praticiens_clean.csv", sep=',')
        except:
            df = pd.read_csv("base_praticiens_clean.csv", sep='|')
            
        df = df.fillna("")
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Fichier introuvable sur GitHub.")
    st.stop()

# --- DÉTECTION AUTOMATIQUE DES COLONNES ---
# On crée une fonction pour trouver le vrai nom de la colonne dans le fichier
def trouver_colonne(df, mots_cles):
    for col in df.columns:
        if any(mot.lower() in col.lower() for mot in mots_cles):
            return col
    return None

# On cherche les vrais noms
col_prof = trouver_colonne(df, ['profession', 'libellé profession'])
col_ville = trouver_colonne(df, ['ville', 'commune', 'bureau'])
col_cp = trouver_colonne(df, ['code postal', 'postal'])
col_nom = trouver_colonne(df, ['nom', 'exercice'])
col_prenom = trouver_colonne(df, ['prénom', 'prenom'])
col_savoir = trouver_colonne(df, ['savoir', 'expertise']) # Peut être None

# Si on ne trouve pas la colonne Profession, on arrête
if not col_prof:
    st.error(f"❌ Impossible de trouver la colonne des professions. Voici les colonnes disponibles : {list(df.columns)}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("🛡️ Info-Praticien")
st.sidebar.caption("Annuaire vérifié RPPS/ADELI")

ville = st.sidebar.text_input("📍 Ville", "")

# On utilise le nom de colonne détecté (col_prof)
metiers = st.sidebar.multiselect("🎓 Profession", options=sorted(df[col_prof].unique()))
mot_cle = st.sidebar.text_input("💡 Spécialité (ex: EMDR)", "")

# --- FILTRES ---
df_filtre = df.copy()

if metiers:
    df_filtre = df_filtre[df_filtre[col_prof].isin(metiers)]

if ville and col_ville:
    df_filtre = df_filtre[df_filtre[col_ville].str.contains(ville, case=False, na=False)]

if mot_cle:
    # On construit le filtre intelligemment
    mask = df_filtre[col_prof].str.contains(mot_cle, case=False, na=False)
    if col_savoir:
        mask = mask | df_filtre[col_savoir].str.contains(mot_cle, case=False, na=False)
    df_filtre = df_filtre[mask]

# --- RÉSULTATS ---
st.title(f"🔍 {len(df_filtre)} Praticiens trouvés")

# Affichage des 20 premiers
for index, row in df_filtre.head(20).iterrows():
    # On sécurise l'affichage des noms/prénoms
    nom = row[col_nom] if col_nom else "Inconnu"
    prenom = row[col_prenom] if col_prenom else ""
    profession = row[col_prof]
    
    with st.expander(f"👨‍⚕️ {nom} {prenom} - {profession}"):
        if col_cp and col_ville:
            st.write(f"📍 {row[col_cp]} {row[col_ville]}")
        if col_savoir and row[col_savoir]:
            st.info(f"💡 {row[col_savoir]}")
