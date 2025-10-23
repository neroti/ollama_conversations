
#!/bin/bash
echo "🚀 Installation de l'Assistant Ollama avec venv..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    sudo zypper install python3 python3-pip
fi

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv_assistant

# Activer venv
source venv_assistant/bin/activate

# Mettre à jour pip
echo "🔄 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install streamlit requests pathlib

# Vérifier l'installation
echo "🔍 Vérification des installations..."
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)"
python -c "import requests; print('✅ Requests:', requests.__version__)"

# Créer les dossiers de données
mkdir -p sauvegardes exports

# Tester Ollama
echo "🔍 Vérification d'Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama n'est pas démarré. Démarrage..."
    ollama serve &
    sleep 10
fi

# Télécharger un modèle léger pour test
echo "📥 Téléchargement d'un modèle de test..."
ollama pull llama3.2:1b

echo ""
echo "✅ Installation terminée!"
echo "🎯 Pour activer l'environnement: source venv_assistant/bin/activate"
echo "🎯 Pour lancer l'application: ./lancement.sh"
