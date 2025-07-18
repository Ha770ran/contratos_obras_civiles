import webbrowser
import time
from app import app

if __name__ == "__main__":
    # Espera 1 segundo para dar tiempo a levantar el servidor
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()

