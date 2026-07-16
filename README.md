# Détection de Fraude Bancaire par Machine Learning

Projet de fin d'année — Dakar Institute of Technology (DIT)
Département Informatique & Science des Données — Année académique 2024/2025

## Description

Ce projet consiste à analyser des transactions bancaires afin de détecter automatiquement les opérations frauduleuses, à partir du dataset public **Credit Card Fraud Detection** (ULB/Kaggle). Il couvre l'ensemble du pipeline : exploration des données, prétraitement, gestion du déséquilibre des classes, modélisation et évaluation comparative de plusieurs algorithmes de Machine Learning.

## Auteurs

- Patrice DIONE
- Mame Faty DIENG

## Dataset

Le dataset utilisé est le **Credit Card Fraud Detection dataset** disponible sur [Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud) :
- 284 807 transactions de cartes bancaires européennes (septembre 2013)
- 492 transactions frauduleuses (~0,17 %)
- 30 variables : `Time`, `Amount`, `V1` à `V28` (composantes issues d'une ACP pour préserver la confidentialité)
- Variable cible : `Class` (0 = transaction normale, 1 = fraude)

> Le fichier `creditcard.csv` n'est pas versionné dans ce repo (voir `.gitignore`) en raison de sa taille. Télécharge-le depuis Kaggle et place-le dans `data/creditcard.csv` avant d'exécuter le notebook.

## Structure du projet

```
detection-fraude-DIT/
├── notebooks/
│   └── notebook_PF.ipynb      # Pipeline complet : EDA, prétraitement, modélisation
├── data/                      # Dataset (non versionné, à ajouter localement)
├── requirements.txt           # Dépendances Python
├── .gitignore
└── README.md
```

## Méthodologie

Le projet suit une démarche structurée en plusieurs étapes :

1. **Analyse exploratoire (EDA)** — statistiques descriptives, visualisations, analyse du déséquilibre des classes
2. **Prétraitement** — nettoyage, normalisation (RobustScaler), traitement des outliers (IQR)
3. **Gestion du déséquilibre** — SMOTE appliqué uniquement sur l'ensemble d'entraînement (anti data-leakage)
4. **Modélisation** — comparaison de 4 algorithmes :
   - Régression Logistique (baseline)
   - Random Forest
   - XGBoost
   - Isolation Forest (détection d'anomalies non supervisée)
5. **Évaluation** — Precision, Recall, F1-Score, AUC-ROC, matrices de confusion, courbes ROC / Precision-Recall

## Installation

```bash
git clone https://github.com/<ton-compte>/detection-fraude-DIT.git
cd detection-fraude-DIT
pip install -r requirements.txt
```

Puis lance Jupyter :

```bash
jupyter notebook notebooks/notebook_PF.ipynb
```

## Résultats

*À compléter une fois l'évaluation finale des modèles réalisée.*

| Modèle | Precision | Recall | F1-Score | AUC-ROC |
|---|---|---|---|---|
| Régression Logistique | — | — | — | — |
| Random Forest | — | — | — | — |
| XGBoost | — | — | — | — |
| Isolation Forest | — | — | — | — |

## Licence

Projet académique — DIT, à usage pédagogique.
