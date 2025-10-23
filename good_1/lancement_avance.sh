
#!/bin/bash
echo "🤖 Lancement de l'Assistant Ollama Multi-Modèles..."

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

# Afficher les modèles disponibles
echo "📚 Modèles disponibles:"
curl -s http://localhost:11434/api/tags | python3 -c "
import json, sys
data = json.load(sys.stdin)
for model in data.get('models', []):
    print(f'  - {model['name']}')
"

echo ""
echo "🌐 Lancement de l'interface Streamlit..."
echo "📱 L'application sera disponible sur: http://localhost:8501"
echo "🎯 Fonctionnalités: Sélection de modèle, gestion des conversations"
echo "🛑 Pour arrêter: Ctrl+C"

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
