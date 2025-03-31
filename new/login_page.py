import tkinter as tk
from client_new import Client
from page import Page
import hashlib
from server_request_new import ServerRequest
from server_response import ServerResponse
from tkinter import messagebox


class LoginPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD", show_logout_button=False)

        # Custom Fonts
        self.title_font = ("Arial", 50, "bold")
        self.label_font = ("Arial", 20)
        self.button_font = ("Arial", 20)

        # Title Label
        self.title_label = tk.Label(self, text="LOGIN", font=self.title_font, bg="#95DBCD")
        self.title_label.pack(pady=30)

        # Username Label and Entry
        self.username_label = tk.Label(self, text="Enter username:", font=self.label_font, bg="#95DBCD")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, font=self.label_font, bg="#BFC6C7", width=20)
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Enter password:", font=self.label_font, bg="#95DBCD")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, font=self.label_font, bg="#BFC6C7", width=20, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(self, text="Login", font=self.button_font, bg="#639A97", fg="white", width=20, height=1, command=lambda: self.login(self.username_entry.get(), self.password_entry.get()))
        self.login_button.pack(pady=(30, 15))

        # Register Section
        self.register_frame = tk.Frame(self, bg="#95DBCD")
        self.register_frame.pack(side="bottom", pady=(0, 50))
        
        self.register_text = tk.Label(self.register_frame, text="Don't have an account yet?", font=self.label_font, bg="#95DBCD")
        self.register_text.pack()
        
        self.register_button = tk.Button(self.register_frame, text="Register", font=self.button_font, bg="#639A97", fg="white", width=20, height=1, command=lambda: controller.show_frame("RegisterPage"))
        self.register_button.pack(pady=10)


    def login(self, username: str, password: str):
        '''Sends a login request to the server'''
        print(f"username: {username}, password: {password}")
        password_hash = self.hash_password(password)
        request = ServerRequest.create_login_payload(username, password_hash)
        response = self.connected_client.send_request(request)
        self.handle_response(response)

    
    def hash_password(self, password: str):
        '''hashes the password using the SHA-256 algorithm'''
        return hashlib.sha256(password.encode()).hexdigest()
    

    def handle_response(self, response: ServerResponse):
        """
        Handle the server response.
        :param response: The server response to handle.
        """
        if response.response_code == "OK":
            messagebox.showinfo("Success", "Login successful!")
            # Proceed to the next page or functionality
            self.controller.show_frame("MainPage")
        else:
            super().handle_response(response)