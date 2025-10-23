
# streamlit_app.py
import streamlit as st
import requests
import json
import os
from datetime import datetime
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Assistant IA Ollama Cloud",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Message d'accueil cloud
st.title("🌍 Assistant IA - Version Cloud")
st.markdown("""
*Votre assistant IA personnel accessible partout dans le monde!*

🔗 **Connectez-vous à votre instance Ollama locale ou distante**
""")

# Configuration de la connexion Ollama
st.sidebar.header("🔧 Configuration Cloud")

# URL d'Ollama (peut être locale ou distante)
ollama_url = st.sidebar.text_input(
    "URL de l'API Ollama:",
    value="http://localhost:11434",
    help="URL de votre instance Ollama (localhost pour local, IP:port pour distant)"
)

# Vérification de la connexion
def test_ollama_connection(url):
    try:
        response = requests.get(f"{url}/api/tags", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

# Section connexion
if st.sidebar.button("🔗 Tester la connexion"):
    with st.spinner("Test de connexion à Ollama..."):
        connected, models_data = test_ollama_connection(ollama_url)
        if connected:
            st.sidebar.success("✅ Connecté à Ollama!")
            if models_data and 'models' in models_data:
                st.sidebar.info(f"📚 {len(models_data['models'])} modèles détectés")
        else:
            st.sidebar.error("❌ Impossible de se connecter à Ollama")

# Instructions de déploiement
with st.expander("📖 Instructions de configuration cloud"):
    st.markdown("""
    ### Pour utiliser cette application dans le cloud:

    **Option 1 - Ollama Local:**
    ```bash
    # Gardez Ollama en local et utilisez ngrok
    ./deploy_with_ngrok.sh
    ```

    **Option 2 - Serveur dédié:**
    ```bash
    # Installez Ollama sur un serveur cloud
    curl -fsSL https://ollama.ai/install.sh | sh
    ollama pull llama3.2:1b
    ```

    **Option 3 - Service cloud Ollama:**
    - Utilisez un service comme [Ollama Cloud](https://ollama.ai) (si disponible)
    - Ou déployez sur [Hugging Face Spaces](https://huggingface.co/spaces)
    """)

# Gestion des modèles
def get_available_models(url):
    try:
        response = requests.get(f"{url}/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except:
        return []

# Interface de chat simplifiée pour le cloud
st.header("💬 Chat IA Cloud")

# Initialisation de session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = "llama3.2:1b"

# Sélection du modèle
available_models = get_available_models(ollama_url)
if available_models:
    selected_model = st.selectbox(
        "Choisir le modèle:",
        options=available_models,
        key="model_selector_cloud"
    )
    st.session_state.current_model = selected_model
else:
    st.warning("⚠️ Aucun modèle détecté. Vérifiez la connexion Ollama.")

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input utilisateur
if prompt := st.chat_input("Tapez votre message..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Envoyer à Ollama
    with st.chat_message("assistant"):
        with st.spinner("🤔 Réflexion en cours..."):
            try:
                payload = {
                    "model": st.session_state.current_model,
                    "messages": st.session_state.messages,
                    "stream": False
                }

                response = requests.post(
                    f"{ollama_url}/api/chat",
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    response_data = response.json()
                    assistant_response = response_data['message']['content']
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    st.write(assistant_response)
                else:
                    error_msg = f"Erreur API: {response.status_code}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)

            except Exception as e:
                error_msg = f"Erreur de connexion: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)

# Bouton de réinitialisation
if st.button("🔄 Nouvelle conversation", key="new_chat_cloud"):
    st.session_state.messages = []
    st.rerun()

# Statistiques
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Statistiques Cloud")
st.sidebar.write(f"**Messages:** {len(st.session_state.messages)}")
st.sidebar.write(f"**Modèle actuel:** {st.session_state.current_model}")
st.sidebar.write(f"**Modèles disponibles:** {len(available_models)}")

if __name__ == "__main__":
    st.info("🌐 **Application prête pour le déploiement cloud!**")
