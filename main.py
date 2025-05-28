import gdown
import os
import pandas as pd
from src.modeles.preprocess import Preprocessing, RecipeClassifier
from src.modeles.analyse import Analysis

def download_from_drive(share_url, dest_path):
    if os.path.exists(dest_path):
        print("✅ Fichier déjà présent.")
        return

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print("⬇️ Téléchargement avec gdown...")
    gdown.download(url=share_url, output=dest_path, quiet=False, fuzzy=True)
    print("✅ Fichier téléchargé avec succès.")

def run_preprocessing():
    share_url = "https://drive.google.com/file/d/16NBaxXvLAK7pRKOB5y1HGiFCxD_3FqhD/view?usp=sharing"
    raw_file_path = "./data/RAW_recipes.csv"
    output_path = "./data/cleaned_recipes.csv"

    download_from_drive(share_url, raw_file_path)

    print(f"Fichier brut prêt : {raw_file_path}")

    preprocessor = Preprocessing(file_path=raw_file_path)
    preprocessor.preprocess()
    preprocessor.remove_outliers()
    preprocessor.save_cleaned_data(output_path)

    classifier = RecipeClassifier(preprocessor.recipe)
    classifier.classify_recipes()
    classifier.save_cleaned_data(output_path)

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
