
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from ollama_agent import OllamaAgent
from model_manager import ModelManager

def advanced_interface():
    st.set_page_config(
        page_title="Gestionnaire Ollama Avancé",
        page_icon="⚡",
        layout="wide"
    )

    st.title("⚡ Gestionnaire Ollama Avancé")

    # Initialisation
    if 'model_manager' not in st.session_state:
        st.session_state.model_manager = ModelManager()
        st.session_state.agent = OllamaAgent()

    # Sidebar principale
    with st.sidebar:
        st.header("🧠 Gestion des Modèles")

        # Section téléchargement
        st.subheader("📥 Télécharger un modèle")
        recommended_models = st.session_state.model_manager.get_recommended_models()
        selected_download = st.selectbox("Modèle recommandé:", recommended_models)

        if st.button("Télécharger le modèle sélectionné"):
            with st.spinner("Téléchargement en cours..."):
                progress_placeholder = st.empty()
                for status in st.session_state.model_manager.pull_model(selected_download):
                    progress_placeholder.text(status)
                st.success(f"✅ {selected_download} téléchargé!")

        # Modèle personnalisé
        custom_model = st.text_input("Ou modèle personnalisé:")
        if st.button("Télécharger modèle personnalisé") and custom_model:
            with st.spinner("Téléchargement en cours..."):
                progress_placeholder = st.empty()
                for status in st.session_state.model_manager.pull_model(custom_model):
                    progress_placeholder.text(status)

    # Contenu principal - Liste des modèles
    st.header("📚 Modèles Installés")

    installed_models = st.session_state.model_manager.get_installed_models()

    if not installed_models:
        st.warning("Aucun modèle installé. Utilisez la sidebar pour en télécharger.")
    else:
        for model in installed_models:
            with st.expander(f"🧩 {model['name']}", expanded=False):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"**Paramètres:** {model.get('parameters', 'N/A')}")
                    st.write(f"**Famille:** {model.get('family', 'N/A')}")
                    st.write(f"**Quantization:** {model.get('quantization', 'N/A')}")

                with col2:
                    if st.button("🎯 Utiliser", key=f"use_{model['name']}"):
                        st.session_state.agent.change_model(model['name'])
                        st.success(f"Modèle changé: {model['name']}")

                with col3:
                    if st.button("🗑️ Supprimer", key=f"del_{model['name']}"):
                        if st.session_state.model_manager.delete_model(model['name']):
                            st.success(f"Modèle {model['name']} supprimé")
                            st.rerun()
                        else:
                            st.error("Erreur suppression")

if __name__ == "__main__":
    advanced_interface()
