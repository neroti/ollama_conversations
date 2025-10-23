
#!/bin/bash
echo "🚀 Installation de l'Assistant Ollama..."

# Créer l'environnement
mkdir -p ~/ollama_conversations/{sauvegardes,exports}

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip3 install streamlit requests pathlib

# Tester Ollama
echo "🔍 Vérification d'Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama n'est pas démarré. Démarrage..."
    ollama serve &
    sleep 10
fi

# Télécharger un modèle léger pour test
echo "📥 Téléchargement d'un modèle de test..."
ollama pull llama3.2:1b

echo "✅ Installation terminée!"
echo "🎯 Pour lancer l'application: streamlit run app.py"
