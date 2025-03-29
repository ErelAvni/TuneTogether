import tkinter as tk
from tkinter import messagebox
from client_new import Client
from server_response import ServerResponse
from abc import ABC, abstractmethod


class Page(tk.Frame):
    def __init__(self, parent, controller, connected_client: Client, bg_param="#95DBCD"):
        super().__init__(parent, bg=bg_param)
        self.controller = controller
        self.connected_client = connected_client

        # Custom Fonts
        self.title_font = ("Arial", 50, "bold")
        self.label_font = ("Arial", 20)
        self.button_font = ("Arial", 20)

    
    @abstractmethod
    def handle_response(self, response: ServerResponse):
        """
        Handle the server response.
        :param response: The server response to handle.
        """
        if response.response_code == "OK":
            messagebox.showinfo("Success", "Operation completed successfully.")
        elif response.response_code == "DATA_NOT_FOUND":
            messagebox.showerror("Error", "Data not found.")
        elif response.response_code == "UNAUTHORIZED":
            messagebox.showerror("Error", "Unauthorized access.")
        elif response.response_code == "INVALID_REQUEST":
            messagebox.showerror("Error", "Invalid request.")
        elif response.response_code == "INVALID_DATA":
            messagebox.showerror("Error", "Invalid data provided.")
        elif response.response_code == "INTERNAL_ERROR":
            messagebox.showerror("Error", "Internal server error.")