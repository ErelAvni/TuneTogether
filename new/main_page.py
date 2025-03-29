import tkinter as tk
from client_new import Client
from page import Page
import hashlib
from server_request_new import ServerRequest
from server_response import ServerResponse
from tkinter import messagebox

class MainPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")


    # Title Label
        self.title_label = tk.Label(self, text="TUNE TOGETHER", font=self.title_font, bg="#95DBCD")
        self.title_label.pack(pady=30)

    
    def _create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                if index < len(self.song_list):
                    song_title = self.song_list[index]
                    self._create_box(i, j, song_title)


    def _create_box(self, row, col, song_title):
        # Create a frame for each box
        box_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=1)
        box_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Configure row and column weights for the box frame
        box_frame.grid_rowconfigure(0, weight=1)  # For the title
        box_frame.grid_rowconfigure(1, weight=1)  # For the buttons
        box_frame.grid_columnconfigure(0, weight=1) # For the play button
        box_frame.grid_columnconfigure(1, weight=1) # For the comment button

        # Title Label (top half)
        title_label = tk.Label(box_frame, text=song_title, anchor="center", wraplength=150)
        title_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Play Button (bottom-left)
        play_button = tk.Button(box_frame, text="Play", command=lambda t=song_title: self._play_song(t))
        play_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Comment Button (bottom-right)
        comment_button = tk.Button(box_frame, text="Comment", command=lambda t=song_title: self._comment_song(t))
        comment_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)