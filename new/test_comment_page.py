import tkinter as tk

def build_comment_ui(root):
    root.title("Song Comments UI")
    root.geometry("700x500")
    root.configure(bg='#9adbd2')

    title = tk.Label(root, text="SONG NAME", font=("Helvetica", 16), bg='#9adbd2')
    title.pack(pady=10)

    main_frame = tk.Frame(root, bg='#9adbd2')
    main_frame.pack(expand=True)

    active_canvas = {"canvas": None}  # use dict for mutable reference inside lambdas

    def make_scrollable_comment_section(parent, title_text, comments):
        frame = tk.Frame(parent, bg="white", bd=1, relief='solid')

        title_label = tk.Label(frame, text=title_text, fg="red" if "youtube" in title_text.lower() else "black", bg="white")
        title_label.pack(anchor="w", padx=10, pady=5)

        canvas = tk.Canvas(frame, width=200, height=300, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        inner = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner, anchor='nw')

        for comment_text in comments:
            lbl = tk.Label(inner, text=comment_text, bg="#d3d3d3", anchor="w", justify="left", wraplength=180)
            lbl.pack(fill="x", padx=5, pady=3)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": canvas}))
        canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == canvas else None)

        return frame

    root.bind_all("<MouseWheel>", lambda e: active_canvas["canvas"].yview_scroll(-1 * int(e.delta / 120), "units") if active_canvas["canvas"] else None)

    # Left
    yt_frame = make_scrollable_comment_section(main_frame, "youtube comments", ["commenter: blah\nblah blah blah blah"] * 10)
    yt_frame.grid(row=0, column=0, padx=10)

    # Middle
    add_frame = tk.Frame(main_frame, bg="white", bd=1, relief='solid', padx=10, pady=10)
    add_frame.grid(row=0, column=1, padx=10)

    tk.Label(add_frame, text="add comment", bg="white").pack()
    tk.Label(add_frame, text="comment data", bg="white").pack()

    tk.Text(add_frame, height=6, width=30, bg="#d3d3d3").pack(pady=5)
    tk.Button(add_frame, text="COMMENT", bg="#4b9c97", fg="white").pack()

    # Right
    tt_frame = make_scrollable_comment_section(main_frame, "tune together comments", ["commentor:\nblah blah blah"] * 10)
    tt_frame.grid(row=0, column=2, padx=10)

# Run it
if __name__ == "__main__":
    root = tk.Tk()
    build_comment_ui(root)
    root.mainloop()
