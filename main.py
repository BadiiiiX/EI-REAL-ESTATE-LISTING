import threading

from src.ui.MainApp import MainApp
from src.ws.RestApi import RestApi


import src.ws.Controllers.AdController
import src.ws.Controllers.HistoryController

API_URL = "127.0.0.1"
PORT = 8090

def start_api():
    RestApi.get_instance().run(host=API_URL, port=PORT)

if __name__ == "__main__":
    url = f"http://{API_URL}:{PORT}"

    threading.Thread(target=start_api, daemon=True).start()

    app = MainApp(url)


