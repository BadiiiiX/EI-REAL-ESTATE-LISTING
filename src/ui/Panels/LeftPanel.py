import tkinter as tk
from tkinter import ttk, filedialog

FIELD_MAP = {
    "Identifier": "id",
    "Price": "price",
    "Area": "area",
    "Code": "code",
    "Region": "region",
    "Type": "type"
}

class LeftPanel(ttk.Frame):

    def __init__(self, parent, on_ad_selected=None, on_upload_clicked=None):
        super().__init__(parent, width=200)

        self.on_ad_selected = on_ad_selected
        self.on_upload_clicked = on_upload_clicked
        self.ad_list = set()

        self.pack(side="left", fill="y")

        ttk.Button(self, text="Charger une annonce", command=self.handle_upload).pack(pady=5)

        self.annonce_list = tk.Listbox(self)
        self.load_list()

        info_frame = ttk.LabelFrame(self, text="Information")
        info_frame.pack(padx=5, pady=5, fill="both")

        self.info_entries = {}
        for label in ["Identifier", "Price", "Area", "Code", "Region", "Type"]:
            ttk.Label(info_frame, text=label).pack(anchor="w")
            entry = ttk.Entry(info_frame, state="readonly")
            entry.pack(fill="x", padx=2)
            self.info_entries[label] = entry

        self.annonce_list.bind("<<ListboxSelect>>", self.on_select)

    def load_list(self):
        self.annonce_list.delete(0, tk.END)
        for item in sorted(self.ad_list):
            self.annonce_list.insert("end", item)
        self.annonce_list.pack(padx=5, pady=5, fill="y", expand=True)

    def handle_upload(self):
        path = filedialog.Open(self).show()
        if path and path.endswith('.html'):
            if callable(self.on_upload_clicked):
                self.on_upload_clicked(path)

    def on_select(self, event):
        selection = self.annonce_list.curselection()
        if selection:
            ad_id = self.annonce_list.get(selection[0])
            if callable(self.on_ad_selected):
                self.on_ad_selected(ad_id)

    def update_info(self, ad_info: dict):
        for display_key, data_key in FIELD_MAP.items():
            entry = self.info_entries[display_key]
            value = ad_info.get(data_key, "")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            entry.config(state="readonly")

    def refresh(self):
        self.load_list()