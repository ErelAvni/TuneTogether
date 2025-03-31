import tkinter as tk
from tkinter import messagebox
from client_new import Client
from server_response import ServerResponse
from server_request_new import ServerRequest
from abc import ABC, abstractmethod


class Page(tk.Frame):
    def __init__(self, parent, controller, connected_client: Client, username : str = None, bg_param="#95DBCD", show_logout_button: bool = True):
        super().__init__(parent, bg=bg_param)
        self.controller = controller
        self.connected_client = connected_client

        # Custom Fonts
        self.title_font = ("Arial", 50, "bold")
        self.label_font = ("Arial", 20)
        self.button_font = ("Arial", 20)

        self.logout_button(show_logout_button) # Create the logout button

    
    def logout_button(self, show: bool):
        """
        Create a logout button that allows the user to log out of the application.
        """
        if not show:
            return
        logout_button_frame = tk.Frame(self, bg="#95DBCD")
        logout_button_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)  # Positioned in the top-right corner with padding
        logout_button = tk.Button(logout_button_frame, text="Logout", font=self.button_font, command= lambda: self.logout())
        logout_button.pack(pady=5, padx=5)  # Add padding to the button


    def logout(self):
        """
        Handle the logout process.
        """
        # Perform any necessary cleanup or state reset here
        print(f"Logging out user: {self.connected_client.username}")
        if self.connected_client.username:
            print(f"Logging out user: {self.connected_client.username}")
            self.connected_client.send_request(ServerRequest.create_logout_payload(self.connected_client.username))
        else:
            print("No user logged in.")
        self.controller.show_frame("LoginPage")  # Show the login page again


    @abstractmethod
    def handle_response(self, response: ServerResponse):
        """
        Handle the server response.
        :param response: The server response to handle.
        """
        if response.response_code == "OK":
            messagebox.showinfo("Success", "Operation completed successfully.")
        elif response.response_code == "DATA_NOT_FOUND":
            messagebox.showerror("Error", f"Data not found. {response.message}")
        elif response.response_code == "UNAUTHORIZED":
            messagebox.showerror("Error", f"Unauthorized access. {response.message}")
        elif response.response_code == "INVALID_REQUEST":
            messagebox.showerror("Error", f"Invalid request. {response.message}")
        elif response.response_code == "INVALID_DATA":
            messagebox.showerror("Error", f"Invalid data provided. {response.message}")
        elif response.response_code == "INTERNAL_ERROR":
            messagebox.showerror("Error", f"Internal server error. {response.message}")
