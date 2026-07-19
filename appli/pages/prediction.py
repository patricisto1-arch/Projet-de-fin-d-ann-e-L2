import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Prédiction", page_icon="🔍", layout="wide")

# ─────────────────────────────────────────────────────────────
# STYLE CSS PERSONNALISÉ — même thème marron deux tons
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
        --terracotta: #C0625B;
        --grey: #4A4038;
    }

    .stApp { background: var(--tan); }
    .block-container { padding-top: 1.2rem; max-width: 100%; }

    /* ── Filet de sécurité : texte natif Streamlit (captions, libellés de
       widgets, markdown brut non encadré) forcé en couleur foncée.
       :not([class]) ne cible que les éléments sans classe, donc ne touche
       jamais mes blocs personnalisés (toujours classés). ── */
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
    .note-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        color: var(--grey) !important;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: var(--brown-dark) !important; }
    section[data-testid="stSidebar"] * { color: #F1E4D8 !important; }
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
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: var(--brown) !important;
        border-color: var(--brown-mid) !important;
    }

    /* Barre supérieure Streamlit */
    header[data-testid="stHeader"] { background: var(--brown-dark) !important; }
    header[data-testid="stHeader"] * { color: #F1E4D8 !important; }

    /* En-tête de page, encadré et centré */
    .hero-box {
        background: var(--brown-dark);
        border-radius: 16px;
        padding: 1.4rem 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(62, 39, 35, 0.3);
    }
    .hero-title { font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 0; }
    .hero-subtitle { font-size: 0.98rem; color: #EAD9C8; margin-top: 0.4rem; }

    /* Titres de section : toujours encadrés, donc toujours lisibles */
    .section-header-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-left: 6px solid var(--gold);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0 1rem 0;
    }
    .section-header { font-size: 1.2rem; font-weight: 700; color: var(--brown-dark); margin: 0; }

    /* Blocs pleine largeur */
    .full-block {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        color: var(--grey);
        line-height: 1.7;
    }

    /* Résultat de prédiction */
    .result-banner {
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        font-size: 1.15rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .result-fraud { background: #F6DEDC; color: #7A2E27; border: 2px solid var(--terracotta); }
    .result-legit { background: #E3EEE0; color: #1B5E20; border: 2px solid #6B9E6E; }

    /* Métriques natives st.metric */
    div[data-testid="stMetric"] {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 12px;
        padding: 0.8rem;
    }
    div[data-testid="stMetric"] label { color: var(--brown) !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--brown-dark) !important; }

    /* Bouton principal */
    button[kind="primary"] {
        background-color: var(--brown-dark) !important;
        border-color: var(--brown-dark) !important;
    }
    button[kind="primary"]:hover {
        background-color: var(--brown) !important;
        border-color: var(--brown) !important;
    }
</style>
""", unsafe_allow_html=True)


def section_header(icon, text):
    st.markdown(
        f'<div class="section-header-box"><p class="section-header">{icon} {text}</p></div>',
        unsafe_allow_html=True,
    )


st.markdown("""
<div class="hero-box">
    <p class="hero-title">🔍 Prédiction en temps réel</p>
    <p class="hero-subtitle">Saisissez les caractéristiques d'une transaction pour prédire si elle est frauduleuse.</p>
</div>
""", unsafe_allow_html=True)

# ── Chargement des modèles ─────────────────────────────────
# Chemin robuste : remonte depuis prediction.py (appli/pages/) jusqu'à
# appli/, où se trouve le dossier models/ — peu importe d'où la commande
# streamlit est lancée
APPLI_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = APPLI_DIR / "models"

@st.cache_resource
def load_models():
    models = {}
    with open(MODELS_DIR / 'logistic_regression.pkl', 'rb') as f:
        models['Régression Logistique'] = pickle.load(f)
    with open(MODELS_DIR / 'random_forest.pkl', 'rb') as f:
        models['Random Forest'] = pickle.load(f)
    with open(MODELS_DIR / 'xgboost.pkl', 'rb') as f:
        models['XGBoost'] = pickle.load(f)
    with open(MODELS_DIR / 'isolation_forest.pkl', 'rb') as f:
        models['Isolation Forest'] = pickle.load(f)
    return models

models = load_models()

# ── Sidebar : choix du modèle ─────────────────────────────
st.sidebar.header("⚙️ Configuration")
modele_choisi = st.sidebar.selectbox(
    "Choisir le modèle de prédiction",
    list(models.keys())
)

seuil = st.sidebar.slider(
    "Seuil de détection", 0.0, 1.0, 0.5, 0.01,
    help="Au-dessus de ce seuil, la transaction est classée comme fraude"
)

# ── Formulaire de saisie ───────────────────────────────────
section_header("📝", "Caractéristiques de la transaction")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Informations générales**")
    amount = st.number_input("Montant (€)", 0.0, 30000.0, 100.0, 0.01)
    time   = st.number_input("Time (secondes)", 0, 172800, 50000)

with col2:
    st.markdown("**Features les plus discriminantes**")
    v14 = st.slider("V14", -20.0, 20.0, 0.0, 0.1)
    v10 = st.slider("V10", -20.0, 20.0, 0.0, 0.1)
    v4  = st.slider("V4",  -20.0, 20.0, 0.0, 0.1)
    v17 = st.slider("V17", -20.0, 20.0, 0.0, 0.1)

with col3:
    st.markdown("**Autres features importantes**")
    v12 = st.slider("V12", -20.0, 20.0, 0.0, 0.1)
    v11 = st.slider("V11", -20.0, 20.0, 0.0, 0.1)
    v3  = st.slider("V3",  -20.0, 20.0, 0.0, 0.1)
    v16 = st.slider("V16", -20.0, 20.0, 0.0, 0.1)

# ── Bouton de prédiction ───────────────────────────────────
if st.button("🔍 Analyser la transaction", type="primary",
             use_container_width=True):

    # Construction du vecteur de features (30 features)
    features = np.zeros(30)
    features[0]  = time
    features[1]  = 0      # V1
    features[2]  = 0      # V2
    features[3]  = v3
    features[4]  = v4
    features[10] = v10
    features[11] = v11
    features[12] = v12
    features[13] = v14
    features[15] = v16
    features[16] = v17
    features[29] = amount

    modele = models[modele_choisi]
    st.divider()
    section_header("📌", f"Résultats — {modele_choisi}")

    col_res1, col_res2 = st.columns([1, 1])

    # Prédiction selon le type de modèle
    with col_res1:
        if modele_choisi == 'Isolation Forest':
            pred_raw = modele.predict([features])[0]
            prediction = 1 if pred_raw == -1 else 0
            score = float(-modele.score_samples([features])[0])
            proba = min(score / 0.5, 1.0)
        else:
            prediction = modele.predict([features])[0]
            proba = modele.predict_proba([features])[0][1]

        # Application du seuil
        if modele_choisi != 'Isolation Forest':
            prediction = 1 if proba >= seuil else 0

        if prediction == 1:
            st.markdown(
                '<div class="result-banner result-fraud">🚨 Transaction FRAUDULEUSE détectée !</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="result-banner result-legit">✅ Transaction LÉGITIME</div>',
                unsafe_allow_html=True,
            )

        st.metric("Probabilité de fraude", f"{proba*100:.2f}%")
        st.metric("Modèle utilisé", modele_choisi)
        st.metric("Seuil appliqué", f"{seuil:.2f}")

    with col_res2:
        # Jauge de risque
        couleur = "#C0625B" if proba > seuil else "#3E7A3E"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=proba * 100,
            title={'text': "Niveau de risque (%)"},
            delta={'reference': seuil * 100,
                   'increasing': {'color': "#C0625B"},
                   'decreasing': {'color': "#3E7A3E"}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': couleur},
                'steps': [
                    {'range': [0, 30],  'color': "#DCEBDC"},
                    {'range': [30, 70], 'color': "#F3E3C3"},
                    {'range': [70, 100],'color': "#F0D4D1"}
                ],
                'threshold': {
                    'line': {'color': "#3E2723", 'width': 3},
                    'thickness': 0.8,
                    'value': seuil * 100
                }
            }
        ))
        fig_gauge.update_layout(height=300, paper_bgcolor="#FBF7F2",
                                 font_color="#3E2723")
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Détail de la décision
    st.divider()
    section_header("📊", "Détail de la décision")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    col_d1.metric("Montant", f"{amount:.2f} €")
    col_d2.metric("V14 (feature clé)", f"{v14:.2f}")
    col_d3.metric("V10", f"{v10:.2f}")
    col_d4.metric("V17", f"{v17:.2f}")