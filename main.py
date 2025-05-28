import os
import requests
import pandas as pd
from src.modeles.preprocess import Preprocessing, RecipeClassifier
from src.modeles.analyse import Analysis

def download_from_dropbox(dropbox_url, dest_path):
    if os.path.exists(dest_path):
        print("✅ Fichier déjà présent.")
        return

    print("⬇️ Téléchargement depuis Dropbox...")
    response = requests.get(dropbox_url)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "wb") as f:
        f.write(response.content)
    print("✅ Fichier téléchargé avec succès.")

def run_preprocessing():
    dropbox_url = "https://www.dropbox.com/scl/fi/dy9qt19kgloy9847cwai2/RAW_recipes.csv?rlkey=ro0amizdaw78u253f28vi05mn&st=pw503kyd&dl=1"
    raw_file_path = "./data/RAW_recipes.csv"
    output_path = "./data/cleaned_recipes.csv"

    download_from_dropbox(dropbox_url, raw_file_path)

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
