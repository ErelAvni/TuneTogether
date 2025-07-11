from dotenv import load_dotenv
import os, sys

# Load environment variables from .env file
here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(here, "..", ".."))  # Adjust the path to your project root
load_dotenv(os.path.join(project_root, ".env"))

if project_root not in sys.path:
    sys.path.append(project_root)
    sys.path.insert(0, project_root)

import tkinter as tk
from new.Client.client_new import Client
from new.Client.login_page import LoginPage
from new.Client.register_page import RegisterPage
from new.Client.main_page import MainPage
from new.Client.comment_page import CommentPage
from new.Client.live_chat_page import LiveChatPage
from tkinter import messagebox


class MainApp(tk.Tk):
    def __init__(self, host: str = '127.0.0.1', port: int = 65432):
        """Initialize the main application window."""
        super().__init__()
        self.title("TuneTogether")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.frames = {}

        # Create a Client instance
        self.client = Client(host, port)

        try :
            self.client.connect()
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return

        self.show_frame("LoginPage")


    def show_frame(self, page_name, song_name=None):
        # Destroy the current page if it exists
        for frame in self.frames.values():
            frame.destroy()

        else:
            if page_name == "MainPage":
                messagebox.showinfo("Sucsess", f"Loading {page_name}...")
                frame = MainPage(parent=self, controller=self, connected_client=self.client)
            elif page_name == "RegisterPage":
                messagebox.showinfo("Sucsess", f"Loading {page_name}...")
                frame = RegisterPage(parent=self, controller=self, connected_client=self.client)
            elif page_name == "LoginPage":
                frame = LoginPage(parent=self, controller=self, connected_client=self.client)
            elif page_name == "CommentPage":
                if song_name == None:
                    raise ValueError("song_name must be provided for CommentPage")
                else:
                    messagebox.showinfo("Sucsess", f"Loading {page_name}...")
                    frame = CommentPage(parent=self, controller=self, connected_client=self.client, song_name=song_name)
            elif page_name == "LiveChatPage":
                messagebox.showinfo("Sucsess", f"Loading {page_name}...")
                frame = LiveChatPage(parent=self, controller=self, connected_client=self.client)
            else:
                raise ValueError(f"Unknown page name: {page_name}")
            
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)


    def on_close(self):
            """Handle application close event."""
            if self.client:
                self.client.close()
                print("Connection closed.")
            self.destroy()


if __name__ == "__main__":
    app = MainApp('192.168.1.142')
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close event
    app.mainloop()