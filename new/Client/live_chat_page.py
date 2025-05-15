from new.Client.page import Page
from new.Client.client_new import Client
from new.shared.server_request_new import ServerRequest, LIVE_CHAT_MESSAGE, GET_LIVE_CHAT_MESSAGES
import tkinter as tk
from tkinter import messagebox
from new.shared.comment import Comment


MAX_CHAT_LENGTH = 200  # or whatever limit you want


class LiveChatPage(Page):
    def __init__(self, parent, controller, connected_client: Client):
        super().__init__(parent, controller, connected_client, bg_param="#95DBCD")
        super().create_top_bar(connected_client.username)  # Create the top bar with username

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


        self.chat_canvas = tk.Canvas(chat_frame, bg="white", highlightthickness=0)
        chat_scroll = tk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=chat_scroll.set)

        self.chat_canvas.grid(row=1, column=0, sticky="nsew")
        chat_scroll.grid(row=1, column=1, sticky="ns")

        chat_frame.grid_rowconfigure(1, weight=1)  # Allow canvas to grow vertically

        chat_inner = tk.Frame(self.chat_canvas, bg="white")
        self.chat_canvas.create_window((0, 0), window=chat_inner, anchor='nw')

        self.create_title_section(chat_frame, chat_inner)  # Create the title section
        self.update_chat(chat_inner)  # Fetch and display the chat messages

        add_message_frame = self.create_add_message_section(chat_inner)
        add_message_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        # Bind scrolling
        chat_inner.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.bind("<Enter>", lambda e: active_canvas.update({"canvas": self.chat_canvas}))
        self.chat_canvas.bind("<Leave>", lambda e: active_canvas.update({"canvas": None}) if active_canvas["canvas"] == self.chat_canvas else None)

        self.controller.bind_all("<MouseWheel>", lambda e: active_canvas["canvas"].yview_scroll(-1 * int(e.delta / 120), "units") if active_canvas["canvas"] else None)


    def update_chat(self, chat_inner: tk.Frame):
        """Fetches the latest messages from the server and updates the chat window. In this version, it only fetches the messages once."""
        # Clear current messages
        for widget in chat_inner.winfo_children():
            widget.destroy()

        # Create a request to get the live chat messages
        request = ServerRequest(GET_LIVE_CHAT_MESSAGES)

        # Send the request to the server
        response = self.connected_client.send_request(request)
        try:
            print(response.to_dict())
        except Exception as e:
            print("debug error:", e)
            print("debug error:", type(response))
            pass

        if response.response_code == "OK":
            # Add each message to the chat window
            for message in response.messages:
                text = message.__repr__()
                tk.Label(chat_inner, text=text, bg="#d3d3d3", anchor="w", justify="left", wraplength=1200).pack(fill="x", padx=5, pady=3)
            
        else:
            messagebox.showerror("Error", "Failed to fetch messages from the server.")

        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)  # Scroll to the bottom of the chat window


    def create_title_section(self, chat_frame: tk.Frame, chat_inner: tk.Frame):
        title_bar = tk.Frame(chat_frame, bg="white")
        title_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        title_bar.grid_columnconfigure(0, weight=1)

        tk.Label(title_bar, text="Live chat with all connected users", fg="black", bg="white").grid(row=0, column=0, sticky="w")

        tk.Button(
            title_bar,
            text="Refresh",
            bg="#8bc34a",
            fg="white",
            command=lambda: self.update_chat(chat_inner)
        ).grid(row=0, column=1, sticky="e", padx=(10, 0))


    def add_message(self, comment_text_widget: tk.Text, chat_inner):
        '''Adds a message to the live chat. Calls the server to send the message to all connected users.'''
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

        self.update_chat(chat_inner)  # Update the chat window to show the new message


    def create_add_message_section(self, chat_inner):
        """Create the section for adding messages to the chat."""
        add_frame = tk.Frame(self.content_frame, bg="white", bd=1, relief='solid', padx=2, pady=2)
        add_frame.grid_columnconfigure(0, weight=1)

        tk.Label(add_frame, text="Add message", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        comment_text_widget = tk.Text(add_frame, bg="#d3d3d3", height=5)
        comment_text_widget.grid(row=1, column=0, sticky="ew", padx=10)

        # Character count label
        char_count_label = tk.Label(add_frame, text=f"0/{MAX_CHAT_LENGTH}", bg="white", anchor="e")
        char_count_label.grid(row=2, column=0, sticky="e", padx=10)

        # Bind keypress events to limit and update counter
        comment_text_widget.bind("<Key>", lambda e: self.limit_text_length(e, comment_text_widget))
        comment_text_widget.bind("<KeyRelease>", lambda e: self.update_char_count(e, comment_text_widget, char_count_label))
        comment_text_widget.bind("<<Paste>>", lambda e: self.handle_paste(e, comment_text_widget, char_count_label))

        tk.Button(
            add_frame,
            text="SEND",
            bg="#4b9c97",
            fg="white",
            command=lambda: self.add_message(comment_text_widget, chat_inner)
        ).grid(row=3, column=0, sticky="e", padx=10, pady=5)

        return add_frame


    def limit_text_length(self, event, text_widget):
        content = text_widget.get("1.0", "end-1c")
        if len(content) >= MAX_CHAT_LENGTH and event.keysym != "BackSpace":
            return "break"


    def update_char_count(self, event, text_widget, label):
        content = text_widget.get("1.0", "end-1c")
        label.config(text=f"{len(content)}/{MAX_CHAT_LENGTH}")


    def handle_paste(self, event, text_widget, char_count_label):
        self.controller.after(1, lambda: self._trim_text(text_widget, char_count_label))  # defer to allow paste to complete


    def _trim_text(self, text_widget, char_count_label):
        content = text_widget.get("1.0", "end-1c")
        if len(content) > MAX_CHAT_LENGTH:
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", content[:MAX_CHAT_LENGTH])
        char_count_label.config(text=f"{min(len(content), MAX_CHAT_LENGTH)}/{MAX_CHAT_LENGTH}")
