#!/bin/bash
pytest --cov=src --cov-report=term-missing --cov-report=html tests/
echo "Rapport HTML généré dans le dossier htmlcov/"

