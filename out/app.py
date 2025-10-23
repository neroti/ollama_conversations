
import streamlit as st
import sys
import os
from pathlib import Path

# Ajouter le dossier courant au path Python
sys.path.append(str(Path(__file__).parent))

from ollama_agent import OllamaAgent
from conversation_manager import ConversationManager

def main():
    st.set_page_config(
        page_title="Assistant Ollama",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Assistant Ollama - Gestion Complète")

    # Initialisation de session
    if 'agent' not in st.session_state:
        st.session_state.agent = OllamaAgent()
        st.session_state.manager = ConversationManager()
        st.session_state.messages = []

    # Sidebar - Gestion des conversations
    with st.sidebar:
        st.header("💾 Gestion des Conversations")

        # Section sauvegarde
        st.subheader("Sauvegarder la conversation")
        with st.form("sauvegarde_form"):
            titre_sauvegarde = st.text_input("Titre de sauvegarde", value=f"Conversation_{st.session_state.agent.current_conversation[:10]}...")
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

    # Zone de chat principale
    st.header("💬 Conversation Actuelle")

    # Afficher les messages
    for message in st.session_state.messages:
        with st.chat_message("user" if message['role'] == 'user' else "assistant"):
            st.write(message['content'])

    # Input utilisateur
    if prompt := st.chat_input("Tapez votre message ici..."):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.write(prompt)

        # Obtenir la réponse
        with st.chat_message("assistant"):
            with st.spinner("🤔 Réflexion en cours..."):
                reponse = st.session_state.agent.envoyer_message(prompt)
                st.write(reponse)

        # Mettre à jour l'affichage
        st.session_state.messages = st.session_state.agent.current_conversation
        st.rerun()

if __name__ == "__main__":
    main()
