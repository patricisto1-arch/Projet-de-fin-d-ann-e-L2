import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Comparaison", page_icon="📈", layout="wide")

# ─────────────────────────────────────────────────────────────
# STYLE CSS PERSONNALISÉ — même thème marron deux tons que l'accueil
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

    /* Titres de section : toujours encadrés, donc toujours lisibles */
    .section-header-box {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-left: 6px solid var(--gold);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0 0 1rem 0;
    }
    .section-header { font-size: 1.3rem; font-weight: 700; color: var(--brown-dark); margin: 0; }

    .section-spacer { height: 2rem; }

    /* Blocs pleine largeur */
    .full-block {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        color: var(--grey);
        line-height: 1.7;
        height: 100%;
    }
    .full-block h4 { margin-top: 0; color: var(--brown-dark); }
    .card-gold { border-left: 6px solid var(--gold); }
    .card-brown { border-left: 6px solid var(--brown-mid); }

    /* Onglets */
    button[data-baseweb="tab"] { color: var(--brown-dark) !important; font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: var(--gold) !important;
        color: var(--brown-dark) !important;
    }

    /* Tableau */
    div[data-testid="stDataFrame"] { border: 1px solid #DDCBB8; border-radius: 10px; overflow: hidden; }
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


st.markdown("""
<div class="hero-box">
    <p class="hero-title">📈 Comparaison des modèles ML</p>
</div>
""", unsafe_allow_html=True)

# ── Données des résultats ──────────────────────────────────
resultats = pd.DataFrame({
    'Modèle'    : ['Régression Logistique', 'Random Forest',
                   'XGBoost', 'Isolation Forest'],
    'Precision' : [0.06, 0.82, 0.72, 0.30],
    'Recall'    : [0.92, 0.82, 0.87, 0.33],
    'F1-Score'  : [0.11, 0.8205, 0.79, 0.3153],
    'AUC-ROC'   : [0.9698, 0.9688, 0.9808, 0.9536],
    'Fraudes détectées' : [90, 80, 85, 32],
    'Fausses alertes'   : [1458, 17, 33, 73],
    'Type'      : ['Supervisé', 'Supervisé',
                   'Supervisé', 'Non supervisé'],
})

# ── Tableau comparatif ─────────────────────────────────────
section_header("📋", "Tableau comparatif complet")
st.dataframe(
    resultats.style
    .highlight_max(subset=['Precision','Recall','F1-Score',
                           'AUC-ROC','Fraudes détectées'],
                   color='#D9A441')
    .highlight_min(subset=['Fausses alertes'], color='#D9A441')
    .highlight_min(subset=['Precision','Recall','F1-Score',
                           'AUC-ROC','Fraudes détectées'],
                   color='#E8B4AE')
    .highlight_max(subset=['Fausses alertes'], color='#E8B4AE')
    .format({'Precision':'{:.4f}','Recall':'{:.4f}',
             'F1-Score':'{:.4f}','AUC-ROC':'{:.4f}'}),
    use_container_width=True
)
note_box("🟨 Doré = meilleure valeur de la colonne · 🟥 Rosé = valeur la moins favorable")

spacer()

# ── Graphiques comparatifs ─────────────────────────────────
section_header("📊", "Visualisations comparatives")
tab1, tab2, tab3 = st.tabs(["Métriques", "Résultats opérationnels",
                              "Courbes ROC simulées"])

CHART_BG = "#FBF7F2"

with tab1:
    metriques_sel = st.multiselect(
        "Choisir les métriques à afficher",
        ['Precision', 'Recall', 'F1-Score', 'AUC-ROC'],
        default=['Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    )
    if metriques_sel:
        df_melt = resultats.melt(
            id_vars='Modèle',
            value_vars=metriques_sel,
            var_name='Métrique',
            value_name='Score'
        )
        fig_bar = px.bar(
            df_melt, x='Modèle', y='Score',
            color='Métrique', barmode='group',
            title='Comparaison des métriques par modèle',
            color_discrete_sequence=['#2196F3','#4CAF50',
                                      '#F44336','#FF9800'],
            text_auto='.3f'
        )
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(yaxis_range=[0, 1.15],
                               paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                               font_color="#3E2723")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig_det = px.bar(
            resultats, x='Modèle',
            y='Fraudes détectées',
            color='Modèle', title='Fraudes détectées / 98',
            text='Fraudes détectées',
            color_discrete_sequence=['#9C27B0','#2196F3',
                                      '#F44336','#FF9800']
        )
        fig_det.add_hline(y=98, line_dash="dash",
                           line_color="black",
                           annotation_text="Total fraudes = 98")
        fig_det.update_traces(textposition='outside')
        fig_det.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                               font_color="#3E2723")
        st.plotly_chart(fig_det, use_container_width=True)

    with col2:
        fig_fp = px.bar(
            resultats, x='Modèle',
            y='Fausses alertes',
            color='Modèle', title='Fausses alertes (FP)',
            text='Fausses alertes',
            color_discrete_sequence=['#9C27B0','#2196F3',
                                      '#F44336','#FF9800']
        )
        fig_fp.update_traces(textposition='outside')
        fig_fp.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                              font_color="#3E2723")
        st.plotly_chart(fig_fp, use_container_width=True)

with tab3:
    st.markdown("""
    <div class="full-block card-brown">
    Les courbes ROC simulées sont basées sur les AUC-ROC réels de vos modèles.
    Pour les courbes exactes, rechargez les modèles pkl et recalculez sur le test set.
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    fig_roc = go.Figure()
    couleurs = ['#9C27B0', '#2196F3', '#F44336', '#FF9800']

    for i, row in resultats.iterrows():
        auc = row['AUC-ROC']
        # Courbe ROC approximée à partir de l'AUC
        fpr = np.linspace(0, 1, 100)
        tpr = np.power(fpr, (1-auc)/auc)
        tpr = np.clip(tpr, 0, 1)

        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr,
            name=f"{row['Modèle']} (AUC={auc:.4f})",
            line=dict(color=couleurs[i], width=2.5)
        ))

    fig_roc.add_trace(go.Scatter(
        x=[0,1], y=[0,1],
        name='Aléatoire (AUC=0.5)',
        line=dict(color='gray', dash='dash', width=1)
    ))

    fig_roc.update_layout(
        title='Courbes ROC — Comparaison des 4 modèles',
        xaxis_title='Taux de faux positifs (FPR)',
        yaxis_title='Taux de vrais positifs (TPR)',
        height=500,
        legend=dict(x=0.6, y=0.1),
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        font_color="#3E2723",
    )
    st.plotly_chart(fig_roc, use_container_width=True)

spacer()

# ── Recommandation ─────────────────────────────────────────
section_header("🏆", "Recommandation finale")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="full-block card-gold">
        <h4>🥇 XGBoost — Meilleur AUC-ROC</h4>
        <ul>
            <li>AUC-ROC : <b>0,9808</b> (le plus élevé)</li>
            <li>Recall : <b>0,87</b> (85 fraudes détectées)</li>
            <li>Recommandé si : <b>détection maximale prioritaire</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="full-block card-brown">
        <h4>🥈 Random Forest — Meilleur F1</h4>
        <ul>
            <li>F1-Score : <b>0,8205</b> (le plus élevé)</li>
            <li>Fausses alertes : <b>17 seulement</b></li>
            <li>Recommandé si : <b>expérience client prioritaire</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)