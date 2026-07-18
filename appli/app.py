import streamlit as st

st.set_page_config(
    page_title="Détection de Fraude Bancaire",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Style CSS personnalisé ─────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1F3864;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1F3864, #2E75B6);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.85;
        margin-top: 0.3rem;
    }
    .sidebar .sidebar-content {
        background: #1F3864;
    }
</style>
""", unsafe_allow_html=True)

# ── Page d'accueil ─────────────────────────────────────────
st.markdown('<p class="main-title">🔐 Détection de Fraude Bancaire</p>',
            unsafe_allow_html=True)
st.markdown("""<p class="subtitle">
    Projet de fin d'année — Licence 2 Big Data | 2025–2026<br>
    Dataset : Credit Card Fraud Detection (ULB/Kaggle)
</p>""", unsafe_allow_html=True)

st.divider()

# ── Métriques clés ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Transactions", "284 807",
              help="Nombre total de transactions analysées")
with col2:
    st.metric("🚨 Fraudes", "492",
              help="Transactions frauduleuses dans le dataset")
with col3:
    st.metric("⚖️ Taux de fraude", "0.17%",
              help="Proportion de fraudes — fort déséquilibre")
with col4:
    st.metric("🤖 Modèles testés", "4",
              help="LR, Random Forest, XGBoost, Isolation Forest")

st.divider()

# ── Présentation du projet ─────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📋 À propos du projet")
    st.markdown("""
    Ce projet de fin d'année s'inscrit dans le cadre de la **Licence 2 Big Data**
    sous la direction du **Professeur M. Balde**. Il porte sur l'analyse de
    transactions bancaires et la détection automatique de fraudes par des
    approches de **Machine Learning**.

    **Pipeline complet mis en œuvre :**
    - 🔍 Exploration et analyse des données (EDA)
    - ⚙️ Prétraitement : normalisation, SMOTE, train/test split
    - 🤖 Modélisation : 4 algorithmes ML comparés
    - 📊 Évaluation : métriques adaptées au déséquilibre des classes
    - 🖥️ Déploiement : application Streamlit interactive
    """)

with col_right:
    st.subheader("🏆 Meilleurs résultats")
    st.markdown("""
    | Modèle | AUC-ROC | F1 |
    |---|---|---|
    | XGBoost | **0.9808** | 0.79 |
    | Random Forest | 0.9688 | **0.82** |
    | Régression Log. | 0.9698 | 0.11 |
    | Isolation Forest | 0.9536 | 0.32 |
    """)

st.divider()

# ── Navigation ─────────────────────────────────────────────
st.subheader("🧭 Navigation")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("📊 **Page EDA**\nExploration interactive\ndes données")
with col2:
    st.success("🔍 **Page Prédiction**\nAnalysez une transaction\nen temps réel")
with col3:
    st.warning("📈 **Page Comparaison**\nComparez les 4 modèles\nML entre eux")
with col4:
    st.error("ℹ️ **Utilisez le menu**\nlateral gauche pour\nnaviguer entre les pages")