import numpy as np
from statsmodels.robust.scale import mad
from sklearn.preprocessing import StandardScaler
import nltk
import re
import pandas as pd
from pyfood.utils import Shelf
nltk.download('punkt')

class Preprocessing:
    """
    Classe pour effectuer le prétraitement des données de recettes.

    Attributes:
        recipe (pd.DataFrame): Le DataFrame contenant les données des recettes.
        recipe_cleaned (pd.DataFrame): Le DataFrame contenant les données des recettes nettoyées.
    """

    def __init__(self, file_path):
        """
        Initialise la classe Preprocessing avec un fichier CSV contenant les données des recettes.

        Args:
            file_path (str): Le chemin du fichier CSV contenant les données des recettes.
        """
        self.recipe = pd.read_csv(file_path)
        self.recipe_cleaned = None

    def preprocess(self):
        """
        Effectue le prétraitement des données des recettes.
        """
        self.recipe[['calories','total fat (PDV%)','sugar (PDV%)','sodium (PDV%)',
                     'protein (PDV%)','saturated fat (PDV%)','carbohydrates (PDV%)']] = self.recipe['nutrition'].str.split(",",expand=True)

        self.recipe['calories'] = self.recipe['calories'].str.replace('[','', regex=False).astype(float)
        self.recipe['carbohydrates (PDV%)'] = self.recipe['carbohydrates (PDV%)'].str.replace(']','', regex=False).astype(float)

        nutrition_cols = ['calories', 'total fat (PDV%)', 'sugar (PDV%)', 'sodium (PDV%)', 'protein (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)']
        self.recipe[nutrition_cols] = self.recipe[nutrition_cols].astype(float)

        self.recipe = self.recipe.dropna()

        self.recipe['interaction_steps_ingredients'] = self.recipe['n_steps'] * self.recipe['n_ingredients']

        scaler = StandardScaler()
        columns_to_standardize = ['calories', 'total fat (PDV%)', 'sugar (PDV%)', 'sodium (PDV%)', 'protein (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)']
        self.recipe[columns_to_standardize] = scaler.fit_transform(self.recipe[columns_to_standardize])

        for col in columns_to_standardize:
            skewness = self.recipe[col].skew()
            print(f"Symétrie de {col} : {skewness:.3f}")

    def find_optimal_k1_k2(self, data, col, k1_values, k2_values, target_percent=95):
        """
        Trouve les valeurs optimales de k1 et k2 pour la suppression des outliers.

        Args:
            data (pd.DataFrame): Le DataFrame contenant les données.
            col (str): La colonne pour laquelle trouver les valeurs optimales de k1 et k2.
            k1_values (list): Les valeurs possibles de k1.
            k2_values (list): Les valeurs possibles de k2.
            target_percent (float): Le pourcentage cible de données à conserver.

        Returns:
            tuple: Les valeurs optimales de k1 et k2.
        """
        median = data[col].median()
        mad_value = mad(data[col])
        optimal_k1, optimal_k2 = None, None
        optimal_percent = 0

        for k1 in k1_values:
            for k2 in k2_values:
                lower_bound = median - k1 * mad_value
                upper_bound = median + k2 * mad_value

                filtered_data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
                percent_remaining = len(filtered_data) / len(data) * 100

                if percent_remaining >= target_percent and percent_remaining > optimal_percent:
                    optimal_k1, optimal_k2 = k1, k2
                    optimal_percent = percent_remaining

        return optimal_k1, optimal_k2

    def remove_outliers(self):
        """
        Supprime les outliers des données des recettes.
        """
        cols_to_check = ['calories', 'total fat (PDV%)', 'sodium (PDV%)', 'protein (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)', 'n_ingredients', 'n_steps', 'interaction_steps_ingredients', 'minutes']
        k1_default, k2_default = 1.5, 3.0
        k1_values = np.linspace(1.5, 3, 5)
        k2_values = np.linspace(3, 5, 5)

        for col in cols_to_check:
            optimal_k1, optimal_k2 = self.find_optimal_k1_k2(self.recipe, col, k1_values, k2_values)

            if optimal_k1 is None or optimal_k2 is None:
                print(f"Optimal k1 et k2 non trouvés pour {col}. Utilisation des valeurs par défaut.")
                optimal_k1, optimal_k2 = k1_default, k2_default

            median = self.recipe[col].median()
            mad_value = mad(self.recipe[col])

            if mad_value == 0:
                print(f"MAD nul pour {col}. Aucun outlier supprimé.")
                continue

            lower_bound = median - optimal_k1 * mad_value
            upper_bound = median + optimal_k2 * mad_value

            self.recipe = self.recipe[(self.recipe[col] >= lower_bound) & (self.recipe[col] <= upper_bound)]

            print(f"Outliers supprimés pour {col} avec k1={optimal_k1}, k2={optimal_k2}")

        # Ajout de la colonne log_minutes après la suppression des outliers
        self.recipe['log_minutes'] = np.log1p(self.recipe['minutes'])

    def save_cleaned_data(self, output_path):
        """
        Sauvegarde les données nettoyées dans un fichier CSV.

        Args:
            output_path (str): Le chemin du fichier CSV de sortie.
        """
        self.recipe.to_csv(output_path, index=False)
        print(f"Données prétraitées sauvegardées dans {output_path}")

class RecipeClassifier:
    """
    Classe pour classifier les recettes en végétariennes et véganes.

    Attributes:
        df (pd.DataFrame): Le DataFrame contenant les données des recettes.
        shelf (Shelf): L'objet Shelf pour obtenir des informations sur les aliments.
        non_vegetarian_taxons (list): Les taxons des aliments non végétariens.
        non_vegan_taxons (list): Les taxons des aliments non véganes.
    """

    def __init__(self, df):
        """
        Initialise la classe RecipeClassifier avec un DataFrame contenant les données des recettes.

        Args:
            df (pd.DataFrame): Le DataFrame contenant les données des recettes.
        """
        self.df = df
        self.shelf = Shelf(region='EU', lang_source='en', month_id=0)
        self.non_vegetarian_taxons = ['203', '211', '212', '213', '214']
        self.non_vegan_taxons = ['201', '202']

    def clean_and_tokenize(self, text):
        """
        Nettoie et tokenize le texte.

        Args:
            text (str): Le texte à nettoyer et tokenizer.

        Returns:
            list: Une liste de tokens.
        """
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = [word.strip() for word in text.split()]
        return tokens

    def is_vegetarian(self, text):
        """
        Vérifie si le texte contient des aliments non végétariens.

        Args:
            text (str): Le texte à vérifier.

        Returns:
            str: "végétarienne" si le texte ne contient pas d'aliments non végétariens, sinon "non-végétarienne".
        """
        words_list = self.clean_and_tokenize(text)
        for word in words_list:
            try:
                food_info = self.shelf.get_food_info(word)
                taxon = food_info[2]
                if taxon in self.non_vegetarian_taxons:
                    return "non-végétarienne"
            except:
                continue
        return "végétarienne"

    def is_vegan(self, text):
        """
        Vérifie si le texte contient des aliments non véganes.

        Args:
            text (str): Le texte à vérifier.

        Returns:
            str: "vegan" si le texte ne contient pas d'aliments non véganes, sinon "non-vegan".
        """
        words_list = self.clean_and_tokenize(text)
        for word in words_list:
            try:
                food_info = self.shelf.get_food_info(word)
                taxon = food_info[2]
                if taxon in self.non_vegan_taxons:
                    return "non-vegan"
            except:
                continue
        return "vegan"

    def classify_recipes(self):
        """
        Classifie les recettes en végétariennes et véganes.
        """
        self.df["vege_ingr"] = self.df["ingredients"].apply(self.is_vegetarian)
        self.df["vege_name"] = self.df["name"].apply(self.is_vegetarian) if 'name' in self.df.columns else "non-végétarienne"
        self.df["vege_steps"] = self.df["steps"].apply(self.is_vegetarian)

        self.df["vege"] = ((self.df["vege_steps"] == "végétarienne") &
                         (self.df["vege_name"] == "végétarienne") &
                         (self.df["vege_ingr"] == "végétarienne")).astype(int)

        self.df["vegan_ingr"] = self.df["ingredients"].apply(self.is_vegan)
        self.df["vegan_name"] = self.df["name"].apply(self.is_vegan) if 'name' in self.df.columns else "non-vegan"
        self.df["vegan_steps"] = self.df["steps"].apply(self.is_vegan)

        self.df["vegan"] = ((self.df["vegan_steps"] == "vegan") &
                            (self.df["vegan_name"] == "vegan") &
                            (self.df["vegan_ingr"] == "vegan")).astype(int)

        self.df["vegan_final"] = ((self.df["vege"] == 1) & (self.df["vegan"] == 1)).astype(int)

    def save_cleaned_data(self, output_path):
        """
        Sauvegarde les données classifiées dans un fichier CSV.

        Args:
            output_path (str): Le chemin du fichier CSV de sortie.
        """
        self.df.to_csv(output_path, index=False)
        print(f"Données prétraitées sauvegardées dans {output_path}")