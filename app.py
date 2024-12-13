import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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


# Chargement du fichier CSS (assurez-vous qu'il existe dans votre projet)
local_css("docs/_static/style.css")

#style
st.markdown(
    """
    <style>
    /* Fond global de l'application */
    body {
        background-color: white; /* Fond blanc */
        color: black; /* Texte par défaut en noir pour le contraste */
    }

    /* Conserver l'image de fond pour .stApp */
    .stApp {
        background: url('https://img-3.journaldesfemmes.fr/x9Ghv5tUnuHOrOkweGUIuP2cPZU=/1240x/smart/38888207364b4e12a4058004322afa49/ccmcms-jdf/36666882.jpg') no-repeat center center fixed;
        background-size: cover;
    }

    /* Style pour le titre principal */
    .main-title {
        background: rgba(0, 0, 0, 0.8); /* Fond noir semi-transparent */
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: white; /* Texte en blanc */
    }

    /* Style pour la barre latérale */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.8) !important; /* Fond noir semi-transparent */
        padding: 20px !important; /* Espacement interne */
        border-radius: 15px !important; /* Coins arrondis */
        color: white !important; /* Texte en blanc */
    }

    /* Texte et liens dans la barre latérale */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] a {
        color: white !important; /* Forcer tout le texte et les liens en blanc */
    }

    /* Suppression des bordures inutiles */
    [data-testid="stSidebar"] section {
        border: none !important;
    }

    /* Améliorer les boutons ou sélecteurs */
    [data-testid="stSidebar"] .css-1d391kg {
        background: rgba(255, 255, 255, 0.2) !important; /* Fond semi-transparent */
        color: white !important; /* Texte blanc */
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Charger les données pour visualisation
file_path = "./data/cleaned_recipes.csv"
data = pd.read_csv(file_path)

# Titre principal avec un fond visuel
st.markdown(
    """
    <div class="main-title">
        <h1 style="color: white; text-align: center; font-size: 3.5em;">🌱 Analyse comparative des recettes végétariennes / véganes et des autres recettes </h1>
        <p style="color: white; text-align: center; font-size: 1.5em;">Une exploration interactive des types de recettes de cuisine .</p>
    </div>
    """,
    unsafe_allow_html=True,
)



# Menu latéral stylisé
st.sidebar.header("Navigation")
st.sidebar.markdown("Choisissez ce que vous souhaitez explorer :")

menu_options = [
    "Accueil",
    "Objectifs de l'application",
    "Visualisations",
    "Interactions et Tests",
    "À propos",
]
selected_option = st.sidebar.radio("Sections", menu_options)

# Section Accueil
if selected_option == "Accueil":
    st.subheader(
        "Bienvenue sur l'application d'analyse des recettes végétariennes et vegan !"
    )
    st.markdown(
        """
        <div class="content">
        Cette application permet de d'observer quelques tendances nutritionnelles dans les recettes végétariennes / vegan..
        - Explorer les différences entre recettes végétariennes / vegan et les autres recettes.

        Utilisez le menu à gauche pour en savoir plus !
        </div>
        """,
        unsafe_allow_html=True,
    )

# Section Objectifs de l'application
if selected_option == "Objectifs de l'application":
    st.subheader("Objectifs de l'application")
    st.markdown(
        """
        <div class="content">
        ### Nos objectifs :
Cette application a pour but de fournir quelques éléments de comparaison sur les recettes végétariennes et vegan et les autres recettes.
Nous espérons que cette application sera une ressource utile pour les amateurs de cuisine.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Section Visualisations
if selected_option == "Visualisations":
    st.subheader("Visualisations des Données")
    st.markdown("Sélectionnez le graphique que vous souhaitez afficher :")

    # Options de visualisation
    vis_options = [
        "Répartition des Recettes",
        "Diagramme en Barres des Types de Recettes",
        "Boxplots des Variables Nutritionnelles",
        "Comparaison des Calories par Type de Recette",
        "Comparaison des Protéines par Type de Recette",
        "Comparaison de la Complexité des Recettes",
        "Indice de complexité des recettes",
        "Comparaison Séparée de la Complexité des Recettes",
        "Matrice de Corrélation des Variables Sélectionnées",
    ]
    selected_vis = st.radio("Graphiques", vis_options)

    # Affichage des visualisations en fonction de la sélection
    if selected_vis == "Répartition des Recettes":
        st.markdown(
            """
            <div class="content">
            Ce graphique, réalisé à partir d'environ 150 000 recettes, montre une répartition relativement équilibrée entre les recettes végétariennes (48%) et non-végétariennes (52%).
            Cela suggère une diversité dans les types de recettes, avec une présence significative de recettes végétariennes.
                             
            </div>
            """,
            unsafe_allow_html=True,
        )
        num_vegetarian = data[data["vege"] == 1].shape[0]
        num_vegan = data[data["vegan_final"] == 1].shape[0]
        num_non_vegetarian = data[data["vege"] == 0].shape[0]

        total = num_vegetarian + num_non_vegetarian
        vegetarian_vs_other = [num_vegetarian, num_non_vegetarian]
        vegetarian_vs_other_labels = ["Végétariennes", "Non Végétariennes"]
        vegetarian_vs_other_percentages = [
            (count / total) * 100 for count in vegetarian_vs_other
        ]

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            vegetarian_vs_other_percentages,
            labels=vegetarian_vs_other_labels,
            autopct="%.1f%%",
            startangle=90,
            colors=["#66b3ff", "#99ff99"],
        )
        ax.set_title("Répartition des recettes (Végétariennes vs Non Végétariennes)")
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Diagramme en Barres des Types de Recettes":
        st.subheader("Diagramme en Barres des Types de Recettes")
        st.markdown(
            """
            <div class="content">
            Le nombre de recettes végétariennes (valeur = 1) est plus élevé que celui des recettes véganes.
            Cependant, le nombre de recettes qui ne sont ni véganes ni végétariennes surpassent les deux catégories.
            Cela reflète que bien que les options végétariennes soient populaires, le véganisme reste moins représenté.
                                
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Compter les occurrences pour chaque variable binaire
        vegan_counts = data["vegan_final"].value_counts().sort_index()
        vege_counts = data["vege"].value_counts().sort_index()

        # Préparer les données pour le graphique
        bar_data = (
            pd.DataFrame({"Vegan": vegan_counts, "Végétarien": vege_counts})
            .reset_index()
            .rename(columns={"index": "Catégorie"})
        )

        # Tracer le diagramme en barres
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_data.plot(kind="bar", x="Catégorie", ax=ax, rot=0)

        # Ajouter des titres et des labels
        ax.set_title("Nombre de Recettes par Type (Vegan et Végétarien)")
        ax.set_xlabel("Catégories (0 = Non, 1 = Oui)")
        ax.set_ylabel("Nombre de Recettes")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Afficher le graphique avec Streamlit
        st.pyplot(fig)

    elif selected_vis == "Boxplots des Variables Nutritionnelles":
        st.markdown(
            """
            <div class="content">
            ### Interprétation :
#Grille de lecture : un boxplot permet de visualiser la distribution d'une variable numérique. Il met en évidence les valeurs principales (comme la médiane et les quartiles) ainsi que les éventuelles valeurs aberrantes
Chaque variable nutritionnelle (calories, sodium, protéines, graisses, glucides) présente une distribution différente avec des médianes bien visible.
Les données montrent une hétérogénéité dans les profils nutritionnels des recettes. Cela peut refléter des différences entre recettes simples et élaborées ou des différences entre types de recettes (végétariennes vs non-végétariennes)
            </div>
            """,
            unsafe_allow_html=True,
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

    elif selected_vis == "Comparaison des Calories par Type de Recette":
        st.markdown(
            """
            <div class="content">
Les recettes véganes et végétariennes sont généralement moins caloriques que les autres, ce qui correspond à leur image de repas plus sains.
Ce gra^hique le montre avec une médiane plus élevée plus élevée pour les recettes non caloriques et une répartition plus faible pour les recettes végétariennes ou véganes. 
            </div>
            """,
            unsafe_allow_html=True,
        )
        data["recipe_type"] = data.apply(
            lambda row: (
                "Vegan"
                if row["vegan_final"] == 1
                else "Vegetarienne" if row["vege"] == 1 else "Other"
            ),
            axis=1,
        )
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.boxplot(x="recipe_type", y="calories", data=data, palette="Set2", ax=ax)
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
Les recettes non végétariennes semblent contenir plus de protéines en moyenne.
Les recettes véganes et végétariennes ont des moyennes similaires, mais leurs distributions sont plus étroites.
Les protéines semblent être donc plus présentes dans les recettes contenant de la viande ou des produits animaliers.
            </div>
            """,
            unsafe_allow_html=True,
        )
        data["recipe_type"] = data.apply(
            lambda row: (
                "Vegan"
                if row["vegan_final"] == 1
                else "Vegetarienne" if row["vege"] == 1 else "Other"
            ),
            axis=1,
        )
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(
            x="recipe_type",
            y="protein (PDV%)",
            data=data,
            errorbar="sd",
            palette="pastel",
            ax=ax,
        )
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
            Les recettes végétariennes et vegan appraissent relativement moins complexe selon ces trois critères. Elles prennent moins de temps, contiennent moins d'ingrédients et recquièrent moisn d'étapes.
            </div>
            """,
            unsafe_allow_html=True,
        )
        vegetarian_recipes = data[data["vege"] == 1]
        vegan_recipes = data[data["vegan_final"] == 1]
        other_recipes = data[(data["vege"] == 0) & (data["vegan_final"] == 0)]
        variables = ["minutes", "n_steps", "n_ingredients"]
        fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharey=True)
        sns.boxplot(data=vegetarian_recipes[variables], ax=axes[0], palette="Blues")
        axes[0].set_title("Recettes Végétariennes")
        axes[0].set_xticks(range(len(variables)))
        axes[0].set_xticklabels(["Temps (min)", "Étapes", "Ingrédients"])
        axes[0].grid(True)
        sns.boxplot(data=vegan_recipes[variables], ax=axes[1], palette="Greens")
        axes[1].set_title("Recettes Vegan")
        axes[1].set_xticks(range(len(variables)))
        axes[1].set_xticklabels(["Temps (min)", "Étapes", "Ingrédients"])
        axes[1].grid(True)
        sns.boxplot(data=other_recipes[variables], ax=axes[2], palette="Reds")
        axes[2].set_title("Autres Recettes")
        axes[2].set_xticks(range(len(variables)))
        axes[2].set_xticklabels(["Temps (min)", "Étapes", "Ingrédients"])
        axes[2].grid(True)
        plt.suptitle(
            "Comparaison des Temps, Étapes et Ingrédients par Type de Recette",
            fontsize=16,
        )
        plt.tight_layout()
        st.pyplot(fig)

    elif selected_vis == "Comparaison Séparée de la Complexité des Recettes":
        data["recipe_type"] = data.apply(
            lambda row: (
                "Vegan"
                if row["vegan_final"] == 1
                else "Vegetarienne" if row["vege"] == 1 else "Other"
            ),
            axis=1,
        )
        variables = ["log_minutes", "n_steps", "n_ingredients"]
        titles = [
            "Temps de Préparation (minutes)",
            "Nombre d’Étapes",
            "Nombre d’Ingrédients",
        ]
        for var, title in zip(variables, titles):
            st.markdown(
                f"""
                <div class="content">
                ### Interprétation :
                Ce graphique montre la {title.lower()} pour chaque type de recette (végétariennes, véganes et autres). Les barres d'erreur indiquent l'écart-type.
                </div>
                """,
                unsafe_allow_html=True,
            )
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.barplot(
                x="recipe_type",
                y=var,
                data=data,
                errorbar="sd",
                palette="pastel",
                ax=ax,
            )
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
Cette carte représente le lien entre les variables, plus le lien est étroit plus les couleurs sont foncées. 
En bref, les calories montrent une forte corrélation avec les graisses totales (0.83) et les glucides (0.67), ce qui est attendu d'un point de vue nutritionnel.
Les corrélations négatives avec les indicateurs "vegan_final" et "vege" suggèrent que ces types de recettes sont moins riches en calories et graisses.
Les recettes véganes et végétariennes sont associées à des profils nutritionnels plus légers. Enfin, les fortes corrélations entre variables nutritionnelles reflètent leur interdépendance dans les recettes.
            </div>
            """,
            unsafe_allow_html=True,
        )
        variables = [
            "calories",
            "sodium (PDV%)",
            "protein (PDV%)",
            "total fat (PDV%)",
            "saturated fat (PDV%)",
            "carbohydrates (PDV%)",
            "n_steps",
            "interaction_steps_ingredients",
            "vege",
            "vegan_final",
        ]
        correlation_data = data[variables]
        correlation_matrix = correlation_data.corr()
        fig, ax = plt.subplots(figsize=(8, 5))

        # Création de la heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax
        )
        ax.set_title("Matrice de Corrélation des Variables Sélectionnées", fontsize=16)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

# Section À propos
if selected_option == "À propos":
    st.subheader("À propos de cette application")
    st.markdown(
        """
        ### Informations sur l'application :
        Cette application a été conçue pour analyser des recettes végétariennes et non-végétariennes afin de mettre en lumière leurs bienfaits nutritionnels.

        **Technologies utilisées :**
        - [Python](https://www.python.org/)
        - [Streamlit](https://streamlit.io/)
        - [Seaborn](https://seaborn.pydata.org/)
        - [Matplotlib](https://matplotlib.org/)

        **Développé par :** Alfred Wande-Wula
        """
    )


    # Footer avec image
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <p style="color: gray; font-size: 0.9em;">Merci de visiter notre application d'analyse des recettes végétariennes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
