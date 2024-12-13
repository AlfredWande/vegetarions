import pytest
import pandas as pd
from src.modeles.preprocess import Preprocessing
from src.modeles.preprocess import RecipeClassifier

@pytest.fixture
def sample_data(tmp_path):
    data = {
        'nutrition': ['[100, 10, 5, 200, 10, 5, 50]', '[200, 20, 10, 400, 20, 10, 100]', '[150, 15, 7, 300, 15, 7, 75]'],
        'n_steps': [5, 10, 7],
        'n_ingredients': [10, 15, 12],
        'minutes': [30, 60, 45],
        'ingredients': ['chicken, salt, pepper', 'tofu, soy sauce, garlic', 'beef, onion, tomato'],
        'name': ['Chicken Soup', 'Tofu Stir Fry', 'Beef Stew'],
        'steps': ['cook chicken, add salt and pepper', 'cook tofu, add soy sauce and garlic', 'cook beef, add onion and tomato']
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample_data.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_preprocess(sample_data):
    preprocessor = Preprocessing(sample_data)
    preprocessor.preprocess()
    assert 'calories' in preprocessor.recipe.columns
    assert 'interaction_steps_ingredients' in preprocessor.recipe.columns

def test_remove_outliers(sample_data):
    preprocessor = Preprocessing(sample_data)
    preprocessor.preprocess()
    preprocessor.remove_outliers()
    assert 'log_minutes' in preprocessor.recipe.columns

def test_save_cleaned_data_preprocessing(sample_data, tmp_path):
    preprocessor = Preprocessing(sample_data)
    preprocessor.preprocess()
    output_path = tmp_path / "cleaned_data.csv"
    preprocessor.save_cleaned_data(output_path)
    assert output_path.exists()

def test_classify_recipes(sample_data):
    df = pd.read_csv(sample_data)
    classifier = RecipeClassifier(df)
    classifier.classify_recipes()
    assert 'vege' in classifier.df.columns
    assert 'vegan_final' in classifier.df.columns

def test_save_cleaned_data_classifier(sample_data, tmp_path):
    df = pd.read_csv(sample_data)
    classifier = RecipeClassifier(df)
    classifier.classify_recipes()
    output_path = tmp_path / "classified_data.csv"
    classifier.save_cleaned_data(output_path)
    assert output_path.exists()