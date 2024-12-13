# Analyse comparative des recettes végétariennes et véganes

Ce projet consiste en une **application Streamlit interactive** permettant d'analyser et de comparer des recettes végétariennes, véganes et omnivores en termes de données nutritionnelles. L'application offre une exploration des différences entre ces types de recettes à l'aide de graphiques interactifs. Le projet inclut également la **documentation générée avec Sphinx** et utilise **Poetry** pour la gestion des dépendances et des environnements.

## Table des matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Dépendances](#dépendances)
4. [Tests](#tests)
5. [Documentation](#documentation)
6. [Contribuer](#contribuer)
7. [Licence](#licence)

---

## Installation

### Prérequis

Avant d'exécuter l'application, assurez-vous d'avoir **Python 3.12** ou une version compatible installé sur votre machine. Il est recommandé d'utiliser un environnement virtuel pour éviter les conflits de dépendances.

### les données 

Téléchargez les données depuis Kaggle via le lien suivant : https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv
Placez le fichier téléchargé dans le répertoire /mnt/c/Users/awand/Downloads/raw_data/.
Le chemin du fichier dans main.py doit correspondre à l'endroit où vous avez placé le fichier.

### Étapes d'installation

1. **Clonez le projet depuis le dépôt Git** :
   ```bash

Installez les dépendances avec Poetry :

bash
Copier le code
poetry install
Activez l'environnement virtuel :

bash
Copier le code
poetry shell
Vous êtes maintenant prêt à utiliser l'application ou à exécuter les tests.

Utilisation
Lancer l'application Streamlit
Une fois que l'environnement virtuel est activé, vous pouvez démarrer l'application Streamlit avec la commande suivante :

bash
Copier le code
streamlit run app.py

L'application vous permettra de :

Comparer les valeurs nutritionnelles des recettes végétariennes, véganes et omnivores.
Visualiser les résultats sous forme de graphiques interactifs.
Sélectionner différentes variables d'analyse pour personnaliser les résultats.
Dépendances
Ce projet utilise Poetry pour gérer les dépendances. Voici les principales bibliothèques utilisées :

Dépendances principales pour exécuter le projet :
Streamlit : Pour créer l'application web interactive.
Pandas : Pour la gestion des données.
NumPy : Pour les calculs numériques.
Matplotlib : Pour la création de graphiques.
Seaborn : Pour des visualisations statistiques améliorées.
Scikit-learn : Pour les modèles de machine learning (si nécessaire).
Requests : Pour effectuer des requêtes HTTP.
Dépendances de développement :
pytest : Pour les tests unitaires.
pytest-cov : Pour mesurer la couverture des tests.
flake8 : Pour le linting du code.
Black : Pour formater le code.
Sphinx : Pour générer la documentation du projet.
Poetry : Pour la gestion des dépendances et de l'environnement virtuel.
Tests
Le projet utilise pytest pour les tests unitaires. Voici comment exécuter les tests :

Exécuter les tests :

bash
Copier le code
pytest
Générer un rapport de couverture des tests :

bash
Copier le code
pytest --cov=src --cov-report=html:docs/htmlcov
Cela génère un rapport HTML de la couverture des tests dans le dossier docs/htmlcov.

Documentation
La documentation du projet est générée avec Sphinx. Vous pouvez la construire localement en suivant ces étapes :

Construire la documentation : Dans le dossier docs/, exécutez la commande suivante pour générer la documentation en HTML :

bash
Copier le code
sphinx-build -b html docs/ docs/build/
Accéder à la documentation : Ouvrez le fichier docs/build/index.html dans un navigateur pour consulter la documentation générée.

