import os
import requests
import pandas as pd
from src.modeles.preprocess import Preprocessing, RecipeClassifier
from src.modeles.analyse import Analysis

def download_from_s3(s3_url, dest_path):
    if os.path.exists(dest_path):
        print("✅ Fichier déjà présent.")
        return

    print("⬇️ Téléchargement depuis Amazon S3...")
    response = requests.get(s3_url)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "wb") as f:
        f.write(response.content)
    print("✅ Fichier téléchargé avec succès.")

def run_preprocessing():
    s3_url = "https://myprojetkit.s3.eu-north-1.amazonaws.com/RAW_recipes.csv"
    raw_file_path = "./data/RAW_recipes.csv"
    output_path = "./data/cleaned_recipes.csv"

    download_from_s3(s3_url, raw_file_path)

    print(f"Fichier brut prêt : {raw_file_path}")

    # Étape 1 : Prétraitement
    preprocessor = Preprocessing(file_path=raw_file_path)
    preprocessor.preprocess()
    preprocessor.remove_outliers()
    preprocessor.save_cleaned_data(output_path)

    # Classification des recettes
    classifier = RecipeClassifier(preprocessor.recipe)
    classifier.classify_recipes()
    classifier.save_cleaned_data(output_path)

    # Étape 2 : Analyse
    data = pd.read_csv(output_path)
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

if __name__ == "__main__":
    run_preprocessing()
