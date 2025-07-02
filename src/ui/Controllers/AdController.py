import os
import requests


class AdController:

    def __init__(self, base_uri, left_panel):
        self.base_uri = base_uri
        self.left_panel = left_panel
        self.ad_list = set()
        self.ad_content = {}

    def _add_ad(self, response):
        ad_id = response["id"]
        self.ad_list.add(ad_id)
        self.left_panel.ad_list.add(ad_id)
        self.ad_content[ad_id] = response

    def on_upload(self, file_path: str):
        filename = os.path.basename(file_path)
        url = f"{self.base_uri}/ad/addfile/"
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'text/html')}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            res = response.json()["detail"]
            ad_id = res["id"]
            self._add_ad(res)
            self.left_panel.refresh()

            if callable(self.left_panel.on_ad_selected):
                self.left_panel.on_ad_selected(ad_id)

        else:
            print("Erreur upload :", response.status_code, response.text)

    def on_select(self, ad_id) -> dict | None:
        if ad_id in self.ad_content:
            ad = self.ad_content[ad_id]
            self.left_panel.update_info(ad)
            return ad
        return None
