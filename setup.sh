#!/bin/bash

echo "telekom_ml_2026 proje yapısı hazırlanıyor..."

# Ana klasörler
mkdir -p app/{api/routes,api/dependencies}
mkdir -p app/{core,db,models,schemas,services,repositories,middlewares,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs
mkdir -p scripts
mkdir -p datasets/{raw,processed}
mkdir -p notebooks
mkdir -p models_saved
mkdir -p logs

# Python dosyaları
touch app/main.py

touch app/core/config.py
touch app/core/security.py
touch app/core/constants.py

touch app/db/connection.py

touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/repositories/__init__.py

touch app/api/routes/__init__.py
touch app/api/dependencies/__init__.py

touch app/middlewares/__init__.py

touch app/utils/helpers.py

touch tests/conftest.py

# Root dosyalar
touch requirements.txt
touch pyproject.toml
touch .env
touch .gitignore
touch README.md
touch Dockerfile
touch docker-compose.yml
touch .pre-commit-config.yaml

# VS Code ayarları
mkdir -p .vscode

cat <<EOL > .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.analysis.extraPaths": ["./app"],
    "editor.formatOnSave": true
}
EOL

cat <<EOL > .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter"
    ]
}
EOL

echo "Virtual environment oluşturuluyor..."

python3 -m venv venv

source venv/bin/activate

echo "Temel paketler kuruluyor..."

pip install --upgrade pip

pip install \
fastapi \
uvicorn \
pandas \
numpy \
scikit-learn \
matplotlib \
jupyter \
python-dotenv \
pytest

pip freeze > requirements.txt

echo "Git ignore oluşturuluyor..."

cat <<EOL > .gitignore
venv/
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
models_saved/
logs/
EOL

echo "README oluşturuluyor..."

cat <<EOL > README.md
# telekom_ml_2026

Machine Learning ve FastAPI tabanlı proje.
EOL

echo "Kurulum tamamlandı."
echo "VS Code içinde terminal açıp çalıştırabilirsiniz."