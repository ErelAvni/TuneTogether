import tkinter as tk
from PIL import Image, ImageTk
from client_new import Client
from tkinter import messagebox
from page import Page
import os

class MainPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        self.create_grid()


    # Title Label
        title_frame = tk.Frame(self, bg="#95DBCD")
        title_frame.place(relx=0.5, rely=0.1, anchor="center")  # Center the title frame
        title_frame.lift()  # Move the title frame to the front
        title = tk.Label(title_frame, text="TuneTogether", font=("Arial", 50, "bold"), bg="#95DBCD")
        title.pack()


    def create_grid(self):
        # Create a grid layout for the song boxes
        # Example song list
        self.song_list = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5", "Song 6"]
        
        # Create a container frame to hold the grid
        grid_frame = tk.Frame(self, bg="#95DBCD")
        grid_frame.pack(padx=200, pady=200)  # Add padding to move the grid as a whole
        grid_frame.lower()  # Move the grid frame to the back

        # Grid configuration
        rows = 2
        cols = 3

        for index, song_title in enumerate(self.song_list):
            row = index // cols
            col = index % cols
            self.create_song_box_in_frame(grid_frame, song_title, row, col)


    def create_song_box_in_frame(self, frame, song_title, row, col):
        # Create a frame for each box inside the given frame
        print("Creating song box in frame")
        box_frame = tk.Frame(frame, bg="#95DBCD", bd=1, relief=tk.SUNKEN)

        box_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # Title Label
        title_label = tk.Label(box_frame, text=song_title, bg="#95DBCD", anchor="center")
        title_label.pack(pady=5)

        # Load the play button image using Pillow
        image_path = "new\\images\\play_icon.png"  # Relative path to the image
        try:
            play_image = Image.open(image_path)
            play_image = play_image.resize((32, 32))  # Resize the image if needed
            play_image_tk = ImageTk.PhotoImage(play_image)  # Convert to PhotoImage for Tkinter
        except Exception as e:
            print(f"Error loading image: {e}")
            return  # Exit the function if the image cannot be loaded

        # Buttons
        play_button = tk.Button(box_frame, width=32, height=32)
        play_button.image = play_image_tk  # Keep a reference to the image to prevent garbage collection
        play_button.pack(side=tk.RIGHT, padx=5, pady=5)  # Set the button size to match the image
        comment_button = tk.Button(box_frame, text="Comment", width=10)
        comment_button.pack(side=tk.LEFT, padx=5, pady=5)
