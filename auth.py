
# auth.py
import streamlit as st
import os

def check_password():
    """Retourne `True` si l'utilisateur a entré le bon mot de passe ou si aucun mot de passe n'est défini."""

    # Si aucun mot de passe n'est défini dans les variables d'environnement, on saute l'authentification.
    password_env = os.getenv("STREAMLIT_PASSWORD")
    if password_env is None:
        return True

    def password_entered():
        """Vérifie si le mot de passe entré est correct."""
        if st.session_state["password"] == password_env:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Ne pas stocker le mot de passe
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Afficher le champ de mot de passe si le mot de passe n'a pas été entré.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Mot de passe incorrect, afficher à nouveau le champ + message d'erreur.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Mot de passe incorrect")
        return False
    else:
        # Mot de passe correct.
        return True
