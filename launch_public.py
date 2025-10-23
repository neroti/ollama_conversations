
# launch_public.py
from pyngrok import ngrok
import subprocess
import time
import os

def main():
    # Port sur lequel Streamlit écoute
    port = 8501

    # Démarrer ngrok
    public_url = ngrok.connect(port, bind_tls=True)
    print(f"🔗 Tunnel ngrok créé : {public_url}")

    # Démarrer Streamlit
    streamlit_cmd = ["streamlit", "run", "app.py", "--server.port", str(port), "--server.address", "0.0.0.0"]
    process = subprocess.Popen(streamlit_cmd)

    try:
        # Garder le script en vie
        while process.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Arrêt en cours...")
        process.terminate()
        ngrok.disconnect(public_url)
        ngrok.kill()

if __name__ == "__main__":
    main()
