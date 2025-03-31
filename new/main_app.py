import tkinter as tk
from client_new import Client
from login_page import LoginPage
from register_page import RegisterPage
from main_page import MainPage


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TuneTogether")
        self.geometry("1400x800")
        self.frames = {}

        # Create a Client instance
        self.client = Client()

        try :
            self.client.connect()
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return

        # Initialize frames
        for F in (LoginPage, RegisterPage, MainPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self, connected_client=self.client)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginPage")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


    def on_close(self):
            """Handle application close event."""
            if self.client:
                self.client.close()
                print("Connection closed.")
            self.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close event
    app.mainloop()