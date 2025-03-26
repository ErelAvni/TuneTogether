import tkinter as tk
from client_new import Client
from login_page import LoginPage
from register_page import RegisterPage


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TuneTogether")
        self.geometry("1400x800")
        self.frames = {}

        # Create a Client instance
        client = Client()

        # Initialize frames
        for F in (LoginPage, RegisterPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self, connected_client=client)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()