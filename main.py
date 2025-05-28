import pandas as pd
from src.modeles.preprocess import Preprocessing, RecipeClassifier
from src.modeles.analyse import Analysis
import os

# Définir les chemins
raw_file_path = r"C:\Users\awand\Downloads\raw_data\RAW_recipes.csv"  # Chemin complet du fichier brut
output_path = "./data/cleaned_recipes.csv"

# Vérifier si le fichier brut existe
if not os.path.exists(raw_file_path):
    raise FileNotFoundError(
        f"Le fichier {raw_file_path} est introuvable.\n"
        "Veuillez vérifier le chemin du fichier."
)

print(f"Fichier brut trouvé : {raw_file_path}")

# Étape 1 : Prétraitement
preprocessor = Preprocessing(file_path=raw_file_path)
preprocessor.preprocess()
preprocessor.remove_outliers()
preprocessor.save_cleaned_data(output_path)

# Classification des recettes
classifier = RecipeClassifier(preprocessor.recipe)
classifier.classify_recipes()
classifier.save_cleaned_data(output_path)

# Étape 2 : Chargement des données nettoyées
data = pd.read_csv(output_path)

# Étape 3 : Analyse
analysis = Analysis(data)
interaction_means = analysis.calculate_interaction_means()
print(interaction_means)
analysis.t_test_interactions()
analysis.calculate_correlation_matrix()
analysis.pairwise_correlations()
analysis.point_biserial_correlation()
analysis.t_test_calories()
analysis.high_calorie_analysis()
analysis.t_tests_high_calories()
