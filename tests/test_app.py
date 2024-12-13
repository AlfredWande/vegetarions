import pytest
import pandas as pd
import streamlit as st
from streamlit.testing import TestRunner
from unittest.mock import patch

@pytest.fixture
def sample_data():
    """Fixture pour créer un DataFrame d'exemple pour les tests."""
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

@patch('app.pd.read_csv')
def test_load_data(mock_read_csv, sample_data):
    """Test de la fonction de chargement des données."""
    mock_read_csv.return_value = sample_data

    runner = TestRunner('app')
    result = runner.run()
    assert result.success
    mock_read_csv.assert_called_once_with("./data/cleaned_recipes.csv")

@patch('app.pd.read_csv')
def test_display_data(mock_read_csv, sample_data):
    """Test de l'affichage des données."""
    mock_read_csv.return_value = sample_data

    runner = TestRunner('app')
    result = runner.run()
    assert "Recipe1" in result.text
    assert "Recipe2" in result.text
    assert "Recipe3" in result.text

@patch('app.pd.read_csv')
def test_visualisation_selection(mock_read_csv, sample_data):
    """Test de la sélection des visualisations."""
    mock_read_csv.return_value = sample_data

    runner = TestRunner('app')
    result = runner.run()

    # Test for the presence of the visualisation options
    assert "Répartition des Recettes" in result.text
    assert "Diagramme en Barres des Types de Recettes" in result.text
    assert "Statistiques descriptives" in result.text
    assert "Boxplots des Variables Nutritionnelles" in result.text

@patch('app.pd.read_csv')
def test_sidebar_navigation(mock_read_csv, sample_data):
    """Test de la navigation dans la barre latérale."""
    mock_read_csv.return_value = sample_data

    runner = TestRunner('app')
    result = runner.run()

    # Test for the presence of the sidebar options
    assert "Accueil" in result.text
    assert "Objectifs de l'application" in result.text
    assert "Visualisations" in result.text
    assert "Exploration Interactive" in result.text
    assert "À propos" in result.text

@patch('app.pd.read_csv')
def test_error_handling(mock_read_csv):
    """Test de la gestion des erreurs lors du chargement des données."""
    mock_read_csv.side_effect = FileNotFoundError

    runner = TestRunner('app')
    result = runner.run()

    # Test for the presence of the error message
    assert "Le fichier './data/cleaned_recipes.csv' est introuvable." in result.text