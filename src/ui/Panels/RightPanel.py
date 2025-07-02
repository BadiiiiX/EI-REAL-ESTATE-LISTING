import tkinter as tk
from tkinter import ttk

FIELD_MAP = {
    "Identifier": "id",
    "Date": "date",
    "Price": "price",
    "Code": "code",
    "Commune": "commune",
    "Departement": "departement",
    "House area": "houseArea",
    "Rooms": "rooms",
    "Nature": "nature",
    "Area": "area",
}

class RightPanel(ttk.Frame):
    def __init__(self, parent, on_history_selected=None):
        super().__init__(parent, width=220)
        self.pack(side="left", fill="y")

        self.on_history_selected = on_history_selected
        self.date_list = tk.Listbox(self)
        self.dates = set()

        self.load_dates()

        info_frame = ttk.LabelFrame(self, text="Information")
        info_frame.pack(padx=5, pady=5, fill="both")

        self.info_entries = {}
        for label in [
            "Identifier", "Date", "Price", "Code", "Commune", "Departement",
            "House area", "Rooms", "Nature", "Area", "Lot 1", "Lot 2", "Lot 3", "Lot 4"
        ]:
            ttk.Label(info_frame, text=label).pack(anchor="w")
            entry = ttk.Entry(info_frame, state="readonly")
            entry.pack(fill="x", padx=2)
            self.info_entries[label] = entry

        self.date_list.bind("<<ListboxSelect>>", self.on_select)

    def load_dates(self):

        self.date_list.delete(0, tk.END)
        for item in sorted(self.dates):
            self.date_list.insert("end", item)
        self.date_list.pack(padx=5, pady=5, fill="y", expand=True)

    def set_info(self, key, value):
        if key in self.info_entries:
            self.info_entries[key].config(state="normal")
            self.info_entries[key].delete(0, tk.END)
            self.info_entries[key].insert(0, value)
            self.info_entries[key].config(state="readonly")

    def on_select(self, event):
        selection = self.date_list.curselection()
        if selection:
            history_date = self.date_list.get(selection[0])
            if callable(self.on_history_selected):
                self.on_history_selected(history_date)

    def update_info(self, history_info: dict):
        for display_key, data_key in FIELD_MAP.items():
            entry = self.info_entries[display_key]
            value = history_info.get(data_key, "")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            entry.config(state="readonly")

    def reset_dates(self):
        self.dates.clear()

    def refresh(self):
        self.load_dates()