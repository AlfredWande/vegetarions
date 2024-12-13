import pytest
import pandas as pd
from src.modeles.analyse import Analysis

@pytest.fixture
def sample_data():
    """
    Fixture pour créer un DataFrame d'exemple pour les tests.

    Returns:
        pd.DataFrame: Un DataFrame contenant des données d'exemple pour les tests.
    """
    data = {
        'vege': [1, 0, 1, 0, 1],
        'vegan_final': [1, 0, 0, 0, 1],
        'calories': [200, 150, 300, 400, 100],
        'sodium (PDV%)': [30, 40, 20, 50, 35],
        'protein (PDV%)': [10, 20, 15, 25, 5],
        'interaction_steps_ingredients': [50, 60, 40, 80, 30],
        'total fat (PDV%)': [5, 6, 7, 8, 9],
        'carbohydrates (PDV%)': [50, 40, 30, 60, 70],
        'saturated fat (PDV%)': [2, 3, 4, 5, 6],
    }
    return pd.DataFrame(data)

def test_calculate_interaction_means(sample_data):
    """
    Test de la méthode calculate_interaction_means.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
    """
    analysis = Analysis(sample_data)
    interaction_means = analysis.calculate_interaction_means()
    assert 'vege' in interaction_means
    assert 'vegan_final' in interaction_means
    assert isinstance(interaction_means['vege'], float)

def test_t_test_interactions(sample_data, capsys):
    """
    Test de la méthode t_test_interactions.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.t_test_interactions()
    captured = capsys.readouterr()
    assert "T-statistique pour vege" in captured.out
    assert "T-statistique pour vegan_final" in captured.out

def test_correlation_matrix(sample_data, capsys):
    """
    Test de la méthode calculate_correlation_matrix.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.calculate_correlation_matrix()
    captured = capsys.readouterr()
    assert "Matrice de Corrélation :" in captured.out

def test_pairwise_correlations(sample_data, capsys):
    """
    Test de la méthode pairwise_correlations.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.pairwise_correlations()
    captured = capsys.readouterr()
    assert "Corrélation entre" in captured.out

def test_point_biserial_correlation(sample_data, capsys):
    """
    Test de la méthode point_biserial_correlation.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.point_biserial_correlation()
    captured = capsys.readouterr()
    assert "Corrélation entre" in captured.out

def test_t_test_calories(sample_data, capsys):
    """
    Test de la méthode t_test_calories.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.t_test_calories()
    captured = capsys.readouterr()
    assert "T-test pour les calories" in captured.out

def test_high_calorie_analysis(sample_data, capsys):
    """
    Test de la méthode high_calorie_analysis.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.high_calorie_analysis()
    captured = capsys.readouterr()
    assert "Résumé Nutritionnel des Recettes" in captured.out

def test_t_tests_high_calories(sample_data, capsys):
    """
    Test de la méthode t_tests_high_calories.

    Args:
        sample_data (pd.DataFrame): Le DataFrame d'exemple pour les tests.
        capsys (pytest.CaptureFixture): Fixture pour capturer les sorties standard.
    """
    analysis = Analysis(sample_data)
    analysis.t_tests_high_calories()
    captured = capsys.readouterr()
    assert "T-statistique =" in captured.out