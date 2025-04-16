from page import Page  
import tkinter as tk
from client_new import Client  
from comment import Comment
from song import Song
import db.DButilites

class CommentPage(Page):
    def __init__(self, parent, controller, connected_client: Client, song_name: str):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        super().create_top_bar(connected_client.username)  # Create the top bar with username
        
        all_comments = db.DButilites.load_data_from_json(db.DButilites.COMMENTS_PATH)
        song_comments = all_comments[song_name]

        # Title Label
        title_frame = tk.Frame(self, bg="#95DBCD")
        title_frame.place(relx=0.5, rely=0.2, anchor="center")  # Center the title frame
        title_frame.lift()  # Move the title frame to the front
        title = tk.Label(title_frame, text=song_name, font=("Arial", 50, "bold"), bg="#95DBCD")
        title.pack()
        
        # back button
        back_button = tk.Button(self.top_bar, text="Back", font=("Arial", 20), bg="#4CAF50", fg="white", command=lambda:self.controller.show_frame("MainPage"))
        back_button.pack(side=tk.RIGHT, padx=10, pady=5)  # Add padding to the button

        self.content_frame.place(relx=0.2, rely=0.3, relwidth=1, relheight=0.7)  # Adjust content frame position

        active_canvas = {"canvas": None}

        # LEFT: YouTube comments
        yt_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid')
        tk.Label(yt_frame, text="youtube comments", fg="red", bg="white").pack(anchor="w", padx=10, pady=5)

        yt_canvas = tk.Canvas(yt_frame, width=200, height=300, bg="white", highlightthickness=0)
        yt_scroll = tk.Scrollbar(yt_frame, orient="vertical", command=yt_canvas.yview)
        yt_canvas.configure(yscrollcommand=yt_scroll.set)
        yt_canvas.pack(side="left", fill="both", expand=True)
        yt_scroll.pack(side="right", fill="y")

        yt_inner = tk.Frame(yt_canvas, bg="white")
        yt_canvas.create_window((0, 0), window=yt_inner, anchor='nw')

        song = Song(song_name)
        yt_comments = song.get_comments_by_url()
        if yt_comments is None:
            yt_comments = ["Comments for this song are not available outside of Youtube."]
        for comment in yt_comments:
            text = comment.__repr__()
            tk.Label(yt_inner, text=text, bg="#d3d3d3", anchor="w", justify="left", wraplength=180).pack(fill="x", padx=5, pady=3)

        yt_inner.bind("<Configure>", lambda e: yt_canvas.configure(scrollregion=yt_canvas.bbox("all")))
        yt_canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": yt_canvas}))
        yt_canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == yt_canvas else None)
        yt_frame.grid(row=0, column=0, padx=10)

        # CENTER: Add comment
        add_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid', padx=10, pady=10)
        add_frame.grid(row=0, column=1, padx=10)

        tk.Label(add_frame, text="add comment", bg="white").pack()
        tk.Label(add_frame, text="comment data", bg="white").pack()
        tk.Text(add_frame, height=6, width=30, bg="#d3d3d3").pack(pady=5)
        tk.Button(add_frame, text="COMMENT", bg="#4b9c97", fg="white").pack()

        # RIGHT: TuneTogether comments
        tt_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid')
        tk.Label(tt_frame, text="tune together comments", bg="white").pack(anchor="w", padx=10, pady=5)

        tt_canvas = tk.Canvas(tt_frame, width=200, height=300, bg="white", highlightthickness=0)
        tt_scroll = tk.Scrollbar(tt_frame, orient="vertical", command=tt_canvas.yview)
        tt_canvas.configure(yscrollcommand=tt_scroll.set)
        tt_canvas.pack(side="left", fill="both", expand=True)
        tt_scroll.pack(side="right", fill="y")

        tt_inner = tk.Frame(tt_canvas, bg="white")
        tt_canvas.create_window((0, 0), window=tt_inner, anchor='nw')

        for comment_dict in song_comments:
            comment = Comment.from_dict(comment_dict)
            text = comment.__repr__()
            print(text)
            tk.Label(tt_inner, text=text, bg="#d3d3d3", anchor="w", justify="left", wraplength=180).pack(fill="x", padx=5, pady=3)

        tt_inner.bind("<Configure>", lambda e: tt_canvas.configure(scrollregion=tt_canvas.bbox("all")))
        tt_canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": tt_canvas}))
        tt_canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == tt_canvas else None)
        tt_frame.grid(row=0, column=2, padx=10)

        # Global mouse scroll binding
        self.controller.bind_all("<MouseWheel>", lambda e: active_canvas["canvas"].yview_scroll(-1 * int(e.delta / 120), "units") if active_canvas["canvas"] else None)