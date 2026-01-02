import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Info-Praticien | Portail National",
    page_icon="🇫🇷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. LE DESIGN "CARRÉ & MÉDICAL" (CSS) ---
st.markdown("""
<style>
    /* Reset et polices */
    .stApp {
        background-color: #F4F7FA; /* Fond gris très clair, plus doux que le blanc pur */
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Nettoyage interface */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100%;} /* On enlève les paddings pour gérer nous-mêmes */

    /* --- LE HEADER BLEU PRO --- */
    .hero-header {
        background: linear-gradient(135deg, #004e92 0%, #000428 100%); /* Dégradé bleu nuit médical */
        padding: 40px 20px 60px 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 16px;
        opacity: 0.9;
        margin-top: 10px;
        font-weight: 400;
    }
    .official-badge {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* --- LA BARRE DE RECHERCHE ERGONOMIQUE --- */
    /* On la fait "flotter" sur la limite du bleu et du gris */
    .search-container-floating {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin: -35px auto 30px auto; /* Marge négative pour remonter sur le bleu */
        max-width: 700px; /* Largeur max pour rester ergonomique */
        width: 90%;
    }
    /* Style du champ input */
    .stTextInput>div>div>input {
        border: none;
        padding: 15px;
        font-size: 18px;
        border-bottom: 2px solid #eee;
        border-radius: 0;
        background: transparent;
    }
    .stTextInput>div>div>input:focus {
        box-shadow: none;
        border-bottom-color: #004e92;
    }

    /* --- CARTES RESULTATS --- */
    .results-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
    }
    .pro-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #eef2f6;
        border-left: 4px solid #004e92;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .verified-badge {
        background-color: #E8F5E9; color: #2E7D32; 
        padding: 3px 8px; border-radius: 4px; 
        font-size: 11px; font-weight: 700; 
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Email link style */
    .email-link {
        color: #004e92; text-decoration: none; font-weight: 500;
        display: inline-flex; align-items: center;
        margin-top: 10px;
    }
    .email-link:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- 3. CHARGEMENT DONNÉES ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("base_praticiens_clean.csv", sep=',', dtype=str)
        df = df.fillna("")
        return df
    except:
        return None

df = load_data()

# --- 4. HEADER "HERO" (La partie Bleu Pro) ---
st.markdown("""
<div class="hero-header">
    <div class="official-badge">🇫🇷 Données RPPS Certifiées</div>
    <h1 class="hero-title">Portail National Info-Praticien</h1>
    <p class="hero-subtitle">Vérifiez les diplômes des professionnels de santé mentale.<br>Luttez contre l'exercice illégal.</p>
</div>
""", unsafe_allow_html=True)

# --- 5. BARRE DE RECHERCHE FLOTTANTE (Ergonomique) ---
# On utilise un conteneur spécial pour la faire chevaucher le header
st.markdown('<div class="search-container-floating">', unsafe_allow_html=True)
recherche = st.text_input("Zone de recherche", placeholder="🔍 Tapez un nom, une ville ou une spécialité...", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)


# --- 6. RÉSULTATS ---
# On met tout dans un conteneur centré propre
st.markdown('<div class="results-container">', unsafe_allow_html=True)

if df is None:
    st.error("⚠️ Service momentanément indisponible (Maintenance Base de Données).")
    st.stop()

df_final = df.copy()

if recherche:
    terme = recherche.lower()
    mask = (
        df_final['Nom'].str.lower().str.contains(terme) |
        df_final['Ville'].str.lower().str.contains(terme) |
        df_final['Profession'].str.lower().str.contains(terme)
    )
    df_final = df_final[mask]
    
    nb = len(df_final)
    if nb > 0:
        # Petit message de succès discret
        st.markdown(f"<div style='text-align: center; color: #666; margin-bottom: 20px;'>✅ <b>{nb}</b> professionnels trouvés dans le registre officiel.</div>", unsafe_allow_html=True)
        
        # Boucle d'affichage des cartes
        for index, row in df_final.head(20).iterrows():
            # Gestion Email
            email_html = ""
            if 'Email' in row and row['Email']: 
                email_html = f"""<a href="mailto:{row['Email']}" class="email-link">✉️ Contacter ({row['Email']})</a>"""
            
            # La Carte HTML propre
            st.markdown(f"""
            <div class="pro-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                         <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                            <h3 style="font-size: 18px; margin: 0; color: #1a1a1a;">{row['Nom']} {row['Prenom']}</h3>
                            <span class="verified-badge">Vérifié État</span>
                        </div>
                        <div style="color: #004e92; font-weight: 600; font-size: 15px;">{row['Profession']}</div>
                        
                        <div style="color: #555; font-size: 14px; margin-top: 12px; line-height: 1.4;">
                            📍 {row['AdresseComplete']}<br>
                            <b>{row['CodePostal']} {row['Ville']}</b>
                        </div>
                        {email_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("🤔 Aucun résultat exact. Essayez une recherche plus large.")

else:
    # ACCUEIL VIDE ÉPURÉ
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 40px;">
        <h3 style="color: #333;">Pourquoi ce portail ?</h3>
        <p>Face à la multiplication des pratiques non réglementées, ce service d'utilité publique vous permet de distinguer les professionnels diplômés d'État.</p>
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 30px;">
            <div>🛡️<br><b>100% Officiel</b><br><small>Source RPPS</small></div>
            <div>🔬<br><b>Scientifique</b><br><small>Zéro pseudo-science</small></div>
            <div>🤝<br><b>Gratuit</b><br><small>Service public</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Fin du results-container
