import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

st.set_page_config(page_title="Prédiction", page_icon="🔍", layout="wide")
st.title("🔍 Prédiction en temps réel")
st.markdown("Saisissez les caractéristiques d'une transaction pour prédire si elle est frauduleuse.")

# ── Chargement des modèles ─────────────────────────────────
@st.cache_resource
def load_models():
    models = {}
    with open('models/logistic_regression.pkl', 'rb') as f:
        models['Régression Logistique'] = pickle.load(f)
    with open('models/random_forest.pkl', 'rb') as f:
        models['Random Forest'] = pickle.load(f)
    with open('models/xgboost.pkl', 'rb') as f:
        models['XGBoost'] = pickle.load(f)
    with open('models/isolation_forest.pkl', 'rb') as f:
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
st.subheader("📝 Caractéristiques de la transaction")

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
    st.subheader(f"Résultats — {modele_choisi}")

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
            st.error("🚨 Transaction FRAUDULEUSE détectée !")
        else:
            st.success("✅ Transaction LÉGITIME")

        st.metric("Probabilité de fraude", f"{proba*100:.2f}%")
        st.metric("Modèle utilisé", modele_choisi)
        st.metric("Seuil appliqué", f"{seuil:.2f}")

    with col_res2:
        # Jauge de risque
        couleur = "red" if proba > seuil else "green"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=proba * 100,
            title={'text': "Niveau de risque (%)"},
            delta={'reference': seuil * 100,
                   'increasing': {'color': "red"},
                   'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': couleur},
                'steps': [
                    {'range': [0, 30],  'color': "#c8e6c9"},
                    {'range': [30, 70], 'color': "#fff9c4"},
                    {'range': [70, 100],'color': "#ffcdd2"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.8,
                    'value': seuil * 100
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Détail de la décision
    st.divider()
    st.subheader("📊 Détail de la décision")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    col_d1.metric("Montant", f"{amount:.2f} €")
    col_d2.metric("V14 (feature clé)", f"{v14:.2f}")
    col_d3.metric("V10", f"{v10:.2f}")
    col_d4.metric("V17", f"{v17:.2f}")