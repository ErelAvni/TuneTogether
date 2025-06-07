import tkinter as tk
from PIL import Image, ImageTk
from new.Client.client_new import Client
from tkinter import messagebox
from new.Client.page import Page
import pygame
from new.Client.song import Song
import new.shared.DButilites as DButilities
import os
from new.shared.server_request_new import ServerRequest, GET_ALL_SONG_RATINGS, UPDATE_SONG_RATING


class MainPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        super().create_top_bar(connected_client.username)  # Create the top bar with username
        self.mixer = pygame.mixer  # Use pygame's mixer for audio playback
        self.mixer.init()  # Initialize the mixer
        self.mixer_music = self.mixer.music
        self.current_loaded_song = None  # Track the currently loaded song
        self.song_boxes = {}  # song_name: song_box_frame mapping

        images_path = os.path.join(os.path.dirname(__file__), "images")
        self.images_abs_path = os.path.abspath(images_path)

        self.full_star_image = Image.open(os.path.join(self.images_abs_path, "full_star.png")).resize((20, 20), Image.Resampling.LANCZOS)
        self.empty_star_image = Image.open(os.path.join(self.images_abs_path, "empty_star.png")).resize((20, 20), Image.Resampling.LANCZOS)
        self.full_star_tk = ImageTk.PhotoImage(self.full_star_image)
        self.empty_star_tk = ImageTk.PhotoImage(self.empty_star_image)

        self.create_grid()


        # Title Label
        title_frame = tk.Frame(self, bg="#95DBCD")
        title_frame.place(relx=0.5, rely=0.2, anchor="center")  # Center the title frame
        title_frame.lift()  # Move the title frame to the front
        title = tk.Label(title_frame, text="TuneTogether", font=("Arial", 50, "bold"), bg="#95DBCD")
        title.pack()

        # live chat button
        live_chat_button = tk.Button(self.top_bar, text="Live Chat", font=("Arial", 20), bg="#4CAF50", fg="white", command=lambda:self.controller.show_frame("LiveChatPage"))
        live_chat_button.pack(side=tk.RIGHT, padx=10, pady=5)  # Add padding to the button


    def on_frame_configure(self, event):
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))


    # --- Keep the frame width in sync with canvas width ---
    def on_canvas_resize(self, event):
        grid_canvas.itemconfig(grid_window_id, width=event.width)


    # --- Mouse wheel scroll (Windows only) ---
    def on_mousewheel(self, event):
        grid_canvas.yview_scroll(-1 * int(event.delta / 120), "units")


    def create_grid(self):
        # Create a grid layout for the song boxes
        # Example song list
        print("Creating grid")
        try:
            self.song_dict = {}
            song_names = ["Comfortably Numb", "Billie Jean", "Echoes", "Bring Me To Life", "Call Me Maybe", "Lose Yourself", "Red Swan", "Superstition", "Three Little Birds"]

            for song_name in song_names:
                # Create a Song object for each song
                request = ServerRequest(GET_ALL_SONG_RATINGS, {"song_name": song_name})
                response = self.connected_client.send_request(request)
                if response.response_code != "OK":
                    print(f"Error fetching song ratings for {song_name}: {response.message}")
                    continue
                song_ratings = response.song_ratings if response.song_ratings else {}
                print(response.to_dict())
                song = Song(song_name, song_ratings)
                self.song_dict[song_name] = song  # Store the song object in a dictionary

            # --- Canvas dimensions (smaller than window) ---
            canvas_width = 850
            canvas_height = 400
            global grid_canvas
            grid_canvas = tk.Canvas(self.content_frame, width=canvas_width, height=canvas_height, bg='lightgrey')
            grid_canvas.pack(padx=20, pady=100)
            # --- Vertical Scrollbar ---
            scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=grid_canvas.yview)
            scrollbar.place(in_=grid_canvas, relx=1.0, rely=0, relheight=1.0, anchor='ne')
            grid_canvas.configure(yscrollcommand=scrollbar.set)

            # Create a container frame to hold the grid
            grid_frame = tk.Frame(grid_canvas, bg="#95DBCD")
            global grid_window_id
            grid_window_id = grid_canvas.create_window(canvas_width//2, 0, window=grid_frame, anchor="n")

            # Grid configuration
            cols = 3

            for i in range(len(self.song_dict) // cols + 1):
                grid_frame.grid_rowconfigure(i, minsize=220)
            for j in range(cols):
                grid_frame.grid_columnconfigure(j, minsize=270)

            for index, song in enumerate(self.song_dict.values()):
                row = index // cols
                col = index % cols
                self.create_song_box_in_frame(grid_frame, song, row, col)

            grid_frame.bind("<Configure>", self.on_frame_configure)
            grid_canvas.bind("<Configure>", self.on_canvas_resize)
            grid_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        except Exception as e:
            print(f"Error creating grid: {e}")


    def create_song_box_in_frame(self, frame, song : Song, row, col):
        # Create a frame for each box inside the given frame
        box_frame = tk.Frame(frame, bg="#95DBCD", bd=1, relief=tk.RAISED, width=100, height=50)

        # Prevent the frame from resizing to fit its children
        box_frame.grid_propagate(False)
    
        box_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # Title Label
        title_label = tk.Label(box_frame, text=song.song_name, bg="#95DBCD", anchor="center")
        title_label.pack(pady=5)

        # song image
        try:
            song_image = song.album_cover  # Assuming this is a PIL Image object
            song_image_tk = ImageTk.PhotoImage(song_image)
            song_image_button = tk.Button(
                box_frame,
                image=song_image_tk,
                borderwidth=0,
                highlightthickness=0,
                bg="#95DBCD",
                activebackground="#95DBCD",
                command=lambda: self.display_song_info(song)  # Placeholder for the function
            )
            song_image_button.image = song_image_tk  # Keep a reference to prevent garbage collection
            song_image_button.pack(pady=5)

        except Exception as e:
            print(f"Error loading song image: {e}")

        # Display user's star rating (interactive)
        try:
            self.display_user_star_rating(box_frame, song)
        except Exception as e:
            print(f"Error loading user star rating: {e}")

        # Load the play button image
        play_image_path = os.path.join(self.images_abs_path, "play_icon.png")
        try:
            play_image = Image.open(play_image_path).resize((32, 32))
            play_image_tk = ImageTk.PhotoImage(play_image)
        except Exception as e:
            print(f"Error loading play image: {e}")
            return

        # Create the play button
        play_button = tk.Button(
            box_frame,
            image=play_image_tk,
            borderwidth=0,
            highlightthickness=0,
            bg="#95DBCD",
            activebackground="#95DBCD",
            command=lambda: self.song_button(box_frame, song)  # Pass the button and state
        )

        play_button.image = play_image_tk  # Keep a reference to prevent garbage collection
        play_button.pack(side=tk.LEFT, padx=5, pady=(5, 8))

        # Store the play button and state in the frame
        box_frame.play_button = play_button
        box_frame.is_playing = False  # Initial state is not playing

        # Store the frame in the dictionary for state management
        self.song_boxes[song] = box_frame

        # Comment Button
        comment_button = tk.Button(box_frame, text="Comment", width=10, command=lambda: self.controller.show_frame("CommentPage", song_name=song.song_name))
        comment_button.pack(side=tk.RIGHT, padx=5, pady=5)


    def display_user_star_rating(self, parent_frame, song: Song):
        selected_rating = tk.IntVar(value=song.song_ratings.get(self.username, 0))

        # --- Average Rating Display ---
        avg_star_img = song.get_star_image().resize((100, 20))  # match display size
        avg_star_tk = ImageTk.PhotoImage(avg_star_img)
        avg_star_label = tk.Label(parent_frame, image=avg_star_tk, bg="#95DBCD")
        avg_star_label.image = avg_star_tk  # prevent GC
        avg_star_label.pack()

        # --- User Rating Buttons ---
        star_buttons = []
        button_frame = tk.Frame(parent_frame, bg="#95DBCD")
        button_frame.pack()

        def update_stars(rating):
            selected_rating.set(rating)
            for i, btn in enumerate(star_buttons):
                img = self.full_star_tk if i < rating else self.empty_star_tk
                btn.config(image=img)

            # Update in-memory and save to file
            db_data = DButilities.load_data_from_json(DButilities.SONG_RATINGS_PATH)
            if song.song_name not in db_data:
                db_data[song.song_name] = {}
            db_data[song.song_name][self.username] = rating
            DButilities.update_data_to_json(db_data, DButilities.SONG_RATINGS_PATH, manual_update=True)

            request = ServerRequest(UPDATE_SONG_RATING, {"song_name": song.song_name, "username": self.username, "rating": rating})
            response = self.connected_client.send_request(request)

            # Update song.all_ratings and refresh average
            song.update_song_ratings(response.song_ratings)

            # Refresh average image
            new_avg_image = song.get_star_image().resize((100, 20))
            new_avg_tk = ImageTk.PhotoImage(new_avg_image)
            avg_star_label.configure(image=new_avg_tk)
            avg_star_label.image = new_avg_tk  # update reference

        # Create star buttons for user rating
        for i in range(5):
            img = self.full_star_tk if i < selected_rating.get() else self.empty_star_tk
            btn = tk.Button(button_frame, image=img, bg="#95DBCD", borderwidth=0,
                            command=lambda rating=i+1: update_stars(rating))
            btn.image = img
            btn.pack(side=tk.LEFT, padx=1)
            star_buttons.append(btn)



    def display_song_info(self, song: Song):
        """Display song information in a new window."""
        info_window = tk.Toplevel(self)
        info_window.title("Song Info")
        info_window.geometry("300x200")
        info_window.configure(bg="#95DBCD")

        # Display song details
        artist_label = tk.Label(info_window, text=f"Artist: {song.artist}", bg="#95DBCD")
        artist_label.pack(pady=5)

        duration_label = tk.Label(info_window, text=f"Duration: {song.song_duration}", bg="#95DBCD")
        duration_label.pack(pady=5)

        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack(pady=10)


    def song_button(self, box_frame, song: Song):
        """Handle the play/stop functionality for a song."""
        if box_frame.is_playing:
            # Stop the song
            self.pause_song(song)
            self.update_button_to_play(box_frame)
            box_frame.is_playing = False
        else:
            # Stop all other songs
            for other_song, other_box in self.song_boxes.items():
                if other_box != box_frame:
                    self.update_button_to_play(other_box)
                    other_box.is_playing = False

            # Play the clicked song
            self.play_song(song)
            self.update_button_to_stop(box_frame)
            box_frame.is_playing = True


    def update_button_to_play(self, box_frame):
        """Update the play button in the song box to the play state."""
        play_image_path = os.path.join(self.images_abs_path, "play_icon.png")
        try:
            play_image = Image.open(play_image_path).resize((32, 32))
            play_image_tk = ImageTk.PhotoImage(play_image)
        except Exception as e:
            print(f"Error loading play image: {e}")
            return

        # Update the play button image
        box_frame.play_button.config(
            image=play_image_tk,
            command=lambda: self.song_button(box_frame, self.get_song_from_box(box_frame))  # Switch to stop
        )
        box_frame.play_button.image = play_image_tk  # Keep a reference to prevent garbage collection
   
   
    def play_song(self, song: Song):
        """Start the song playback."""
        try:
            print(f"Playing song: {song.song_name}")
            if self.current_loaded_song == None or song != self.current_loaded_song:
                self.mixer_music.load(song.song_audio_file_path)  # Load the song
                self.mixer_music.play()
                self.current_loaded_song = song  # Update the currently loaded song

            elif song == self.current_loaded_song:
                # If the same song is already loaded, just resume playback
                self.mixer_music.unpause()
                
        except pygame.error as e:
            print(f"Pygame error playing song: {e}")
            messagebox.showerror("Playback Error", f"Could not play the song: {e}")

        except Exception as e:
            print(f"Error playing song: {e}")
            messagebox.showerror("Playback Error", f"Could not play the song: {e}")
        

    def update_button_to_stop(self, box_frame):
        """Update the play button in the song box to the stop state."""
        stop_image_path = os.path.join(self.images_abs_path, "stop_icon.png")
        try:
            stop_image = Image.open(stop_image_path).resize((32, 32))
            stop_image_tk = ImageTk.PhotoImage(stop_image)
        except Exception as e:
            print(f"Error loading stop image: {e}")
            return

        # Update the play button image
        box_frame.play_button.config(
            image=stop_image_tk,
            command=lambda: self.song_button(box_frame, self.get_song_from_box(box_frame))  # Switch to play
        )
        box_frame.play_button.image = stop_image_tk  # Keep a reference to prevent garbage collection


    def pause_song(self, song: Song):
        """Stop the song playback."""
        if self.current_loaded_song != song:
            print("No song is currently loaded.")
            return
        try:
            self.mixer_music.pause()  # Stop the mixer
        except pygame.error as e:
            print(f"Error stopping song: {e}")
            messagebox.showerror("Playback Error", f"Could not stop the song: {e}")
        except Exception as e:
            print(f"Error stopping song: {e}")
            messagebox.showerror("Playback Error", f"Could not stop the song: {e}")

    
    def get_song_from_box(self, box_frame):
        """Retrieve the song associated with a given song box."""
        for song, box in self.song_boxes.items():
            if box == box_frame:
                return song
        return None
    

    def destroy(self):
        """
        Stop the mixer and clean up resources when the page is destroyed.
        """
        try:
            if self.mixer_music.get_busy():  # Check if the mixer is playing
                self.mixer_music.stop()  # Stop the mixer
            print("Mixer stopped.")
        except Exception as e:
            print(f"Error stopping mixer: {e}")
        finally:
            super().destroy()  # Call the parent class's destroy method