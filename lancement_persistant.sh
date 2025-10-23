
#!/bin/bash
# lancement_persistant.sh

echo "🤖 Lancement de l'Assistant Ollama avec Persistance..."

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

# Test de la persistance
echo "💾 Test du système de persistance..."
python test_persistence.py

# Afficher les statistiques de sessions
echo "📊 Statistiques des sessions:"
python -c "
from conversation_manager import ConversationManager
manager = ConversationManager()
history = manager.load_session_history()
print(f'   Sessions totales: {history.get(\"total_sessions\", 0)}')
print(f'   Session actuelle: {history.get(\"current_session_id\", \"Aucune\")}')
"

echo ""
echo "🌐 Lancement de l'interface Streamlit..."
echo "📱 L'application sera disponible sur: http://localhost:8501"
echo "🎯 NOUVEAU: Conversations persistantes + Bouton 'Nouvelle conversation'"
echo "💾 Les historiques sont sauvegardés automatiquement"
echo "🛑 Pour arrêter: Ctrl+C"

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
