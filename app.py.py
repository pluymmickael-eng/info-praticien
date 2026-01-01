import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Info-Praticien",
    page_icon="🛡️",
    layout="wide"
)

# --- 2. FONCTION DE CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # On charge le fichier CSV propre que tu as mis sur GitHub
    # IMPORTANT : Le fichier doit s'appeler exactement comme ça sur GitHub
    try:
        df = pd.read_csv("base_praticiens_clean.csv")
        # On remplit les vides par du texte vide pour éviter les erreurs d'affichage
        df = df.fillna("")
        return df
    except FileNotFoundError:
        return None

# Chargement
df = load_data()

# Si le fichier n'est pas trouvé, on arrête tout avec un message clair
if df is None:
    st.error("⚠️ Erreur Critique : Le fichier 'base_praticiens_clean.csv' est introuvable.")
    st.info("Vérifie sur GitHub que ton fichier s'appelle bien 'base_praticiens_clean.csv' (attention aux majuscules !).")
    st.stop()

# --- 3. BARRE LATÉRALE (Filtres) ---
st.sidebar.header("🔍 Recherche")

# Filtre : Ville
ville_search = st.sidebar.text_input("Ville (ex: Lyon)", "")

# Filtre : Profession
# On récupère la liste des métiers présents dans le fichier
liste_metiers = sorted(df['Profession'].unique())
choix_metiers = st.sidebar.multiselect(
    "Profession",
    options=liste_metiers,
    default=liste_metiers
)

# Filtre : Mots-clés (la "Killer Feature")
mot_cle = st.sidebar.text_input("Spécialité (ex: EMDR, TCC, Hypnose...)", "")

# --- 4. FILTRAGE DES DONNÉES ---
# On commence avec tout le monde, puis on réduit
df_filtre = df.copy()

# A. Filtre par profession
if choix_metiers:
    df_filtre = df_filtre[df_filtre['Profession'].isin(choix_metiers)]

# B. Filtre par Ville (si renseigné)
if ville_search:
    df_filtre = df_filtre[df_filtre['Ville'].str.contains(ville_search, case=False, na=False)]

# C. Filtre par Mot-clé (si renseigné)
if mot_cle:
    # On cherche dans la colonne Profession OU SavoirFaire
    mask = (
        df_filtre['Profession'].str.contains(mot_cle, case=False, na=False) |
        df_filtre['SavoirFaire'].str.contains(mot_cle, case=False, na=False)
    )
    df_filtre = df_filtre[mask]

# --- 5. AFFICHAGE DES RÉSULTATS ---
st.title("🛡️ Info-Praticien")
st.markdown("Annuaire des professionnels de santé vérifiés (RPPS/ADELI).")

# Compteur de résultats
nb_resultats = len(df_filtre)
st.metric(label="Praticiens trouvés", value=nb_resultats)

st.divider()

# Si on a trop de résultats, on prévient l'utilisateur
if nb_resultats > 100:
    st.warning("⚠️ Trop de résultats. Affinez votre recherche (Ville ou Spécialité) pour voir la liste.")
    # On affiche quand même les 10 premiers pour l'exemple
    st.write("Voici un aperçu des 10 premiers :")
    df_display = df_filtre.head(10)
else:
    df_display = df_filtre

# Affichage des fiches
for index, row in df_display.iterrows():
    with st.container():
        # En-tête de la fiche avec Nom et Profession
        c1, c2 = st.columns([3, 1])
        c1.subheader(f"👨‍⚕️ {row['Nom']} {row['Prenom']}")
        c1.caption(f"🎓 {row['Profession']}")
        
        # Adresse et Contact
        st.write(f"📍 **{row['CodePostal']} {row['Ville']}**")
        st.write(f"🏠 {row['AdresseComplete']}")
        
        if row['SavoirFaire']:
            st.info(f"💡 **Expertise :** {row['SavoirFaire']}")
        
        if row['Email']:
            st.write(f"📧 {row['Email']}")
            
        st.markdown("---")

# Pied de page
st.caption("Données issues de l'Annuaire Santé National - Mise à jour 2026")
