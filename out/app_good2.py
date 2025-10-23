
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
        page_title="Assistant Ollama - Conversations Persistantes",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🤖 Assistant Ollama - Conversations Persistantes")

    # Initialisation de session Streamlit
    if 'agent' not in st.session_state:
        st.session_state.agent = OllamaAgent()
        st.session_state.manager = ConversationManager()
        st.session_state.available_models = st.session_state.agent.get_available_models()
        st.session_state.current_model = st.session_state.agent.current_model

        # Charger la session actuelle
        current_session = st.session_state.agent.get_current_session_info()
        st.session_state.messages = current_session.get("messages", [])
        st.session_state.current_session_id = current_session.get("session_id")
        st.session_state.session_title = current_session.get("title", "Nouvelle conversation")

    # Sidebar - Configuration et gestion
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Sélecteur de modèle
        st.subheader("🧠 Sélection du Modèle")

        # Rafraîchir la liste des modèles
        if st.button("🔄 Rafraîchir la liste", key="refresh_models_btn"):
            st.session_state.available_models = st.session_state.agent.get_available_models()
            st.rerun()

        if st.session_state.available_models:
            selected_model = st.selectbox(
                "Choisir un modèle:",
                options=st.session_state.available_models,
                index=st.session_state.available_models.index(st.session_state.current_model)
                if st.session_state.current_model in st.session_state.available_models else 0,
                key="model_selector"
            )

            # Changer de modèle si sélection différent
            if selected_model != st.session_state.current_model:
                if st.button(f"🔁 Passer à {selected_model}", key=f"switch_model_{selected_model}"):
                    if st.session_state.agent.change_model(selected_model):
                        st.session_state.current_model = selected_model
                        st.success(f"✅ Modèle changé: {selected_model}")
                        st.rerun()
                    else:
                        st.error("❌ Erreur changement de modèle")

            # Afficher info modèle actuel
            st.info(f"**Modèle actuel:** {st.session_state.current_model}")
        else:
            st.warning("⚠️ Aucun modèle trouvé. Vérifiez qu'Ollama est démarré.")

        st.divider()

        # BOUTON NOUVELLE CONVERSATION
        st.header("🆕 Nouvelle Conversation")

        col1, col2 = st.columns([2, 1])
        with col1:
            new_convo_model = st.selectbox(
                "Modèle pour nouvelle conversation:",
                options=st.session_state.available_models,
                key="new_convo_model_selector"
            )
        with col2:
            if st.button("✨ Nouvelle", use_container_width=True, key="new_conversation_btn"):
                # Créer une nouvelle conversation
                new_session_id = st.session_state.agent.create_new_conversation(new_convo_model)

                # Mettre à jour l'interface
                st.session_state.messages = []
                st.session_state.current_model = new_convo_model
                st.session_state.current_session_id = new_session_id
                st.session_state.session_title = f"Conversation avec {new_convo_model}"

                st.success("🆕 Nouvelle conversation créée!")
                st.rerun()

        st.divider()

        # Gestion des sessions historiques
        st.header("📚 Sessions Précédentes")

        sessions = st.session_state.agent.list_all_sessions()

        if not sessions:
            st.info("Aucune session précédente")
        else:
            for i, session in enumerate(sessions[:10]):  # 10 dernières sessions
                is_current = session["session_id"] == st.session_state.current_session_id

                col1, col2 = st.columns([3, 1])
                with col1:
                    session_title = session.get("title", "Sans titre")
                    if is_current:
                        st.write(f"**🔵 {session_title}**")
                    else:
                        st.write(f"⚪ {session_title}")

                    st.caption(f"{session.get('message_count', 0)} messages")
                    st.caption(f"Modèle: {session.get('model_used', 'Inconnu')}")
                    st.caption(f"Dernière activité: {session.get('last_activity', '')[:16]}")

                with col2:
                    if not is_current:
                        # CLÉ UNIQUE avec index pour éviter les doublons
                        if st.button("📥", key=f"load_session_{i}_{session['session_id']}"):
                            if st.session_state.agent.switch_to_session(session["session_id"]):
                                st.session_state.messages = st.session_state.agent.current_conversation
                                st.session_state.current_session_id = session["session_id"]
                                st.session_state.session_title = session.get("title", "Session")
                                st.session_state.current_model = session.get("model_used", "llama3.2:1b")
                                st.success("✅ Session chargée!")
                                st.rerun()

        st.divider()

        # Section gestion des conversations (sauvegarde manuelle)
        st.header("💾 Sauvegarde Manuelle")

        with st.form("sauvegarde_form", clear_on_submit=True):
            titre_sauvegarde = st.text_input("Titre de sauvegarde",
                                           value=st.session_state.session_title,
                                           key="save_title_input")
            if st.form_submit_button("💾 Sauvegarder Conversation", use_container_width=True):
                if st.session_state.agent.current_conversation:
                    result = st.session_state.agent.sauvegarder_conversation_actuelle(titre_sauvegarde)
                    if result["status"] == "success":
                        st.success(f"✅ Conversation sauvegardée: {result['fichier']}")
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.warning("⚠️ Aucune conversation à sauvegarder")

        st.divider()

        # Informations système
        st.subheader("📊 Informations Système")
        st.write(f"**Session:** {st.session_state.session_title}")
        st.write(f"**Modèles disponibles:** {len(st.session_state.available_models)}")
        st.write(f"**Sessions totales:** {len(sessions)}")
        st.write(f"**Messages actuels:** {len(st.session_state.messages)}")

        # Bouton export historique complet
        if st.button("📤 Exporter Historique Complet", key="export_history_btn"):
            export_file = st.session_state.manager.export_session_history()
            st.success(f"✅ Historique exporté: {export_file.name}")

    # Zone de chat principale
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.header("💬 Conversation Actuelle")
    with col2:
        st.metric("Modèle", st.session_state.current_model)
    with col3:
        st.metric("Messages", len(st.session_state.messages))

    # Afficher le titre de la session actuelle
    if st.session_state.session_title and st.session_state.session_title != "Nouvelle conversation":
        st.subheader(f"📝 {st.session_state.session_title}")

    # Afficher les messages avec indication du modèle
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message("user" if message['role'] == 'user' else "assistant"):
            if message['role'] == 'assistant':
                st.caption(f"Modèle: {st.session_state.current_model}")
            st.write(message['content'])

    # Input utilisateur
    chat_input_placeholder = st.empty()
    if prompt := chat_input_placeholder.chat_input(f"Tapez votre message pour {st.session_state.current_model}...", key="chat_input"):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.write(prompt)

        # Obtenir la réponse
        with st.chat_message("assistant"):
            st.caption(f"Modèle: {st.session_state.current_model}")
            with st.spinner("🤔 Réflexion en cours..."):
                reponse = st.session_state.agent.envoyer_message(prompt)
                st.write(reponse)

        # Mettre à jour l'affichage et le titre de session
        st.session_state.messages = st.session_state.agent.current_conversation

        # Mettre à jour le titre de session basé sur le premier message
        if len(st.session_state.messages) == 2:  # Après premier échange
            first_message = st.session_state.messages[0]['content']
            new_title = first_message[:30] + "..." if len(first_message) > 30 else first_message
            st.session_state.session_title = new_title

        st.rerun()

if __name__ == "__main__":
    main()
