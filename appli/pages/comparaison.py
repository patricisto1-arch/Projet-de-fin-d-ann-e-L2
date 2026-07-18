import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Comparaison", page_icon="📈", layout="wide")
st.title("📈 Comparaison des modèles ML")

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
st.subheader("📋 Tableau comparatif complet")
st.dataframe(
    resultats.style
    .highlight_max(subset=['Precision','Recall','F1-Score',
                           'AUC-ROC','Fraudes détectées'],
                   color='#c8e6c9')
    .highlight_min(subset=['Fausses alertes'], color='#c8e6c9')
    .highlight_min(subset=['Precision','Recall','F1-Score',
                           'AUC-ROC','Fraudes détectées'],
                   color='#ffcdd2')
    .format({'Precision':'{:.4f}','Recall':'{:.4f}',
             'F1-Score':'{:.4f}','AUC-ROC':'{:.4f}'}),
    use_container_width=True
)

st.divider()

# ── Graphiques comparatifs ─────────────────────────────────
st.subheader("📊 Visualisations comparatives")
tab1, tab2, tab3 = st.tabs(["Métriques", "Résultats opérationnels",
                              "Courbes ROC simulées"])

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
        fig_bar.update_layout(yaxis_range=[0, 1.15])
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
        st.plotly_chart(fig_fp, use_container_width=True)

with tab3:
    st.info("""Les courbes ROC simulées sont basées sur les AUC-ROC
    réels de vos modèles. Pour les courbes exactes, rechargez
    les modèles pkl et recalculez sur le test set.""")

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
        legend=dict(x=0.6, y=0.1)
    )
    st.plotly_chart(fig_roc, use_container_width=True)

st.divider()

# ── Recommandation ─────────────────────────────────────────
st.subheader("🏆 Recommandation finale")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### 🥇 XGBoost — Meilleur AUC-ROC
    - AUC-ROC : **0.9808** (le plus élevé)
    - Recall : **0.87** (85 fraudes détectées)
    - Recommandé si : **détection maximale prioritaire**
    """)

with col2:
    st.info("""
    ### 🥈 Random Forest — Meilleur F1
    - F1-Score : **0.8205** (le plus élevé)
    - Fausses alertes : **17 seulement**
    - Recommandé si : **expérience client prioritaire**
    """)