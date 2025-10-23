
import streamlit as st
import sys
import os
from pathlib import Path
import time

# Ajouter le dossier courant au path Python
sys.path.append(str(Path(__file__).parent))

from ollama_agent import OllamaAgent
from conversation_manager import ConversationManager

def main():
    st.set_page_config(
        page_title="Assistant Ollama Multi-Modèles",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Assistant Ollama - Multi-Modèles")

    # Initialisation de session
    if 'agent' not in st.session_state:
        st.session_state.agent = OllamaAgent()
        st.session_state.manager = ConversationManager()
        st.session_state.messages = []
        st.session_state.available_models = st.session_state.agent.get_available_models()
        st.session_state.current_model = st.session_state.agent.current_model

    # Sidebar - Configuration et gestion
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Sélecteur de modèle
        st.subheader("🧠 Sélection du Modèle")

        # Rafraîchir la liste des modèles
        if st.button("🔄 Rafraîchir la liste"):
            st.session_state.available_models = st.session_state.agent.get_available_models()
            st.rerun()

        if st.session_state.available_models:
            selected_model = st.selectbox(
                "Choisir un modèle:",
                options=st.session_state.available_models,
                index=st.session_state.available_models.index(st.session_state.current_model)
                if st.session_state.current_model in st.session_state.available_models else 0
            )

            # Changer de modèle si sélection différent
            if selected_model != st.session_state.current_model:
                if st.button(f"🔁 Passer à {selected_model}"):
                    if st.session_state.agent.change_model(selected_model):
                        st.session_state.current_model = selected_model
                        st.session_state.messages = []  # Réinitialiser la conversation
                        st.success(f"✅ Modèle changé: {selected_model}")
                        st.rerun()
                    else:
                        st.error("❌ Erreur changement de modèle")

            # Afficher info modèle actuel
            st.info(f"**Modèle actuel:** {st.session_state.current_model}")
        else:
            st.warning("⚠️ Aucun modèle trouvé. Vérifiez qu'Ollama est démarré.")

        st.divider()

        # Section gestion des conversations
        st.header("💾 Gestion des Conversations")

        # Section sauvegarde
        st.subheader("Sauvegarder la conversation")
        with st.form("sauvegarde_form"):
            titre_sauvegarde = st.text_input("Titre de sauvegarde",
                                           value=f"Conversation_{st.session_state.current_model}_{int(time.time())}")
            if st.form_submit_button("💾 Sauvegarder"):
                if st.session_state.agent.current_conversation:
                    result = st.session_state.agent.sauvegarder_conversation_actuelle(titre_sauvegarde)
                    if result["status"] == "success":
                        st.success(f"✅ Conversation sauvegardée: {result['fichier']}")
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.warning("⚠️ Aucune conversation à sauvegarder")

        st.divider()

        # Section chargement
        st.subheader("📁 Conversations Sauvegardées")
        conversations = st.session_state.manager.lister_conversations()

        if not conversations:
            st.info("Aucune conversation sauvegardée")
        else:
            for conv in conversations:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{conv['titre']}**")
                    st.caption(f"{conv['messages']} messages - {conv['date'][:16]}")

                with col2:
                    if st.button("📥", key=f"load_{conv['fichier']}"):
                        result = st.session_state.agent.charger_conversation_sauvegardee(conv['fichier'])
                        if result["status"] == "success":
                            st.session_state.messages = st.session_state.agent.current_conversation
                            st.success("✅ Conversation chargée!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")

                with col3:
                    if st.button("📤", key=f"export_{conv['fichier']}"):
                        export_file = st.session_state.manager.exporter_markdown(conv['fichier'])
                        if export_file:
                            st.success(f"✅ Exporté: {export_file.name}")
                        else:
                            st.error("❌ Erreur lors de l'export")

        st.divider()

        # Informations système
        st.subheader("📊 Informations Système")
        st.write(f"**Modèles disponibles:** {len(st.session_state.available_models)}")
        st.write(f"**Conversations sauvegardées:** {len(conversations)}")
        st.write(f"**Messages actuels:** {len(st.session_state.messages)}")

    # Zone de chat principale
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("💬 Conversation Actuelle")
    with col2:
        st.metric("Modèle", st.session_state.current_model)

    # Afficher les messages avec indication du modèle
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message("user" if message['role'] == 'user' else "assistant"):
            if message['role'] == 'assistant':
                st.caption(f"Modèle: {st.session_state.current_model}")
            st.write(message['content'])

    # Input utilisateur
    if prompt := st.chat_input(f"Tapez votre message pour {st.session_state.current_model}..."):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.write(prompt)

        # Obtenir la réponse
        with st.chat_message("assistant"):
            st.caption(f"Modèle: {st.session_state.current_model}")
            with st.spinner("🤔 Réflexion en cours..."):
                reponse = st.session_state.agent.envoyer_message(prompt)
                st.write(reponse)

        # Mettre à jour l'affichage
        st.session_state.messages = st.session_state.agent.current_conversation
        st.rerun()

if __name__ == "__main__":
    main()
