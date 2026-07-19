import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Accueil — Détection de Fraude Bancaire",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# STYLE CSS PERSONNALISÉ — thème marron deux tons harmonisé
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root {
        --brown-dark: #3E2723;
        --brown: #6D4C41;
        --brown-mid: #8D6E63;
        --tan: #EFE3D7;
        --cream: #FBF7F2;
        --gold: #D9A441;
        --green: #1B5E20;
        --grey: #4A4038;
    }

    /* Fond général : ton clair partout, plus de zone sombre "flottante" */
    .stApp {
        background: var(--tan);
    }

    .block-container { padding-top: 1.2rem; max-width: 100%; }

    /* ── Filet de sécurité : tout texte natif Streamlit (captions, libellés
       de widgets, markdown brut non encadré) est forcé en couleur foncée.
       Le sélecteur :not([class]) ne cible que les éléments SANS classe,
       donc il ne touche jamais mes propres blocs personnalisés (qui ont
       tous une classe) — pas de conflit avec les titres blancs du hero. ── */
    [data-testid="stMarkdownContainer"] p:not([class]),
    [data-testid="stMarkdownContainer"] li:not([class]),
    [data-testid="stMarkdownContainer"] span:not([class]),
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: var(--grey) !important;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: var(--brown-dark) !important;
        font-weight: 600;
    }

    /* Petite boîte de note (remplace st.caption, toujours visible) */
    .note-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        color: var(--grey) !important;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* ── Barre latérale : harmonisée au thème marron foncé ───── */
    section[data-testid="stSidebar"] {
        background: var(--brown-dark) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F1E4D8 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background-color: var(--gold) !important;
        color: var(--brown-dark) !important;
        font-weight: 700 !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] a:hover {
        background-color: rgba(217, 164, 65, 0.25) !important;
        border-radius: 8px;
    }

    /* ── Barre supérieure Streamlit : même teinte que la sidebar ── */
    header[data-testid="stHeader"] {
        background: var(--brown-dark) !important;
    }
    header[data-testid="stHeader"] * {
        color: #F1E4D8 !important;
    }

    /* ── Titre du projet : encadré, toujours visible et centré ── */
    .hero-box {
        background: var(--brown-dark);
        border-radius: 16px;
        padding: 1.6rem 1rem 1.4rem 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(62, 39, 35, 0.3);
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        margin: 0;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #EAD9C8;
        text-align: center;
        margin-top: 0.6rem;
        line-height: 1.6;
    }

    /* Cartes de métriques */
    .metric-card {
        background: linear-gradient(135deg, var(--brown-dark), var(--brown));
        padding: 1.4rem 1rem;
        border-radius: 14px;
        color: #FFFFFF;
        text-align: center;
        box-shadow: 0 4px 14px rgba(62, 39, 35, 0.35);
        height: 100%;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .metric-icon { font-size: 1.6rem; margin-bottom: 0.2rem; }
    .metric-value { font-size: 1.9rem; font-weight: 800; line-height: 1.1; color: #FFFFFF; }
    .metric-label { font-size: 0.8rem; opacity: 0.95; margin-top: 0.3rem; color: #F1E4D8; }

    /* Espacement entre sections */
    .section-spacer { height: 2.6rem; }

    /* ── Titres de section : toujours dans un cadre clair, donc  ──
       toujours lisibles quel que soit le fond derrière au défilement */
    .section-header-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-left: 6px solid var(--gold);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0 0 1rem 0;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--brown-dark);
        margin: 0;
    }

    /* Bloc pleine largeur */
    .full-block {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        color: var(--grey);
        font-size: 1rem;
        line-height: 1.7;
    }

    /* Cartes pipeline */
    .pipeline-card {
        background: var(--cream);
        border-radius: 12px;
        padding: 1rem 0.8rem;
        text-align: center;
        height: 100%;
        border: 1px solid #DDCBB8;
        border-top: 4px solid var(--brown-mid);
    }
    .pipeline-step {
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--gold);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .pipeline-icon { font-size: 1.6rem; margin: 0.35rem 0; }
    .pipeline-title { font-weight: 700; color: var(--brown-dark); font-size: 0.92rem; }
    .pipeline-desc { font-size: 0.75rem; color: var(--grey); margin-top: 0.2rem; }

    /* Tableau de résultats */
    div[data-testid="stDataFrame"] {
        border: 1px solid #DDCBB8;
        border-radius: 10px;
        overflow: hidden;
    }

    footer {visibility: hidden;}
    .app-footer {
        text-align: center;
        color: var(--brown);
        font-size: 0.82rem;
        padding-top: 1.5rem;
        border-top: 1px solid #DDCBB8;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def spacer():
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)


def section_header(icon, text):
    st.markdown(
        f'<div class="section-header-box"><p class="section-header">{icon} {text}</p></div>',
        unsafe_allow_html=True,
    )


def note_box(text):
    st.markdown(f'<div class="note-box">{text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# EN-TÊTE — encadré, centré, toujours lisible
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <p class="main-title">🔐 Détection de Fraude Bancaire</p>
    <p class="subtitle">
        Projet de fin d'année — Licence 2 Big Data | 2025–2026<br>
        Dataset : <b>Credit Card Fraud Detection</b> (ULB/Kaggle)
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MÉTRIQUES CLÉS — pleine largeur
# ─────────────────────────────────────────────────────────────
metrics = [
    ("📊", "284 807", "Transactions analysées"),
    ("🚨", "492", "Fraudes détectées (0,17 %)"),
    ("⚖️", "0,17 %", "Taux de fraude — fort déséquilibre"),
    ("🤖", "4", "Modèles ML comparés"),
]
cols = st.columns(4)
for col, (icon, value, label) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

spacer()

# ─────────────────────────────────────────────────────────────
# SECTION 1 — À PROPOS DU PROJET (pleine largeur)
# ─────────────────────────────────────────────────────────────
section_header("📋", "À propos du projet")
st.markdown("""
<div class="full-block">
Ce projet de fin d'année s'inscrit dans le cadre de la <b>Licence 2 Big Data</b>,
sous la direction du <b>Professeur M. Balde</b>. Il porte sur l'analyse de
transactions bancaires et la détection automatique de fraudes par des
approches de <b>Machine Learning</b>, à partir d'un dataset réel fortement
déséquilibré (0,17 % de fraudes).
</div>
""", unsafe_allow_html=True)

spacer()

# ─────────────────────────────────────────────────────────────
# SECTION 2 — PIPELINE (pleine largeur, 5 blocs)
# ─────────────────────────────────────────────────────────────
section_header("⚙️", "Pipeline mis en œuvre")
pipeline = [
    ("Étape 1", "🔍", "Exploration (EDA)", "Statistiques, distributions, corrélations"),
    ("Étape 2", "⚙️", "Prétraitement", "Normalisation, SMOTE, split 80/20"),
    ("Étape 3", "🤖", "Modélisation", "4 algorithmes ML entraînés"),
    ("Étape 4", "📊", "Évaluation", "Precision, Recall, F1, AUC-ROC"),
    ("Étape 5", "🖥️", "Déploiement", "Application Streamlit interactive"),
]
pcols = st.columns(5)
for pcol, (step, icon, title, desc) in zip(pcols, pipeline):
    with pcol:
        st.markdown(f"""
        <div class="pipeline-card">
            <div class="pipeline-step">{step}</div>
            <div class="pipeline-icon">{icon}</div>
            <div class="pipeline-title">{title}</div>
            <div class="pipeline-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

spacer()

# ─────────────────────────────────────────────────────────────
# SECTION 3 — RÉSULTATS (pleine largeur)
# ─────────────────────────────────────────────────────────────
section_header("🏆", "Meilleurs résultats")

results = pd.DataFrame([
    ["XGBoost",          0.9808, 0.79],
    ["Random Forest",    0.9688, 0.82],
    ["Régression Log.",  0.9698, 0.11],
    ["Isolation Forest", 0.9536, 0.32],
], columns=["Modèle", "AUC-ROC", "F1-Score"])

best_auc = results["AUC-ROC"].max()
best_f1 = results["F1-Score"].max()

def highlight_best(s):
    if s.name == "AUC-ROC":
        return ["background-color: #D9A441; color: #3E2723; font-weight:800" if v == best_auc else "" for v in s]
    if s.name == "F1-Score":
        return ["background-color: #D9A441; color: #3E2723; font-weight:800" if v == best_f1 else "" for v in s]
    return ["" for _ in s]

st.dataframe(
    results.style.apply(highlight_best, axis=0).format({"AUC-ROC": "{:.4f}", "F1-Score": "{:.2f}"}),
    hide_index=True,
    use_container_width=True,
)
note_box("🟨 Surlignage doré = meilleure valeur de la colonne. XGBoost offre le meilleur AUC-ROC ; Random Forest le meilleur F1-Score sur la classe Fraude.")

spacer()

# ─────────────────────────────────────────────────────────────
# SECTION 4 — EN BREF (pleine largeur)
# ─────────────────────────────────────────────────────────────
section_header("🧾", "En bref")
st.markdown("""
<div class="full-block">

- Entraînement sur données **rééquilibrées (SMOTE)**
- Évaluation sur le jeu de test **original**, non modifié
- Métriques adaptées au déséquilibre : **F1-Score**, **AUC-ROC**

</div>
""", unsafe_allow_html=True)

spacer()

# ─────────────────────────────────────────────────────────────
# PIED DE PAGE
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Dakar Institute of Technology — Détection de Fraude Bancaire par Machine Learning<br>
    Patrice DIONE · Mame Faty DIENG — Encadré par Professeur M. Balde
</div>
""", unsafe_allow_html=True)