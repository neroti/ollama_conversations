
#!/bin/bash
echo "🤖 Lancement de l'Assistant Ollama..."

# Vérifier si venv est activé
if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source venv_assistant/bin/activate
fi

# Vérifier les dépendances
echo "🔍 Vérification des dépendances..."
python -c "import streamlit, requests" || {
    echo "❌ Dépendances manquantes. Installation..."
    pip install -r requirements.txt
}

# Vérifier Ollama
echo "🔍 Vérification d'Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Démarrage d'Ollama..."
    ollama serve &
    sleep 8
fi

# Lancer l'application
echo "🌐 Lancement de l'interface Streamlit..."
echo "📱 L'application sera disponible sur: http://localhost:8501"
echo "🛑 Pour arrêter: Ctrl+C"

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
