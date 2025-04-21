from page import Page
from client_new import Client
from server_request_new import ServerRequest, LIVE_CHAT_MESSAGE, GET_LIVE_CHAT_MESSAGES
from server_response import ServerResponse
import tkinter as tk
from tkinter import messagebox
from comment import Comment

class LiveChatPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        super().create_top_bar(connected_client.username)  # Create the top bar with username
        
        # back button
        back_button = tk.Button(self.top_bar, text="Back", font=("Arial", 20), bg="#4CAF50", fg="white", command=lambda:self.controller.show_frame("MainPage"))
        back_button.pack(side=tk.RIGHT, padx=10, pady=5)  # Add padding to the button
        
        active_canvas = {"canvas": None}

        chat_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid')
        tk.Label(chat_frame, text="Live chat with all connected users", fg="black", bg="white").pack(anchor="w", padx=10, pady=5)
        
        chat_canvas = tk.Canvas(chat_frame, width=800, height=500, bg="white", highlightthickness=0)
        chat_scroll = tk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview)
        chat_canvas.configure(yscrollcommand=chat_scroll.set)
        chat_canvas.pack(fill="both", expand=True)
        chat_scroll.pack(side="right", fill="y")

        chat_inner = tk.Frame(chat_canvas, bg="white")
        chat_canvas.create_window((0, 0), window=chat_inner, anchor='nw')


        chat_inner.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
        chat_canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": chat_canvas}))
        chat_canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == chat_canvas else None)
        chat_frame.grid(row=0, column=0, padx=200)
        
        self.controller.bind_all("<MouseWheel>", lambda e: active_canvas["canvas"].yview_scroll(-1 * int(e.delta / 120), "units") if active_canvas["canvas"] else None)

        self.update_chat(chat_inner)  # Start updating the chat


    def add_message(self, comment_text_widget: tk.Text):
        '''Adds a message to the live chat.'''
        comment_text = comment_text_widget.get("1.0", tk.END).strip()

        if not comment_text:
            messagebox.showerror("Error", "Comment cannot be empty.")
            return

        comment = Comment(
            username=self.connected_client.username,
            content=comment_text
        )
        
        # Send the comment to the server
        request = ServerRequest(LIVE_CHAT_MESSAGE, comment.to_dict())

        self.connected_client.send_request(request)

        # Clear the Text widget
        comment_text_widget.delete("1.0", tk.END)


    def update_chat(self, chat_inner):
        """Fetch new messages and update the chat display."""
        # Fetch messages from the server or shared data source
        all_messages = self.connected_client.send_request(ServerRequest(GET_LIVE_CHAT_MESSAGES))
        # Clear the current chat display
        for widget in chat_inner.winfo_children():
            widget.destroy()

        print(all_messages)
        # Add each message to the chat display
        for message in all_messages:
            text = message.__repr__()
            tk.Label(chat_inner, text=text, bg="white", anchor="w", justify="left", wraplength=780).pack(fill="x", padx=5, pady=3)

        # Schedule the next update
        self.after(1000, lambda: self.update_chat(chat_inner))  # Update every 1 second