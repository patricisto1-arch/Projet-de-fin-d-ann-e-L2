import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")

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
        margin: 0.4rem 0 1rem 0;
    }
    .section-header { font-size: 1.2rem; font-weight: 700; color: var(--brown-dark); margin: 0; }

    /* Blocs pleine largeur (remplacent st.info / st.success / st.error) */
    .full-block {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        color: var(--grey);
        line-height: 1.7;
        height: 100%;
    }
    .card-gold { border-left: 6px solid var(--gold); }
    .card-brown { border-left: 6px solid var(--brown-mid); }
    .card-terracotta { border-left: 6px solid var(--terracotta); }

    /* Onglets */
    button[data-baseweb="tab"] { color: var(--brown-dark) !important; font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: var(--gold) !important;
        color: var(--brown-dark) !important;
    }

    /* Métriques natives st.metric */
    div[data-testid="stMetric"] {
        background: var(--cream);
        border: 1px solid #DDCBB8;
        border-radius: 12px;
        padding: 0.8rem;
    }
    div[data-testid="stMetric"] label { color: var(--brown) !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--brown-dark) !important; }

    /* Tableaux */
    div[data-testid="stDataFrame"] { border: 1px solid #DDCBB8; border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


def section_header(icon, text):
    st.markdown(
        f'<div class="section-header-box"><p class="section-header">{icon} {text}</p></div>',
        unsafe_allow_html=True,
    )


def note_box(text):
    st.markdown(f'<div class="note-box">{text}</div>', unsafe_allow_html=True)


CHART_BG = "#FBF7F2"
FONT_COLOR = "#3E2723"
GRID_COLOR = "#DDCBB8"


def style_fig(fig, legend=True):
    """Force explicitement la couleur des axes, graduations et titres
    (sinon le thème sombre de Streamlit impose du texte blanc, invisible
    sur fond clair)."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, size=13),
        title_font=dict(color=FONT_COLOR, size=15),
        legend=dict(font=dict(color=FONT_COLOR)) if legend else None,
        margin=dict(t=60),
    )
    fig.update_xaxes(
        color=FONT_COLOR,
        title_font=dict(color=FONT_COLOR),
        tickfont=dict(color=FONT_COLOR),
        gridcolor=GRID_COLOR,
        linecolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
    )
    fig.update_yaxes(
        color=FONT_COLOR,
        title_font=dict(color=FONT_COLOR),
        tickfont=dict(color=FONT_COLOR),
        gridcolor=GRID_COLOR,
        linecolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
    )
    return fig


st.markdown("""
<div class="hero-box">
    <p class="hero-title">📊 Exploration des données (EDA)</p>
</div>
""", unsafe_allow_html=True)

# Chemin robuste : remonte depuis EDA.py jusqu'à la racine du projet,
# peu importe d'où la commande streamlit est lancée
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "creditcard.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


df = load_data()

# ── Onglets ────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Aperçu", "⚖️ Distribution", "💰 Montants",
    "🚨 Valeurs aberrantes", "🔗 Corrélations", "🧮 Matrices de confusion"
])

# ── Tab 1 : Aperçu ─────────────────────────────────────────
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", f"{df.shape[0]:,}")
    col2.metric("Colonnes", f"{df.shape[1]}")
    col3.metric("Valeurs manquantes", "0")

    section_header("📋", "Aperçu des données")
    n = st.slider("Nombre de lignes à afficher", 5, 50, 10)
    classe = st.selectbox("Filtrer par classe",
                          ["Toutes", "Normal (0)", "Fraude (1)"])
    if classe == "Normal (0)":
        st.dataframe(df[df['Class']==0].head(n),
                     use_container_width=True)
    elif classe == "Fraude (1)":
        st.dataframe(df[df['Class']==1].head(n),
                     use_container_width=True)
    else:
        st.dataframe(df.head(n), use_container_width=True)

    section_header("📈", "Statistiques descriptives")
    st.dataframe(df.describe().round(4), use_container_width=True)

# ── Tab 2 : Distribution des classes ──────────────────────
with tab2:
    section_header("⚖️", "Distribution des classes")
    col1, col2 = st.columns(2)

    counts = df['Class'].value_counts()

    with col1:
        fig_bar = px.bar(
            x=['Normal (0)', 'Fraude (1)'],
            y=[counts[0], counts[1]],
            color=['Normal', 'Fraude'],
            color_discrete_map={'Normal':'#2196F3','Fraude':'#F44336'},
            title='Nombre de transactions par classe',
            text=[f'{counts[0]:,}', f'{counts[1]:,}'],
            labels={'x':'Classe','y':'Nombre'}
        )
        fig_bar.update_traces(textposition='outside', textfont_color=FONT_COLOR)
        fig_bar.update_layout(showlegend=False)
        style_fig(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            values=[counts[0], counts[1]],
            names=['Normal (99.83%)', 'Fraude (0.17%)'],
            color_discrete_sequence=['#2196F3','#F44336'],
            title='Proportion des classes',
            hole=0.4
        )
        fig_pie.update_traces(pull=[0, 0.1], textfont_color="#FFFFFF")
        style_fig(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(f"""
    <div class="full-block card-brown">
        <b>Déséquilibre des classes :</b>
        <ul>
            <li>Transactions normales : <b>{counts[0]:,} (99.83%)</b></li>
            <li>Transactions frauduleuses : <b>{counts[1]:,} (0.17%)</b></li>
            <li>Ratio : 1 fraude pour <b>{counts[0]//counts[1]} transactions normales</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ── Tab 3 : Distribution des montants ──────────────────────
with tab3:
    section_header("💰", "Distribution des montants par classe")

    fig_amount = make_subplots(rows=1, cols=2,
        subplot_titles=('Transactions normales', 'Transactions frauduleuses'))

    fig_amount.add_trace(
        go.Histogram(x=df[df['Class']==0]['Amount'],
                     nbinsx=50, name='Normal',
                     marker_color='#2196F3', opacity=0.8),
        row=1, col=1)
    fig_amount.add_trace(
        go.Histogram(x=df[df['Class']==1]['Amount'],
                     nbinsx=50, name='Fraude',
                     marker_color='#F44336', opacity=0.8),
        row=1, col=2)

    fig_amount.update_layout(height=400, showlegend=False,
                              title_text='Distribution des montants')
    style_fig(fig_amount)
    fig_amount.update_annotations(font_color=FONT_COLOR)
    st.plotly_chart(fig_amount, use_container_width=True)

    # Statistiques comparatives
    section_header("📊", "Statistiques comparatives — Amount")
    stats = df.groupby('Class')['Amount'].describe().round(2)
    stats.index = ['Normal (0)', 'Fraude (1)']
    st.dataframe(stats, use_container_width=True)

    # Distribution temporelle
    section_header("🕒", "Distribution temporelle")
    fig_time = make_subplots(rows=1, cols=2,
        subplot_titles=('Normal', 'Fraude'))
    fig_time.add_trace(
        go.Histogram(x=df[df['Class']==0]['Time'],
                     nbinsx=50, marker_color='#2196F3', opacity=0.8),
        row=1, col=1)
    fig_time.add_trace(
        go.Histogram(x=df[df['Class']==1]['Time'],
                     nbinsx=50, marker_color='#F44336', opacity=0.8),
        row=1, col=2)
    fig_time.update_layout(height=400, showlegend=False)
    style_fig(fig_time)
    fig_time.update_annotations(font_color=FONT_COLOR)
    st.plotly_chart(fig_time, use_container_width=True)

# ── Tab 4 : Valeurs aberrantes (outliers) ──────────────────
with tab4:
    section_header("🚨", "Détection des valeurs aberrantes (méthode IQR)")

    st.markdown("""
    <div class="full-block card-brown">
    La méthode de l'écart interquartile (<b>IQR</b>) considère comme aberrante toute valeur
    en dehors de l'intervalle <b>[Q1 − 1,5×IQR ; Q3 + 1,5×IQR]</b>, où IQR = Q3 − Q1.
    Cette analyse est appliquée séparément sur les transactions normales et frauduleuses,
    afin de vérifier si les valeurs jugées "aberrantes" sont en réalité le signe d'un
    comportement frauduleux plutôt qu'une erreur de saisie.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    features_outliers = st.multiselect(
        "Variables à analyser",
        ['Amount', 'Time', 'V14', 'V17', 'V12', 'V10', 'V16', 'V4', 'V11'],
        default=['Amount', 'V14', 'V17', 'V12']
    )

    def iqr_bounds(series):
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        return q1 - 1.5 * iqr, q3 + 1.5 * iqr

    if features_outliers:
        rows = []
        for feat in features_outliers:
            for cls, label in [(0, 'Normal'), (1, 'Fraude')]:
                serie = df[df['Class'] == cls][feat]
                low, high = iqr_bounds(serie)
                n_out = ((serie < low) | (serie > high)).sum()
                pct = 100 * n_out / len(serie)
                rows.append({
                    'Variable': feat, 'Classe': label,
                    'Borne basse': round(low, 2), 'Borne haute': round(high, 2),
                    'Valeurs aberrantes': int(n_out),
                    '% de la classe': f"{pct:.2f} %",
                })
        outlier_df = pd.DataFrame(rows)

        section_header("📋", "Récapitulatif des valeurs aberrantes")
        st.dataframe(outlier_df, use_container_width=True, hide_index=True)

        total_normal_out = outlier_df[outlier_df['Classe'] == 'Normal']['Valeurs aberrantes'].sum()
        total_fraude_out = outlier_df[outlier_df['Classe'] == 'Fraude']['Valeurs aberrantes'].sum()
        pct_fraude_out = 100 * total_fraude_out / (len(features_outliers) * (df['Class'] == 1).sum())
        pct_normal_out = 100 * total_normal_out / (len(features_outliers) * (df['Class'] == 0).sum())

        st.markdown(f"""
        <div class="full-block card-gold">
            <b>Observation clé :</b> en moyenne sur les variables sélectionnées,
            <b>{pct_fraude_out:.1f} %</b> des valeurs côté Fraude sont détectées comme
            aberrantes par la méthode IQR, contre seulement <b>{pct_normal_out:.1f} %</b>
            côté Normal. Ce déséquilibre confirme que les "outliers" ne sont pas de simples
            erreurs de saisie : ils concentrent une grande partie du signal discriminant
            utilisé par les modèles (cohérent avec l'importance de V14, V17, V12, V10
            observée en section Corrélations et en modélisation).
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        section_header("📦", "Boxplots par variable et par classe")
        for feat in features_outliers:
            fig_box = px.box(
                df, x='Class', y=feat, color='Class',
                color_discrete_map={0: '#2196F3', 1: '#F44336'},
                points='outliers',
                title=f"Distribution de {feat} — Normal (0) vs Fraude (1)",
                labels={'Class': 'Classe'},
            )
            fig_box.update_layout(showlegend=False)
            style_fig(fig_box)
            st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.markdown(
            '<div class="full-block card-brown">Sélectionne au moins une variable pour lancer l\'analyse.</div>',
            unsafe_allow_html=True,
        )

# ── Tab 5 : Corrélations ───────────────────────────────────
with tab5:
    section_header("🔗", "Corrélation des features avec Class")

    correlations = df.corr()['Class'].drop('Class').sort_values()
    colors = ['#F44336' if x < 0 else '#2196F3' for x in correlations]

    fig_corr = go.Figure(go.Bar(
        x=correlations.values,
        y=correlations.index,
        orientation='h',
        marker_color=colors
    ))
    fig_corr.add_vline(x=0, line_dash="dash", line_color=FONT_COLOR,
                        line_width=1)
    fig_corr.update_layout(
        title='Corrélation des features avec la variable Class',
        height=600,
        xaxis_title='Coefficient de corrélation',
        yaxis_title='Feature',
    )
    style_fig(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        top_pos = correlations.tail(5)[::-1]
        items = "".join(f"<li><b>{feat}</b> : {val:.4f}</li>" for feat, val in top_pos.items())
        st.markdown(f"""
        <div class="full-block card-gold">
            <b>Top 5 corrélations positives</b>
            <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        top_neg = correlations.head(5)
        items = "".join(f"<li><b>{feat}</b> : {val:.4f}</li>" for feat, val in top_neg.items())
        st.markdown(f"""
        <div class="full-block card-terracotta">
            <b>Top 5 corrélations négatives</b>
            <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)

# ── Tab 6 : Matrices de confusion ──────────────────────────
with tab6:
    section_header("🧮", "Matrices de confusion par modèle")

    st.markdown("""
    <div class="full-block card-brown">
    Résultats obtenus sur l'ensemble de test (56 962 transactions : 56 864 normales,
    98 frauduleuses), identiques à ceux détaillés au chapitre 5 du rapport et à la
    page Comparaison.
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    # Chiffres réels (cohérents avec la page Comparaison et le rapport, section 5.2/5.4)
    conf_data = {
        'Régression Logistique': {'TN': 55406, 'FP': 1458, 'FN': 8,  'TP': 90,
                                   'Precision': 0.06, 'Recall': 0.92, 'F1': 0.11, 'AUC': 0.9698},
        'Random Forest':         {'TN': 56847, 'FP': 17,   'FN': 18, 'TP': 80,
                                   'Precision': 0.82, 'Recall': 0.82, 'F1': 0.8205, 'AUC': 0.9688},
        'XGBoost':                {'TN': 56831, 'FP': 33,   'FN': 13, 'TP': 85,
                                   'Precision': 0.72, 'Recall': 0.87, 'F1': 0.79, 'AUC': 0.9808},
        'Isolation Forest':       {'TN': 56791, 'FP': 73,   'FN': 66, 'TP': 32,
                                   'Precision': 0.30, 'Recall': 0.33, 'F1': 0.3153, 'AUC': 0.9536},
    }

    modele_sel = st.selectbox("Choisir un modèle", list(conf_data.keys()), key="conf_matrix_model")
    d = conf_data[modele_sel]

    col_a, col_b = st.columns([1, 1])

    with col_a:
        z = [[d['TN'], d['FP']], [d['FN'], d['TP']]]
        fig_cm = go.Figure(data=go.Heatmap(
            z=z,
            x=['Prédit : Normal', 'Prédit : Fraude'],
            y=['Réel : Normal', 'Réel : Fraude'],
            colorscale=[[0, '#FBF7F2'], [1, '#D9A441']],
            text=z,
            texttemplate="%{text:,}",
            textfont={"size": 18, "color": "#3E2723"},
            showscale=False,
        ))
        fig_cm.update_layout(title=f"Matrice de confusion — {modele_sel}", height=420)
        fig_cm.update_yaxes(autorange="reversed")
        style_fig(fig_cm, legend=False)
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_b:
        st.metric("Precision (Fraude)", f"{d['Precision']:.2f}")
        st.metric("Recall (Fraude)", f"{d['Recall']:.2f}")
        st.metric("F1-Score (Fraude)", f"{d['F1']:.4f}")
        st.metric("AUC-ROC", f"{d['AUC']:.4f}")
        st.markdown(f"""
        <div class="full-block card-gold" style="margin-top:0.8rem;">
            <b>Lecture rapide :</b>
            <ul>
                <li><b>{d['TP']}</b> fraudes détectées sur 98</li>
                <li><b>{d['FN']}</b> fraudes manquées (faux négatifs)</li>
                <li><b>{d['FP']}</b> fausses alertes (faux positifs)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)