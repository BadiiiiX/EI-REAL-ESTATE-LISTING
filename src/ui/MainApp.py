import tkinter as tk

from src.ui.Controllers.AppController import AppController
from src.ui.Panels.CenterPanel import CenterPanel
from src.ui.Panels.LeftPanel import LeftPanel
from src.ui.Panels.RightPanel import RightPanel


class MainApp(tk.Tk):
    def __init__(self, api_url):
        super().__init__()
        self.title("Analyseur d'annonces immobilières")

        self.left_panel = LeftPanel(self)
        self.center_panel = CenterPanel(self)
        self.right_panel = RightPanel(self)

        self.controller = AppController(self.left_panel, self.right_panel, self.center_panel, api_url)

        self.mainloop()