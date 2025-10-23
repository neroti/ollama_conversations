
# deploy_with_ngrok.sh
#!/bin/bash

echo "🌍 DÉPLOIEMENT CLOUD AVEC NGROK"

# Vérifier si Ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "📥 Installation de Ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok
fi

# Vérifier l'authentification Ngrok
if [ ! -f ~/.ngrok2/ngrok.yml ]; then
    echo "🔐 Configuration de Ngrok requise:"
    echo "1. Allez sur https://dashboard.ngrok.com"
    echo "2. Créez un compte gratuit"
    echo "3. Récupérez votre token d'authentification"
    echo "4. Exécutez: ngrok config add-authtoken VOTRE_TOKEN"
    exit 1
fi

# Démarrer Ollama en arrière-plan
echo "🚀 Démarrage d'Ollama..."
ollama serve &
OLLAMA_PID=$!
sleep 5

# Vérifier qu'Ollama fonctionne
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama est démarré"
else
    echo "❌ Erreur: Ollama ne répond pas"
    exit 1
fi

# Démarrer Streamlit en arrière-plan
echo "🌐 Démarrage de Streamlit..."
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!
sleep 5

# Démarrer Ngrok
echo "🔗 Lancement du tunnel Ngrok..."
ngrok http 8501

# Nettoyage à l'arrêt
cleanup() {
    echo "🛑 Arrêt en cours..."
    kill $OLLAMA_PID $STREAMLIT_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Attendre indéfiniment
wait
