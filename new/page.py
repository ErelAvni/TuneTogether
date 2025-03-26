import tkinter as tk
from tkinter import messagebox
from client_new import Client


class Page(tk.Frame):
    def __init__(self, parent, controller, connected_client: Client, bg_param="#95DBCD"):
        super().__init__(parent, bg=bg_param)
        self.controller = controller
        self.connected_client = connected_client

        # Custom Fonts
        self.title_font = ("Arial", 50, "bold")
        self.label_font = ("Arial", 20)
        self.button_font = ("Arial", 20)