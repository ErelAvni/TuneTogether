import threading
from page import Page
from client_new import Client
from server_request_new import ServerRequest, LIVE_CHAT_MESSAGE, GET_LIVE_CHAT_MESSAGES
import tkinter as tk
from tkinter import messagebox
from comment import Comment
import time


class LiveChatPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        super().create_top_bar(connected_client.username)  # Create the top bar with username
        
        self.running = False
        self.poll_thread = None
        self.lock = threading.Lock()

        # back button
        back_button = tk.Button(self.top_bar, text="Back", font=("Arial", 20), bg="#4CAF50", fg="white", command=lambda:self.controller.show_frame("MainPage"))
        back_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Make content frame expandable
        self.content_frame.grid_columnconfigure(0, weight=1)

        active_canvas = {"canvas": None}

        # Chat frame
        chat_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid')
        chat_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        chat_frame.grid_columnconfigure(0, weight=1)

        tk.Label(chat_frame, text="Live chat with all connected users", fg="black", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        chat_canvas = tk.Canvas(chat_frame, bg="white", highlightthickness=0)
        chat_scroll = tk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview)
        chat_canvas.configure(yscrollcommand=chat_scroll.set)

        chat_canvas.grid(row=1, column=0, sticky="nsew")
        chat_scroll.grid(row=1, column=1, sticky="ns")

        chat_frame.grid_rowconfigure(1, weight=1)  # Allow canvas to grow vertically

        chat_inner = tk.Frame(chat_canvas, bg="white")
        chat_canvas.create_window((0, 0), window=chat_inner, anchor='nw')

        add_message_frame = self.create_add_message_section()
        add_message_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Bind scrolling
        chat_inner.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
        chat_canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": chat_canvas}))
        chat_canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == chat_canvas else None)

        self.controller.bind_all("<MouseWheel>", lambda e: active_canvas["canvas"].yview_scroll(-1 * int(e.delta / 120), "units") if active_canvas["canvas"] else None)

        self.start_chat_polling(chat_inner)  # Start polling for chat messages


    def add_message(self, comment_text_widget: tk.Text):
        '''Adds a message to the live chat.'''
        with self.lock:
            if self.update_chat_id:
                self.after_cancel(self.update_chat_id)  # Cancel the scheduled `after` call
                self.update_chat_id = None

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

            # Restart the chat update
            self.update_chat_id = self.after(1000, lambda: self.update_chat(comment_text_widget.master))  # Update every 1 second


    def create_add_message_section(self):
        """Create the section for adding messages to the chat."""
        add_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid', padx=2, pady=2)
        add_frame.grid_columnconfigure(0, weight=1)

        tk.Label(add_frame, text="Add message", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        comment_text_widget = tk.Text(add_frame, bg="#d3d3d3", height=5)
        comment_text_widget.grid(row=1, column=0, sticky="ew", padx=10)

        tk.Button(
            add_frame,
            text="SEND",
            bg="#4b9c97",
            fg="white",
            command=lambda: self.add_message(comment_text_widget)
        ).grid(row=2, column=0, sticky="e", padx=10, pady=5)

        return add_frame


    def start_chat_polling(self, chat_inner):
        if self.poll_thread is not None and self.poll_thread.is_alive():
            return  # ✅ Prevent starting more than one thread

        self.running = True

        def polling_loop():
            while self.running:
                try:
                    with self.lock:
                        print(f"[Thread] Polling messages... thread id: {threading.get_ident()}")
                        print("Fetching messages...")
                        response = self.connected_client.send_request(ServerRequest(GET_LIVE_CHAT_MESSAGES))
                        messages = response.messages if response.response_code == "OK" else []

                    # Safely update GUI from main thread
                    self.after(0, lambda: self.display_chat_messages(chat_inner, messages))

                except Exception as e:
                    print(f"[Polling error] {e}")

                time.sleep(1)  # Safe loop delay

        self.poll_thread = threading.Thread(target=polling_loop, daemon=True)
        self.poll_thread.start()


    def display_chat_messages(self, chat_inner, messages):
        for widget in chat_inner.winfo_children():
            widget.destroy()
        for message in messages:
            tk.Label(chat_inner, text=repr(message), bg="white", anchor="w", justify="left", wraplength=780).pack(fill="x", padx=5, pady=3)


    def destroy(self):
        """Clean up resources when the page is destroyed."""
        self.running = False
        if self.poll_thread and self.poll_thread.is_alive():
            self.poll_thread.join(timeout=1)
        
        super().destroy()  # Call the parent class's destroy method