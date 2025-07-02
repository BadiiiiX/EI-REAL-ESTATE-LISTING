from src.ui.Controllers.AdController import AdController
from src.ui.Controllers.HistoryController import HistoryController
from src.ui.Controllers.PredictionController import PredictionController

class AppController:
    def __init__(self, left_panel, right_panel, center_panel, api_url):

        self.api_url = api_url

        self.left = left_panel
        self.right = right_panel
        self.center = center_panel
        self.ad_controller = AdController(self.api_url, left_panel)
        self.history_controller = HistoryController(self.api_url, right_panel)
        self.prediction_controller = PredictionController(center_panel)

        self.__handle_left_panel()
        self.__handle_right_panel()

    def __handle_left_panel(self):
        self.left.on_upload_clicked = self.on_upload_ad
        self.left.on_ad_selected = self.on_select_ad

    def __handle_right_panel(self):
        self.right.on_history_selected = self.on_history

    def on_upload_ad(self, path):
        self.ad_controller.on_upload(path)

    def on_select_ad(self, ad_id):
        ad = self.ad_controller.on_select(ad_id)
        if ad is not None:
            histories = self.history_controller.load_histories(ad["code"])

            if len(histories) > 0:
                self.prediction_controller.update_graph(ad, histories)
            else:
                self.center.clear_graph(f"{ad['type']} - {ad['id']} | {ad['region']}")


    def on_history(self, history_date):
        self.history_controller.load_history(history_date)