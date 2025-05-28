import os
import requests
import pandas as pd
from src.modeles.preprocess import Preprocessing, RecipeClassifier
from src.modeles.analyse import Analysis

def download_from_drive(share_url, dest_path):
    if os.path.exists(dest_path):
        print("✅ Fichier déjà présent.")
        return

    if "drive.google.com" in share_url:
        try:
            file_id = share_url.split("/d/")[1].split("/")[0]
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        except Exception:
            raise ValueError("❌ Impossible de lire l'URL Google Drive.")
    else:
        raise ValueError("❌ Lien Google Drive invalide.")

    print("⬇️ Téléchargement du fichier depuis Google Drive...")
    response = requests.get(download_url)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(response.content)
    print("✅ Fichier téléchargé avec succès.")

def run_preprocessing():
    # 🔁 Chemin distant
    share_url = "https://drive.google.com/file/d/16NBaxXvLAK7pRKOB5y1HGiFCxD_3FqhD/view?usp=sharing"
    raw_file_path = "./data/RAW_recipes.csv"
    output_path = "./data/cleaned_recipes.csv"

    # Téléchargement si nécessaire
    download_from_drive(share_url, raw_file_path)

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

# Lancement manuel possible
if __name__ == "__main__":
    run_preprocessing()
