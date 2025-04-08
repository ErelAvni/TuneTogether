import tkinter as tk
from tkinter import messagebox
from client_new import Client
from page import Page
from server_request_new import ServerRequest
import hashlib
from server_response import ServerResponse

class RegisterPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD", show_top_bar=False)

        # Title Label
        self.title_label = tk.Label(self, text="REGISTER", font=self.title_font, bg="#95DBCD")
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

        # Age Label and Entry
        self.age_label = tk.Label(self, text="Enter Age:", font=self.label_font, bg="#95DBCD")
        self.age_label.pack()
        self.age_entry = tk.Entry(self, font=self.label_font, bg="#BFC6C7", width=20)
        self.age_entry.pack(pady=5)

        # Register Button
        self.login_button = tk.Button(self, text="Register", font=self.button_font, bg="#639A97", fg="white", width=20, height=1, command=lambda: self.register(self.username_entry.get(), self.password_entry.get(), self.age_entry.get()))
        self.login_button.pack(pady=(30, 15))

        # Login Section
        self.register_frame = tk.Frame(self, bg="#95DBCD")
        self.register_frame.pack(side="bottom", pady=(0, 50))
        
        self.register_text = tk.Label(self.register_frame, text="Already a member?", font=self.label_font, bg="#95DBCD")
        self.register_text.pack()
        
        self.register_button = tk.Button(self.register_frame, text="Login", font=self.button_font, bg="#639A97", fg="white", width=20, height=1, command=lambda: controller.show_frame("LoginPage"))
        self.register_button.pack(pady=10)

    
    def hash_password(self, password: str):
        '''hashes the password using the SHA-256 algorithm'''
        return hashlib.sha256(password.encode()).hexdigest()


    def register(self, username: str, password: str, age: int):
        '''Sends a register request to the server'''
        print(f"username: {username}, password: {password}, age: {age}")
        password_hash = self.hash_password(password)
        request = ServerRequest.create_register_payload(username, password_hash, age)
        response = self.connected_client.send_request(request)
        self.handle_response(response)


    def handle_response(self, response: ServerResponse):
        """
        Handle the server response.
        :param response: The server response to handle.
        """
        if response.response_code == "OK":
            messagebox.showinfo("Success", "register successful!")
            # Proceed to the next page or functionality
            self.controller.show_frame("MainPage")
        else:
            super().handle_response(response)