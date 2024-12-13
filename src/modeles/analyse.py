import pandas as pd
from scipy.stats import ttest_ind, pearsonr, pointbiserialr

class Analysis:
    """
    Classe pour effectuer diverses analyses statistiques sur un DataFrame de recettes.

    Attributes:
        data (pd.DataFrame): Le DataFrame contenant les données des recettes.
    """

    def __init__(self, data):
        """
        Initialise la classe Analysis avec un DataFrame.

        Args:
            data (pd.DataFrame): Le DataFrame contenant les données des recettes.
        """
        if isinstance(data, str):
            self.data = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data
        else:
            raise ValueError("Les données doivent être un chemin de fichier ou un DataFrame pandas.")

    def calculate_interaction_means(self):
        """
        Calcule les moyennes des interactions steps-ingredients pour les recettes végétariennes et véganes.
        """
        interaction_means = {}
        for col in ['vege', 'vegan_final']:
            if col in self.data.columns:
                interaction = self.data[self.data[col] == 1]['interaction_steps_ingredients']
                interaction_means[col] = interaction.mean()
            else:
                raise ValueError(f"La colonne {col} n'existe pas dans les données.")
        return interaction_means

    def t_test_interactions(self):
        """
        Effectue un test t de Student pour comparer les interactions entre les étapes et les ingrédients
        entre les recettes végétariennes et non-végétariennes, ainsi que pour les recettes véganes et non-véganes.
        """
        for col in ['vege', 'vegan_final']:
            interaction = self.data[self.data[col] == 1]['interaction_steps_ingredients']
            non_interaction = self.data[self.data[col] == 0]['interaction_steps_ingredients']

            t_stat, p_value = ttest_ind(interaction, non_interaction)
            print(f"T-statistique pour {col} : {t_stat}, P-valeur : {p_value}")

    def calculate_correlation_matrix(self):
        """
        Calcule et affiche la matrice de corrélation pour les variables numériques du DataFrame.
        """
        numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_data.corr()
        print("Matrice de Corrélation :")
        print(correlation_matrix)

    def pairwise_correlations(self):
        """
        Calcule et affiche les corrélations de Pearson entre les paires de variables nutritionnelles.
        """
        variables = ['calories', 'sodium (PDV%)', 'protein (PDV%)', 'total fat (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)']
        print("Tests de corrélation deux à deux :")
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                var1 = variables[i]
                var2 = variables[j]
                correlation, p_value = pearsonr(self.data[var1], self.data[var2])
                print(f"Corrélation entre {var1} et {var2} : r = {correlation:.3f}, p = {p_value:.3e}")

    def point_biserial_correlation(self):
        """
        Calcule et affiche les corrélations point-bisériales entre une variable binaire (végétarienne ou végane)
        et des variables nutritionnelles.
        """
        for binary_col in ['vege', 'vegan_final']:
            for col in ['calories', 'protein (PDV%)']:
                correlation, p_value = pointbiserialr(self.data[binary_col], self.data[col])
                print(f"Corrélation entre {binary_col} et {col} : r = {correlation:.3f}, p = {p_value:.3e}")

    def t_test_calories(self):
        """
        Effectue des tests t de Student pour comparer les moyennes des calories
        entre les recettes végétariennes et non-végétariennes, ainsi que pour les recettes véganes et non-véganes.
        """
        print("Tests t de Student pour les calories :")
        for binary_col in ['vege', 'vegan_final']:
            group_veg = self.data[self.data[binary_col] == 1]['calories']
            group_non_veg = self.data[self.data[binary_col] == 0]['calories']
            t_stat, p_value = ttest_ind(group_veg, group_non_veg)
            print(f"T-test pour les calories avec {binary_col} : T = {t_stat:.3f}, p = {p_value:.3e}")

    def high_calorie_analysis(self):
        """
        Analyse les recettes très caloriques en comparant les résumés nutritionnels
        des recettes végétariennes et non-végétariennes, ainsi que pour les recettes véganes et non-véganes.
        """
        calories_threshold = self.data['calories'].quantile(0.75)
        high_calories = self.data[self.data['calories'] > calories_threshold]

        for col in ['vege', 'vegan_final']:
            veg_recipes = high_calories[high_calories[col] == 1]
            non_veg_recipes = high_calories[high_calories[col] == 0]

            veg_summary = veg_recipes[['sodium (PDV%)', 'carbohydrates (PDV%)', 'saturated fat (PDV%)']].describe()
            non_veg_summary = non_veg_recipes[['sodium (PDV%)', 'carbohydrates (PDV%)', 'saturated fat (PDV%)']].describe()

            print(f"Résumé Nutritionnel des Recettes {col.capitalize()} Très Caloriques :")
            print(veg_summary)
            print(f"\nRésumé Nutritionnel des Recettes Non-{col.capitalize()} Très Caloriques :")
            print(non_veg_summary)

    def t_tests_high_calories(self):
        """
        Effectue des tests t de Student pour comparer les variables nutritionnelles
        entre les recettes végétariennes et non-végétariennes, ainsi que pour les recettes véganes et non-véganes parmi les recettes très caloriques.
        """
        calories_threshold = self.data['calories'].quantile(0.75)
        high_calories = self.data[self.data['calories'] > calories_threshold]

        for col in ['vege', 'vegan_final']:
            veg_recipes = high_calories[high_calories[col] == 1]
            non_veg_recipes = high_calories[high_calories[col] == 0]

            for var in ['sodium (PDV%)', 'carbohydrates (PDV%)', 'saturated fat (PDV%)']:
                t_stat, p_value = ttest_ind(veg_recipes[var], non_veg_recipes[var])
                print(f"{var} pour {col} : T-statistique = {t_stat:.3f}, P-valeur = {p_value:.3e}")