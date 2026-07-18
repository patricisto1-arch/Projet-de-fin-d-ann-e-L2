import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("📊 Exploration des données (EDA)")

@st.cache_data
def load_data():
    df = pd.read_csv('data/creditcard.csv')
    return df

df = load_data()

# ── Onglets ────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Aperçu", "⚖️ Distribution", "💰 Montants", "🔗 Corrélations"
])

# ── Tab 1 : Aperçu ─────────────────────────────────────────
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", f"{df.shape[0]:,}")
    col2.metric("Colonnes", f"{df.shape[1]}")
    col3.metric("Valeurs manquantes", "0")

    st.subheader("Aperçu des données")
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

    st.subheader("Statistiques descriptives")
    st.dataframe(df.describe().round(4), use_container_width=True)

# ── Tab 2 : Distribution des classes ──────────────────────
with tab2:
    st.subheader("Distribution des classes")
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
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            values=[counts[0], counts[1]],
            names=['Normal (99.83%)', 'Fraude (0.17%)'],
            color_discrete_sequence=['#2196F3','#F44336'],
            title='Proportion des classes',
            hole=0.4
        )
        fig_pie.update_traces(pull=[0, 0.1])
        st.plotly_chart(fig_pie, use_container_width=True)

    st.info(f"""
    **Déséquilibre des classes :**
    - Transactions normales : **{counts[0]:,} (99.83%)**
    - Transactions frauduleuses : **{counts[1]:,} (0.17%)**
    - Ratio : 1 fraude pour **{counts[0]//counts[1]} transactions normales**
    """)

# ── Tab 3 : Distribution des montants ──────────────────────
with tab3:
    st.subheader("Distribution des montants par classe")

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
    st.plotly_chart(fig_amount, use_container_width=True)

    # Statistiques comparatives
    st.subheader("Statistiques comparatives — Amount")
    stats = df.groupby('Class')['Amount'].describe().round(2)
    stats.index = ['Normal (0)', 'Fraude (1)']
    st.dataframe(stats, use_container_width=True)

    # Distribution temporelle
    st.subheader("Distribution temporelle")
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
    st.plotly_chart(fig_time, use_container_width=True)

# ── Tab 4 : Corrélations ───────────────────────────────────
with tab4:
    st.subheader("Corrélation des features avec Class")

    correlations = df.corr()['Class'].drop('Class').sort_values()
    colors = ['#F44336' if x < 0 else '#2196F3' for x in correlations]

    fig_corr = go.Figure(go.Bar(
        x=correlations.values,
        y=correlations.index,
        orientation='h',
        marker_color=colors
    ))
    fig_corr.add_vline(x=0, line_dash="dash", line_color="black",
                        line_width=1)
    fig_corr.update_layout(
        title='Corrélation des features avec la variable Class',
        height=600,
        xaxis_title='Coefficient de corrélation',
        yaxis_title='Feature'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.success("**Top 5 corrélations positives**")
        top_pos = correlations.tail(5)[::-1]
        for feat, val in top_pos.items():
            st.write(f"• **{feat}** : {val:.4f}")
    with col2:
        st.error("**Top 5 corrélations négatives**")
        top_neg = correlations.head(5)
        for feat, val in top_neg.items():
            st.write(f"• **{feat}** : {val:.4f}")