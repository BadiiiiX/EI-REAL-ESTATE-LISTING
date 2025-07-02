import requests


class HistoryController:
    def __init__(self, base_uri, right_panel):
        self.base_uri = base_uri
        self.right_panel = right_panel
        self.actual_code = None
        self.histories = {}

    def _add_history(self, code):

        self.right_panel.reset_dates()

        for r in self.histories[code]:
            self.right_panel.dates.add(r["id"])

        self.right_panel.refresh()

    def load_histories(self, code):
        self.actual_code = code

        if not (code in self.histories):
            self.fetch_histories(code)

        self._add_history(code)
        if callable(self.right_panel.on_history_selected) and len(self.histories[code]) > 0:
            self.right_panel.on_history_selected(self.histories[code][0]["id"])

        return self.histories[code]

    def fetch_histories(self, code):
        try :
            url = f"{self.base_uri}/history/{code}"
            response = requests.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                raw = response.json()["detail"]
                final = []

                seen = {}

                for entry in raw:
                    base_id = entry["id"]

                    count = seen.get(base_id, 0)
                    seen[base_id] = count + 1

                    unique_id = base_id if count == 0 else f"{base_id}-{count}"
                    entry["id"] = unique_id

                    final.append(entry)

                self.histories[code] = final

        except Exception as e:
            print(e)

    def get_history_by_id(self, history_id):
        for e in self.histories[self.actual_code]:
            if e["id"] == history_id:
                return e

        return None

    def load_history(self, history_date):
        data = self.get_history_by_id(history_date)

        if data is not None:
            self.right_panel.update_info(data)