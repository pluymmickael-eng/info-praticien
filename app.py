import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Info-Praticien | Registre Officiel",
    page_icon="🇫🇷",
    layout="wide", # On passe en large pour que ça respire
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "PREMIUM DESIGN" ---
st.markdown("""
<style>
    /* FOND ET TYPO */
    .stApp {
        background-color: #F9FAFB; /* Gris très pâle 'Clinique' */
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* CACHER LES ÉLÉMENTS STREAMLIT */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 0 !important; max-width: 1200px !important;}

    /* HEADER */
    .hero-section {
        background: linear-gradient(180deg, #FFFFFF 0%, #F3F4F6 100%);
        padding: 60px 20px 40px 20px;
        text-align: center;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 30px;
    }
    .main-title {
        color: #111827;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #4B5563;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 5px;
    }
    .ans-badge {
        background-color: #DEF7EC;
        color: #03543F;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 99px;
        border: 1px solid #BCF0DA;
        display: inline-block;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* BARRE DE RECHERCHE STYLISÉE */
    .search-container {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
        margin-top: 20px;
    }

    /* CARTES RÉSULTATS */
    .pro-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .pro-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
        border-color: #E5E7EB;
    }
    .verified-icon {
        color: #059669; /* Vert confiance */
        margin-left: 6px;
        font-size: 14px;
    }
    .job-title {
        color: #1D4ED8; /* Bleu médical */
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* BOUTONS ET INFO */
    .phone-badge {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CHARGEMENT & DÉTECTION ---
def trouver_colonne(df, mots_cles):
    for col in df.columns:
        if any(mot.lower() in col.lower() for mot in mots_cles):
            return col
    return None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("base_praticiens_clean.csv", sep=',', dtype=str)
        # Fallback si séparateur incorrect
        if len(df.columns) < 2: 
             df = pd.read_csv("base_praticiens_clean.csv", sep='|', dtype=str)
        df = df.fillna("")
        return df
    except:
        return None

df = load_data()

# --- 4. HEADER (DESIGN ÉPURÉ) ---
st.markdown("""
<div class="hero-section">
    <div class="ans-badge">🇫🇷 Données Certifiées État</div>
    <h1 class="main-title">Registre des Praticiens</h1>
    <p class="subtitle">Reconnus par l'Agence du Numérique en Santé (ANS).</p>
    <p style="color: #6B7280; font-style: italic; margin-top: 10px;">"Mettez-vous et mettez vos proches entre de bonnes mains."</p>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ Base de données en cours de mise à jour.")
    st.stop()

# --- 5. IDENTIFICATION COLONNES ---
# On mappe les colonnes vitales
col_prof = trouver_colonne(df, ['profession', 'metier', 'job', 'libellé profession'])
col_nom = trouver_colonne(df, ['nom', 'exercice', 'last name'])
col_prenom = trouver_colonne(df, ['prenom', 'prénom'])
col_ville = trouver_colonne(df, ['ville', 'commune', 'bureau'])
col_cp = trouver_colonne(df, ['code postal', 'cp', 'postal'])
col_tel = trouver_colonne(df, ['telephone', 'téléphone', 'tel', 'coordonnées'])
col_adresse = trouver_colonne(df, ['adresse', 'voie', 'rue'])

# --- 6. MOTEUR DE RECHERCHE "DOCTOLIB STYLE" ---
# On met ça dans un conteneur blanc centré
c_space1, c_main, c_space2 = st.columns([1, 6, 1])

with c_main:
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # ZONE 1 : Le Métier (Liste déroulante intelligente)
        # C'est ça ta "suggestion" : l'utilisateur choisit dans une liste existante
        c1, c2 = st.columns([1, 1])
        
        with c1:
            liste_metiers = ["Toutes professions"] + sorted(df[col_prof].unique()) if col_prof else []
            choix_metier = st.selectbox(
                "Je cherche un...", 
                options=liste_metiers,
                index=0,
                help="Sélectionnez la profession certifiée"
            )
            
        # ZONE 2 : La Ville / Nom (Texte libre)
        with c2:
            recherche_libre = st.text_input(
                "À proximité de / Nom", 
                placeholder="Ex: Lyon, 69002, ou Dr Martin..."
            )
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FILTRAGE ET RÉSULTATS ---
df_final = df.copy()

# Filtre A : Métier (si sélectionné)
if choix_metier and choix_metier != "Toutes professions" and col_prof:
    df_final = df_final[df_final[col_prof] == choix_metier]

# Filtre B : Texte Libre (si rempli)
if recherche_libre:
    terme = recherche_libre.lower()
    # On cherche dans Nom, Ville ou CP
    mask = df_final[col_nom].astype(str).str.lower().str.contains(terme, na=False)
    if col_ville:
        mask = mask | df_final[col_ville].astype(str).str.lower().str.contains(terme, na=False)
    if col_cp:
        mask = mask | df_final[col_cp].astype(str).str.lower().str.contains(terme, na=False)
    df_final = df_final[mask]

# --- 8. AFFICHAGE CARTE PRO ---
st.write("") # Espace

# On affiche les résultats seulement si une recherche est faite (plus propre)
if recherche_libre or (choix_metier and choix_metier != "Toutes professions"):
    
    nb = len(df_final)
    # Titre discret des résultats
    st.markdown(f"<div style='text-align: center; color: #6B7280; margin-bottom: 20px;'>{nb} professionnels certifiés trouvés</div>", unsafe_allow_html=True)

    # On utilise 2 colonnes pour les résultats (Format Grille plus moderne)
    col_res1, col_res2 = st.columns(2)
    
    for index, row in df_final.head(40).iterrows(): # Limite à 40
        
        # Choix de la colonne (gauche ou droite)
        col_dest = col_res1 if index % 2 == 0 else col_res2
        
        # Récup des données
        nom = row[col_nom] if col_nom else "Inconnu"
        prenom = row[col_prenom] if col_prenom else ""
        job = row[col_prof] if col_prof else ""
        
        # Adresse propre
        adresse = row[col_adresse] if col_adresse else ""
        ville = f"{row[col_cp]} {row[col_ville]}" if (col_cp and col_ville) else ""
        adresse_full = f"{adresse}<br>{ville}" if adresse else ville
        
        # Téléphone
        tel_html = ""
        if col_tel and row[col_tel]:
            tel_clean = row[col_tel]
            tel_html = f'<div class="phone-badge">📞 {tel_clean}</div>'
        
        with col_dest:
            st.markdown(f"""
            <div class="pro-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <div class="job-title">{job}</div>
                        <div style="font-size: 18px; font-weight: 700; color: #111827;">
                            {nom} {prenom} 
                            <span title="Diplôme vérifié" class="verified-icon">✅</span>
                        </div>
                        <div style="font-size: 14px; color: #4B5563; margin-top: 8px; line-height: 1.5;">
                            📍 {adresse_full}
                        </div>
                        {tel_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    # PAGE D'ACCUEIL VIDE (RASSURANTE)
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c2:
        st.info("👋 Commencez par sélectionner une profession ou tapez une ville ci-dessus.")
