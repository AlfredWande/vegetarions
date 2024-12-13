import pandas as pd
import pytest
from src.modeles.preprocess import Preprocessing

@pytest.fixture
def mock_data():
    data = {
        'id': [1, 2],
        'name': ['Recipe1', 'Recipe2'],
        'nutrition': ['[200,5,10,20,15,5,30]', '[300,10,20,30,25,15,60]'],
        'n_steps': [2, 2],
        'n_ingredients': [5, 6],
        'minutes': [30, 40]
    }
    return pd.DataFrame(data)

def test_preprocess(mock_data, tmp_path):
    # Créer un fichier temporaire à partir des données fictives
    input_file = tmp_path / "raw_recipes.csv"
    output_file = tmp_path / "cleaned_recipes.csv"
    mock_data.to_csv(input_file, index=False)

    # Initialiser le préprocesseur
    preprocessor = Preprocessing(file_path=str(input_file))
    preprocessor.preprocess()
    preprocessor.remove_outliers()
    preprocessor.save_cleaned_data(output_path=str(output_file))

    # Charger les données traitées
    processed_data = pd.read_csv(output_file)

    # Tests pour valider les colonnes attendues
    expected_columns = [
        'id', 'name', 'calories', 'total fat (PDV%)', 'sugar (PDV%)',
        'sodium (PDV%)', 'protein (PDV%)', 'saturated fat (PDV%)',
        'carbohydrates (PDV%)', 'interaction_steps_ingredients', 'log_minutes'
    ]
    # Vérifier que toutes les colonnes attendues sont présentes dans les données traitées
    missing_columns = [col for col in expected_columns if col not in processed_data.columns]
    assert not missing_columns, f"Colonnes manquantes dans les données traitées : {missing_columns}"