
# app_interface.py
import streamlit as st
from ollama_web_agent import OllamaWebAgent
from conversation_manager import ConversationManager

def main():
    st.title("🤖 Assistant Ollama - Gestion Conversations")

    # Initialisation
    if 'agent' not in st.session_state:
        st.session_state.agent = OllamaWebAgent()
        st.session_state.manager = ConversationManager()

    # Sidebar - Gestion des conversations
    with st.sidebar:
        st.header("💾 Gestion des Conversations")

        # Sauvegarde manuelle
        with st.form("sauvegarde_form"):
            titre_sauvegarde = st.text_input("Titre de sauvegarde")
            if st.form_submit_button("💾 Sauvegarder"):
                if st.session_state.agent.current_conversation:
                    fichier = st.session_state.manager.sauvegarder_conversation(
                        st.session_state.agent.current_conversation,
                        titre_sauvegarde or None
                    )
                    st.success(f"Conversation sauvegardée: {fichier.name}")
                else:
                    st.warning("Aucune conversation à sauvegarder.")

        # Liste des conversations
        st.subheader("📁 Conversations Sauvegardées")
        conversations = st.session_state.manager.lister_conversations()

        for conv in conversations:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{conv['titre']}**")
                st.caption(f"{conv['messages']} messages - {conv['date'][:10]}")
            with col2:
                if st.button("📥", key=f"load_{conv['fichier']}"):
                    conversation_data = st.session_state.manager.charger_conversation(conv['fichier'])
                    if conversation_data:
                        st.session_state.agent.current_conversation = conversation_data['messages']
                        st.rerun()
                    else:
                        st.error("Erreur lors du chargement")

                if st.button("📤", key=f"export_{conv['fichier']}"):
                    export_file = st.session_state.manager.exporter_markdown(conv['fichier'])
                    if export_file:
                        st.success(f"Exporté: {export_file.name}")
                    else:
                        st.error("Erreur lors de l'export")

    # Chat principal
    st.header("💬 Conversation Actuelle")

    # Affichage de l'historique
    for message in st.session_state.agent.current_conversation:
        with st.chat_message("user" if message['role'] == 'user' else "assistant"):
            st.write(message['content'])

    # Input utilisateur
    if prompt := st.chat_input("Votre message..."):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.write(prompt)

        # Obtenir et afficher la réponse
        with st.chat_message("assistant"):
            with st.spinner("Réflexion..."):
                reponse = st.session_state.agent.envoyer_message(prompt)
                st.write(reponse)

if __name__ == "__main__":
    main()
