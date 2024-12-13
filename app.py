import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Analyse nutrionnelles des recettes végétariennes / vegan",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajouter du CSS pour personnaliser le design
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Le fichier CSS '{file_name}' est introuvable. Assurez-vous qu'il existe dans le répertoire du projet.")

# Chargement du fichier CSS (assurez-vous qu'il existe dans votre projet)
local_css("style.css")

# CSS pour changer le fond de l'application en noir et les écrits en blanc
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: black;
    }
    .stApp {
        background: url('https://img-3.journaldesfemmes.fr/x9Ghv5tUnuHOrOkweGUIuP2cPZU=/1240x/smart/38888207364b4e12a4058004322afa49/ccmcms-jdf/36666882.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .main-title {
        background: rgba(0, 0, 0, 0.8); /* Change background to semi-transparent black */
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white; /* Change text color to white */
    }
    .content {
        background: rgba(0, 0, 0, 0.6); /* Change background to semi-transparent black */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white; /* Change text color to white */
    }
  .css-1d391kg {  
        background-color: black !important; /* Change la couleur de fond de la sidebar */
        color: white !important; /* Change la couleur du texte de la sidebar */
    }
    .css-1v3fvcr, .css-1v3fvcr span {  
        color: white !important; /* Change également la couleur des sous-titres ou du texte de menu */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Charger les données pour visualisation
file_path = "./data/cleaned_recipes.csv"
data = pd.read_csv(file_path)

# Titre principal avec un fond visuel
st.markdown(
    """
    <div class="main-title">
        <h1 style="color: white; text-align: center; font-size: 3.5em;">🌱 Analyse des Recettes Végétariennes</h1>
        <p style="color: white; text-align: center; font-size: 1.5em;">Une exploration interactive des recettes végétariennes et de leurs bienfaits nutritionnels.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Menu latéral stylisé
st.sidebar.header("Navigation")
st.sidebar.markdown("Choisissez ce que vous souhaitez explorer :")

menu_options = [
    "Accueil",
    "Objectifs de l'application",
    "Visualisations",
    "Exploration Interactive",
    "À propos"
]
selected_option = st.sidebar.radio("Sections", menu_options)

# Section Accueil
if selected_option == "Accueil":
    st.subheader("Bienvenue sur l'application d'analyse des recettes végétariennes !")
    st.markdown(
        """
        <div class="content">
        Cette application permet de d'observer quelques tendances nutritionnelles dans les recettes végétariennes / vegan..
        - Explorer les différences entre recettes végétariennes / vegan et les autres recettes.

        Utilisez le menu à gauche pour en savoir plus !
        </div>
        """,
        unsafe_allow_html=True
    )

# Section Objectifs de l'application
if selected_option == "Objectifs de l'application":
    st.subheader("Objectifs de l'application")
    st.markdown(
        """
        <div class="content">
        ### Nos objectifs :
        - **Analyser les variables nutritionnelles** : Découvrez comment les nutriments varient entre les types de recettes.
        - **Fournir une interface intuitive** : Naviguez facilement à travers les analyses et visualisations.

        Nous espérons que cette application sera une ressource utile pour les amateurs de cuisine saine.
        </div>
        """,
        unsafe_allow_html=True
    )

# Section Visualisations
if selected_option == "Visualisations":
    st.subheader("Visualisations des Données")
    st.markdown("Sélectionnez le graphique que vous souhaitez afficher :")

    # Options de visualisation
    vis_options = [
        "Répartition des Recettes",
        "Diagramme en Barres des Types de Recettes",
        "Statistiques descriptives",
        "Boxplots des Variables Nutritionnelles",
        "Comparaison par Type de Recette Végétarienne",
        "Recette Végane",
        "Comparaison des Calories par Type de Recette",
        "Comparaison des Protéines par Type de Recette",
        "Comparaison de la Complexité des Recettes",
        "Comparaison Séparée de la Complexité des Recettes",
        "Matrice de Corrélation des Variables Sélectionnées"
    ]
    selected_vis = st.radio("Graphiques", vis_options)

    # Affichage des visualisations en fonction de la sélection
    if selected_vis == "Répartition des Recettes":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique montre la répartition des recettes végétariennes et non-végétariennes. Les pourcentages indiquent la proportion de chaque type de recette.
            </div>
            """,
            unsafe_allow_html=True
        )
        num_vegetarian = data[data['vege'] == 1].shape[0]
        num_vegan = data[data['vegan_final'] == 1].shape[0]
        num_non_vegetarian = data[data['vege'] == 0].shape[0]

        total = num_vegetarian + num_non_vegetarian
        vegetarian_vs_other = [num_vegetarian, num_non_vegetarian]
        vegetarian_vs_other_labels = ['Végétariennes', 'Non Végétariennes']
        vegetarian_vs_other_percentages = [(count / total) * 100 for count in vegetarian_vs_other]

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(vegetarian_vs_other_percentages, labels=vegetarian_vs_other_labels, autopct="%.1f%%", startangle=90, colors=["#66b3ff", "#99ff99"])
        ax.set_title("Répartition des recettes (Végétariennes vs Non Végétariennes)")
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Diagramme en Barres des Types de Recettes":
        st.subheader("Diagramme en Barres des Types de Recettes")
        recipe_counts = data['recipe_type'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=recipe_counts.index, y=recipe_counts.values, ax=ax)
        ax.set_title("Nombre de Recettes par Type")
        ax.set_xlabel("Type de Recette")
        ax.set_ylabel("Nombre de Recettes")
        st.pyplot(fig)

    elif selected_vis == "Statistiques Descriptives":
        st.subheader("Statistiques Descriptives")
        st.write(data.describe())


    elif selected_vis == "Boxplots des Variables Nutritionnelles":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique montre la distribution des différentes variables nutritionnelles. Les boxplots permettent de visualiser la médiane, les quartiles et les valeurs extrêmes pour chaque variable.
            </div>
            """,
            unsafe_allow_html=True
        )
        variables = [
            "calories",
            "sodium (PDV%)",
            "protein (PDV%)",
            "total fat (PDV%)",
            "saturated fat (PDV%)",
            "carbohydrates (PDV%)",
        ]
        df_melted = data[variables].melt(var_name="Variable", value_name="Valeur")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(x="Variable", y="Valeur", data=df_melted, palette="Set2", ax=ax)
        ax.set_title("Boxplots regroupés des Variables Nutritionnelles")
        ax.set_xlabel("Variables")
        ax.set_ylabel("Valeurs")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Boxplots par Type de Recette Végétarienne":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique compare les variables nutritionnelles entre les recettes végétariennes et non-végétariennes. Les boxplots montrent les différences de distribution pour chaque variable.
            </div>
            """,
            unsafe_allow_html=True
        )
        variables = ["calories", "sodium (PDV%)", "protein (PDV%)"]
        fig, axes = plt.subplots(1, 3, figsize=(9, 3))
        for i, var in enumerate(variables):
            sns.boxplot(x="vege", y=var, data=data, palette="Set2", ax=axes[i])
            axes[i].set_title(f"{var}")
            axes[i].set_xlabel("(0 = Non-Végétarienne, 1 = Végétarienne)")
            axes[i].set_ylabel(var)
            axes[i].grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Boxplots par Type de Recette Végane":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique compare les variables nutritionnelles entre les recettes véganes et non-véganes. Les boxplots montrent les différences de distribution pour chaque variable.
            </div>
            """,
            unsafe_allow_html=True
        )
        variables = ["calories", "sodium (PDV%)", "protein (PDV%)"]
        fig, axes = plt.subplots(1, 3, figsize=(9, 3))
        for i, var in enumerate(variables):
            sns.boxplot(x="vegan_final", y=var, data=data, palette="Set2", ax=axes[i])
            axes[i].set_title(f"{var}")
            axes[i].set_xlabel("(0 = Non-Vegan, 1 = Vegan)")
            axes[i].set_ylabel(var)
            axes[i].grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Comparaison des Calories par Type de Recette":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique compare les calories entre les différents types de recettes (végétariennes, véganes et autres). Les boxplots montrent la distribution des calories pour chaque type de recette.
            </div>
            """,
            unsafe_allow_html=True
        )
        data['recipe_type'] = data.apply(
            lambda row: 'Vegan' if row['vegan_final'] == 1
                        else 'Vegetarienne' if row['vege'] == 1
                        else 'Other', axis=1
        )
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.boxplot(x='recipe_type', y='calories', data=data, palette="Set2", ax=ax)
        ax.set_title("Comparaison des Calories par Type de Recette")
        ax.set_xlabel("Type de Recette")
        ax.set_ylabel("Calories")
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Comparaison des Protéines par Type de Recette":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique montre la moyenne des protéines pour chaque type de recette (végétariennes, véganes et autres). Les barres d'erreur indiquent l'écart-type.
            </div>
            """,
            unsafe_allow_html=True
        )
        data['recipe_type'] = data.apply(
            lambda row: 'Vegan' if row['vegan_final'] == 1
                        else 'Vegetarienne' if row['vege'] == 1
                        else 'Other', axis=1
        )
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(x='recipe_type', y='protein (PDV%)', data=data, errorbar='sd', palette="pastel", ax=ax)
        ax.set_title("Moyenne des Protéines par Type de Recette")
        ax.set_xlabel("Type de Recette")
        ax.set_ylabel("Protéines Moyennes (PDV%)")
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Comparaison de la Complexité des Recettes":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique compare la complexité des recettes (temps de préparation, nombre d'étapes et nombre d'ingrédients) entre les recettes végétariennes, véganes et autres.
            </div>
            """,
            unsafe_allow_html=True
        )
        vegetarian_recipes = data[data['vege'] == 1]
        vegan_recipes = data[data['vegan_final'] == 1]
        other_recipes = data[(data['vege'] == 0) & (data['vegan_final'] == 0)]
        variables = ['minutes', 'n_steps', 'n_ingredients']
        fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharey=True)
        sns.boxplot(data=vegetarian_recipes[variables], ax=axes[0], palette="Blues")
        axes[0].set_title("Recettes Végétariennes")
        axes[0].set_xticks(range(len(variables)))
        axes[0].set_xticklabels(['Temps (min)', 'Étapes', 'Ingrédients'])
        axes[0].grid(True)
        sns.boxplot(data=vegan_recipes[variables], ax=axes[1], palette="Greens")
        axes[1].set_title("Recettes Vegan")
        axes[1].set_xticks(range(len(variables)))
        axes[1].set_xticklabels(['Temps (min)', 'Étapes', 'Ingrédients'])
        axes[1].grid(True)
        sns.boxplot(data=other_recipes[variables], ax=axes[2], palette="Reds")
        axes[2].set_title("Autres Recettes")
        axes[2].set_xticks(range(len(variables)))
        axes[2].set_xticklabels(['Temps (min)', 'Étapes', 'Ingrédients'])
        axes[2].grid(True)
        plt.suptitle("Comparaison des Temps, Étapes et Ingrédients par Type de Recette", fontsize=16)
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Comparaison Séparée de la Complexité des Recettes":
        data['recipe_type'] = data.apply(
            lambda row: 'Vegan' if row['vegan_final'] == 1
                        else 'Vegetarienne' if row['vege'] == 1
                        else 'Other', axis=1
        )
        variables = ['log_minutes', 'n_steps', 'n_ingredients']
        titles = ['Temps de Préparation (minutes)', 'Nombre d’Étapes', 'Nombre d’Ingrédients']
        for var, title in zip(variables, titles):
            st.markdown(
                f"""
                <div class="content">
                ### Interprétation :
                Ce graphique montre la {title.lower()} pour chaque type de recette (végétariennes, véganes et autres). Les barres d'erreur indiquent l'écart-type.
                </div>
                """,
                unsafe_allow_html=True
            )
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.barplot(x='recipe_type', y=var, data=data, errorbar='sd', palette="pastel", ax=ax)
            ax.set_title(title, fontsize=14)
            ax.set_xlabel("Type de Recette")
            ax.set_ylabel(var)
            ax.grid(True)
            plt.tight_layout()
            st.pyplot(fig)

    elif selected_vis == "Matrice de Corrélation des Variables Sélectionnées":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Cette matrice de corrélation montre les relations entre les différentes variables nutritionnelles et de complexité des recettes. Les valeurs de corrélation varient de -1 à 1, où 1 indique une corrélation positive parfaite et -1 une corrélation négative parfaite.
            </div>
            """,
            unsafe_allow_html=True
        )
        variables = [
            "calories",
            "sodium (PDV%)",
            "protein (PDV%)",
            "total fat (PDV%)",
            "saturated fat (PDV%)",
            "carbohydrates (PDV%)",
            "n_steps",
            "n_ingredients",
            "log_minutes",
            "interaction_steps_ingredients"
        ]
        correlation_data = data[variables]
        correlation_matrix = correlation_data.corr()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
        ax.set_title("Matrice de Corrélation des Variables Sélectionnées", fontsize=16)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique montre la répartition des recettes véganes parmi les recettes végétariennes. Les pourcentages indiquent la proportion de chaque type de recette.
            </div>
            """,
            unsafe_allow_html=True
        )
        vegan_among_vegetarian_percentages = [(num_vegan / num_vegetarian) * 100, ((num_vegetarian - num_vegan) / num_vegetarian) * 100]
        vegan_among_vegetarian_labels = ['Vegan', 'Végétarienne (non-vegan)']

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(vegan_among_vegetarian_percentages, labels=vegan_among_vegetarian_labels, autopct="%.1f%%", startangle=90, colors=["#ff9999", "#66b3ff"])
        ax.set_title("Répartition des recettes Vegan parmi les Végétariennes")
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
            Ce graphique montre la répartition des recettes véganes parmi les recettes végétariennes. Les pourcentages indiquent la proportion de chaque type de recette.
            </div>
            """,
            unsafe_allow_html=True
        )

# Section Exploration Interactive
if selected_option == "Exploration Interactive":
    st.sidebar.subheader("Filtrer les Recettes")
    max_calories = st.sidebar.slider("Calories Maximum", 0, int(data['calories'].max()), 500)
    max_sodium = st.sidebar.slider("Sodium Maximum", 0, int(data['sodium (PDV%)'].max()), 50)

    filtered_data = data[(data['calories'] <= max_calories) & (data['sodium (PDV%)'] <= max_sodium)]
    st.dataframe(filtered_data)

# Section À propos
if selected_option == "À propos":
    st.subheader("À propos de cette application")
    st.markdown(
        """
        <div class="content">
        ### Informations sur l'application :
        Cette application a été conçue pour analyser des recettes végétariennes et non-végétariennes afin de mettre en lumière leurs bienfaits nutritionnels.

        **Technologies utilisées :**
        - [Python](https://www.python.org/)
        - [Streamlit](https://streamlit.io/)
        - [Seaborn](https://seaborn.pydata.org/)
        - [Matplotlib](https://matplotlib.org/)

        **Développé par :** Alfred Wande-Wula
        </div>
        """,
        unsafe_allow_html=True
    )


# Footer avec image
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p style="color: gray; font-size: 0.9em;">Merci de visiter notre application d'analyse des recettes végétariennes.</p>
    </div>
    """,
    unsafe_allow_html=True
)

