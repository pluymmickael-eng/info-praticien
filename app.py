import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Info-Praticien | Portail National",
    page_icon="🇫🇷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS (DESIGN MÉDICAL & PROPRE) ---
st.markdown("""
<style>
    /* Reset général */
    .stApp {
        background-color: #F8F9FA;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Cacher les éléments Streamlit inutiles */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 0 !important; max-width: 100%;}

    /* HEADER BLEU INTEGRAL */
    .hero-header {
        background-color: #000091; /* Bleu Institutionnel */
        padding: 40px 20px 40px 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* INPUT DE RECHERCHE DANS LE BLEU */
    .stTextInput > div > div > input {
        border: none;
        border-radius: 8px;
        padding: 15px;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* CARTES RÉSULTATS */
    .pro-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #000091; /* Marqueur bleu à gauche */
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    h1 { color: white !important; font-size: 28px; font-weight: 700; margin-bottom: 10px;}
    p { font-size: 14px; opacity: 0.9;}
    
</style>
""", unsafe_allow_html=True)

# --- 3. INTELLIGENCE ARTIFICIELLE (Détection des colonnes) ---
def trouver_colonne(df, mots_cles):
    """Cherche une colonne qui contient un des mots clés (insensible à la casse)"""
    for col in df.columns:
        for mot in mots_cles:
            if mot.lower() in col.lower():
                return col
    return None # Si on trouve rien

# --- 4. CHARGEMENT ROBUSTE ---
@st.cache_data
def load_data():
    try:
        # On essaie de lire avec virgule
        df = pd.read_csv("base_praticiens_clean.csv", sep=',', dtype=str)
        if len(df.columns) < 2: # Si ça a foiré (tout dans une colonne), on tente le pipe |
             df = pd.read_csv("base_praticiens_clean.csv", sep='|', dtype=str)
        
        df = df.fillna("")
        return df
    except:
        return None

df = load_data()

# --- 5. HEADER (L'EN-TÊTE BLEU) ---
st.markdown("""
<div class="hero-header">
    <div style="font-size: 40px; margin-bottom: 10px;">🇫🇷</div>
    <h1>Portail Info-Praticien</h1>
    <p>Annuaire de vérification des diplômes de santé.</p>
</div>
""", unsafe_allow_html=True)

# --- 6. GESTION DES ERREURS (Anti-Crash) ---
if df is None:
    st.error("⚠️ Maintenance des données en cours.")
    st.stop()

# On identifie les vrais noms des colonnes dans TON fichier
col_nom = trouver_colonne(df, ['nom', 'exercice', 'last name'])
col_prenom = trouver_colonne(df, ['prenom', 'prénom', 'first name'])
col_prof = trouver_colonne(df, ['profession', 'metier', 'job'])
col_ville = trouver_colonne(df, ['ville', 'commune', 'bureau'])
col_cp = trouver_colonne(df, ['code', 'postal', 'cp'])
col_email = trouver_colonne(df, ['email', 'mail', 'courriel'])

# Si on ne trouve pas la colonne NOM, on prend la première colonne par défaut pour éviter le crash
if not col_nom:
    col_nom = df.columns[0] 

# --- 7. BARRE DE RECHERCHE (Simple et centrée) ---
col_search, _ = st.columns([1, 0.01]) # Astuce pour centrer
with col_search:
    recherche = st.text_input("Recherche", placeholder="🔍 Nom, Ville ou Profession...", label_visibility="collapsed")

# --- 8. RÉSULTATS ---
if recherche:
    terme = recherche.lower()
    
    # On construit le filtre dynamiquement (pour éviter le KeyError)
    mask = df[col_nom].astype(str).str.lower().str.contains(terme, na=False)
    
    if col_ville:
        mask = mask | df[col_ville].astype(str).str.lower().str.contains(terme, na=False)
    if col_prof:
        mask = mask | df[col_prof].astype(str).str.lower().str.contains(terme, na=False)
        
    df_final = df[mask]
    
    st.write(f"**{len(df_final)}** résultat(s)")
    
    for index, row in df_final.head(20).iterrows():
        # Récupération sécurisée des données
        nom = row[col_nom]
        prenom = row[col_prenom] if col_prenom else ""
        profession = row[col_prof] if col_prof else "Profession de santé"
        ville = f"{row[col_cp]} {row[col_ville]}" if (col_cp and col_ville) else ""
        email = row[col_email] if (col_email and row[col_email]) else None
        
        # HTML Email
        btn_email = ""
        if email:
            btn_email = f'<a href="mailto:{email}" style="color:#000091; font-weight:bold; text-decoration:none;">✉️ Contacter</a>'

        st.markdown(f"""
        <div class="pro-card">
            <div style="font-size: 18px; font-weight: bold; color: #333;">
                👨‍⚕️ {nom} {prenom}
            </div>
            <div style="color: #000091; font-weight: 600; margin-top: 4px;">
                {profession}
            </div>
            <div style="color: #666; font-size: 14px; margin-top: 8px;">
                📍 {ville}
            </div>
            <div style="margin-top: 10px;">
                {btn_email}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Accueil Vide
    st.info("👋 Tapez le nom d'un praticien ou une ville pour vérifier un diplôme.")
