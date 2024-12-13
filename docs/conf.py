# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../src/modeles/'))  # Chemin vers le répertoire racine du projet

project = 'Analyse des recettes végétariennes et véganes'
copyright = '2024, Alfred Wande-Wula'
author = 'Alfred Wande-Wula'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Pour les docstrings Google et NumPy
    'sphinx.ext.viewcode',  # Ajoute des liens vers le code source
]

templates_path = ['_templates']
exclude_patterns = []

language = 'Française'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
