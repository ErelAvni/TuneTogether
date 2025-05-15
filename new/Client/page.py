import tkinter as tk
from tkinter import messagebox
from new.Client.client_new import Client
from new.shared.server_response import ServerResponse
from new.shared.server_request_new import ServerRequest
from abc import ABC, abstractmethod


class Page(tk.Frame):
    def __init__(self, parent, controller, connected_client: Client, bg_param="#95DBCD", show_top_bar: bool = True):
        super().__init__(parent, bg=bg_param)
        self.controller = controller
        self.connected_client = connected_client
        self.username = self.connected_client.username

        # Custom Fonts
        self.title_font = ("Arial", 50, "bold")
        self.label_font = ("Arial", 20)
        self.button_font = ("Arial", 20)

        # Create the top bar
        if show_top_bar:
            self.create_top_bar()

        # Create a content frame for page-specific content
        self.content_frame = tk.Frame(self, bg=bg_param)
        self.content_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)  # Positioned below the top bar


    def refresh_page(self, song_name: str):
        """Refresh the current page by reinitializing it."""
        # Get the current page class
        page_class = self.__class__
        # Destroy the current frame
        self.destroy()
        # Recreate the page
        messagebox.showinfo("Success", f"Reloading {page_class.__name__}...")
        if page_class.__name__ == "CommentPage" and song_name is not None:
            new_page = page_class(self.master, self.controller, self.connected_client, song_name=song_name)
        else:
            new_page = page_class(self.master, self.controller, self.connected_client)
        new_page.pack(fill="both", expand=True)
        self.controller.frames[page_class.__name__] = new_page


    def create_top_bar(self, username: str = None, song_name : str = None):
        """
        Create a top bar that contains the username and logout button.
        """
        # Create the top bar frame
        self.top_bar = tk.Frame(self, bg="#4CAF50", height=50)  # Green background for the bar
        self.top_bar.place(relx=0, rely=0, relwidth=1)  # Position it at the top, spanning the full width

        # Display the username
        username_label = tk.Label(self.top_bar, text=f"Logged in as: {username}",
                                font=self.label_font, bg="#4CAF50", fg="white", anchor="w")
        username_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Add the logout button
        logout_button = tk.Button(self.top_bar, text="Logout", font=self.button_font, bg="#F44336", fg="white",
                                command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Add a refresh button to the top bar
        refresh_button = tk.Button(
            self.top_bar,
            text="Refresh",
            bg="#4CAF50",
            fg="white",
            command=lambda:self.refresh_page(song_name=song_name)  # Pass the song name to refresh_page
        )
        refresh_button.pack(side="right", padx=10, pady=5)


    def logout(self):
        """
        Handle the logout process.
        """
        # Perform any necessary cleanup or state reset here
        print(f"Logging out user: {self.connected_client.username}")
        if self.connected_client.username:
            self.connected_client.send_request(ServerRequest.create_logout_payload(self.connected_client.username))
        else:
            print("No user logged in.")
        self.controller.show_frame("LoginPage")  # Show the login page again    


    def logout_button(self):
        """
        Create a logout button that allows the user to log out of the application.
        """
        logout_button_frame = tk.Frame(self, bg="#95DBCD")
        logout_button_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)  # Positioned in the top-right corner with padding
        logout_button = tk.Button(logout_button_frame, text="Logout", font=self.button_font, command= lambda: self.logout())
        logout_button.pack(pady=5, padx=5)  # Add padding to the button


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
