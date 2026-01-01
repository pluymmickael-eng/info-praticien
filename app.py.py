import pandas as pd

# --- CONFIGURATION ---
SOURCE_FILE = 'ps-libreacces-personne-activite.txt' 
OUTPUT_FILE = 'base_praticiens_clean.csv'

# Liste des mots-clés à garder (insensible à la casse)
KEYWORDS = ['Psychologue', 'Psychiatre', 'Psychothérapeute', 'Psychiatrie']

# Si tu veux filtrer par département (ex: '59' ou '75'). Mets None pour toute la France.
DEPARTEMENT_CIBLE = None 

# ---------------------

print("⏳ Chargement du fichier (patience...)...")
# On utilise l'encodage 'utf-8' qui semble avoir fonctionné pour le chargement
df = pd.read_csv(SOURCE_FILE, sep='|', encoding='utf-8', low_memory=False)

print(f"✅ Fichier chargé : {len(df)} lignes.")

# --- 1. DÉTECTION INTELLIGENTE DES COLONNES ---
print("🕵️‍♂️ Recherche automatique des bonnes colonnes...")

def trouver_colonne(mots_cles, df_cols):
    """Cherche une colonne qui contient tous les mots clés donnés"""
    for col in df_cols:
        # On met tout en minuscule pour comparer
        col_lower = col.lower()
        # Si tous les mots clés sont dans le nom de la colonne
        if all(mot in col_lower for mot in mots_cles):
            return col
    return None

# On cherche la colonne qui contient "libell" ET "profession" (peu importe les accents)
col_profession = trouver_colonne(['libell', 'profession'], df.columns)
# On cherche la colonne qui contient "libell" ET "savoir" (pour savoir-faire)
col_savoir = trouver_colonne(['libell', 'savoir'], df.columns)
# On cherche le code postal
col_cp = trouver_colonne(['code', 'postal'], df.columns)
# On cherche la ville
col_ville = trouver_colonne(['libell', 'commune'], df.columns)
# On cherche le nom
col_nom = trouver_colonne(['nom', 'exercice'], df.columns)

# Vérification
if not col_profession:
    print("❌ ERREUR CRITIQUE : Impossible de trouver la colonne Profession.")
    print("Voici les colonnes disponibles :", df.columns.tolist())
    exit()

print(f"   -> Colonne Profession identifiée : '{col_profession}'")
print(f"   -> Colonne Savoir-Faire identifiée : '{col_savoir}'")

# --- 2. FILTRAGE ---
print("🔍 Filtrage des praticiens (C'est là que la magie opère)...")

# On remplit les vides pour éviter les bugs
df[col_profession] = df[col_profession].fillna('')
df[col_savoir] = df[col_savoir].fillna('')

def is_target(row):
    # On regarde dans la profession ET le savoir-faire
    prof = str(row[col_profession]).lower()
    savoir = str(row[col_savoir]).lower()
    
    # On vérifie si un des mots clés est présent
    for k in KEYWORDS:
        k_lower = k.lower()
        if k_lower in prof or k_lower in savoir:
            return True
    return False

# Application du filtre
mask = df.apply(is_target, axis=1)
df_clean = df[mask].copy()

print(f"📉 Praticiens trouvés (avant filtre géo) : {len(df_clean)}")

# --- 3. NETTOYAGE ADRESSE ---
if col_cp:
    # On vire ceux sans code postal
    df_clean = df_clean.dropna(subset=[col_cp])
    # On nettoie le code postal (enlève les '.0' si présents)
    df_clean[col_cp] = df_clean[col_cp].astype(str).str.replace(r'\.0$', '', regex=True)

    if DEPARTEMENT_CIBLE:
        print(f"📍 Restriction au département : {DEPARTEMENT_CIBLE}")
        df_clean = df_clean[df_clean[col_cp].str.startswith(DEPARTEMENT_CIBLE)]

# --- 4. EXPORT ---
# On sélectionne les colonnes utiles à sauvegarder
cols_a_garder = [col_nom, col_profession, col_savoir, col_cp, col_ville]
# On ajoute l'email si on le trouve
col_email = trouver_colonne(['mail'], df.columns)
if col_email:
    cols_a_garder.append(col_email)

print("💾 Sauvegarde...")
df_clean[cols_a_garder].to_csv(OUTPUT_FILE, index=False, sep=',')

print(f"🚀 TERMINE ! Tu as {len(df_clean)} pros dans le fichier '{OUTPUT_FILE}'.")
