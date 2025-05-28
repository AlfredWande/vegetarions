import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from main import run_preprocessing  # ✅ Ajout pour générer les données automatiquement

# Configuration de la page
st.set_page_config(
    page_title="Analyse nutritionnelle des recettes végétariennes / vegan",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ajouter du CSS pour personnaliser le design
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(
            f"Le fichier CSS '{file_name}' est introuvable. Assurez-vous qu'il existe dans le répertoire du projet."
        )

# Chargement du fichier CSS
local_css("docs/_static/style.css")

# Style CSS personnalisé
st.markdown(
    """
    <style>
    body { background-color: white; color: black; }
    .stApp {
        background: url('https://img-3.journaldesfemmes.fr/x9Ghv5tUnuHOrOkweGUIuP2cPZU=/1240x/smart/38888207364b4e12a4058004322afa49/ccmcms-jdf/36666882.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .main-title {
        background: rgba(0, 0, 0, 0.8);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
    }
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.8) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        color: white !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] a {
        color: white !important;
    }
    [data-testid="stSidebar"] section {
        border: none !important;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chemin vers les données nettoyées
file_path = "./data/cleaned_recipes.csv"

# ✅ Générer automatiquement le fichier nettoyé si absent
if not os.path.exists(file_path):
    st.warning("Fichier nettoyé introuvable. Génération en cours...")
    run_preprocessing()
    st.success("Fichier nettoyé généré avec succès.")

# Charger les données
data = pd.read_csv(file_path)

# Titre principal
st.markdown(
    """
    <div class="main-title">
        <h1 style="color: white; text-align: center; font-size: 3.5em;">🌱 Analyse comparative des recettes végétariennes / véganes et des autres recettes </h1>
        <p style="color: white; text-align: center; font-size: 1.5em;">Une exploration interactive des types de recettes de cuisine.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Barre latérale
st.sidebar.header("Navigation")
menu = [
    "Accueil",
    "Objectifs de l'application",
    "Visualisations",
    "À propos"
]
choice = st.sidebar.radio("Menu", menu)

if choice == "Accueil":
    st.subheader("Bienvenue dans l'application d'analyse nutritionnelle")
    st.markdown("""
    Cette application vous permet d'explorer les différences nutritionnelles
    entre les recettes végétariennes, véganes et les autres recettes.
    """)

elif choice == "Objectifs de l'application":
    st.subheader("Objectifs de l'application")
    st.markdown("""
    - Mettre en lumière les profils nutritionnels des recettes végétariennes et véganes.
    - Comparer avec les recettes traditionnelles.
    - Fournir des visualisations simples et informatives.
    """)

elif choice == "Visualisations":
    st.subheader("Explorations graphiques")
    vis = st.selectbox("Choisissez une visualisation", [
        "Répartition des types de recettes",
        "Boxplot des calories par type",
        "Matrice de corrélation nutritionnelle"
    ])

    data["type"] = data.apply(
        lambda row: "Vegan" if row["vegan_final"] == 1 else ("Végétarienne" if row["vege"] == 1 else "Autre"),
        axis=1
    )

    if vis == "Répartition des types de recettes":
        counts = data["type"].value_counts()
        st.bar_chart(counts)

    elif vis == "Boxplot des calories par type":
        fig, ax = plt.subplots()
        sns.boxplot(x="type", y="calories", data=data, ax=ax)
        st.pyplot(fig)

    elif vis == "Matrice de corrélation nutritionnelle":
        variables = [
            "calories", "sodium (PDV%)", "protein (PDV%)",
            "total fat (PDV%)", "saturated fat (PDV%)", "carbohydrates (PDV%)"
        ]
        corr = data[variables].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

elif choice == "À propos":
    st.subheader("À propos")
    st.markdown("""
    Application développée par **Alfred Wande-Wula**.

    Technologies :
    - Python
    - Streamlit
    - Pandas / Matplotlib / Seaborn
    """)

    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <p style="color: gray; font-size: 0.9em;">Merci de visiter cette application d'analyse nutritionnelle.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
