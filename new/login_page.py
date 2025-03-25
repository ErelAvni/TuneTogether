import tkinter as tk
import hashlib


def hash_password(password: str) -> str:
    """
    Hash the given password using SHA-256.

    :param password: The password to hash.
    :return: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def create_login_ui():
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("1000x600")
    root.configure(bg="#95DBCD")

    # Custom Fonts
    title_font = ("Arial", 50, "bold")
    label_font = ("Arial", 20)
    button_font = ("Arial", 20)

    # Title Label
    title_label = tk.Label(root, text="LOGIN", font=title_font, bg="#95DBCD")
    title_label.pack(pady=30)

    # Username Label and Entry
    username_label = tk.Label(root, text="Enter username:", font=label_font, bg="#95DBCD")
    username_label.pack()
    username_entry = tk.Entry(root, font=label_font, bg="#BFC6C7", width=20)
    username_entry.pack(pady=5)

    # Password Label and Entry
    password_label = tk.Label(root, text="Enter password:", font=label_font, bg="#95DBCD")
    password_label.pack()
    password_entry = tk.Entry(root, font=label_font, bg="#BFC6C7", width=20, show="*")
    password_entry.pack(pady=5)

    # Login Button
    login_button = tk.Button(root, text="Login", font=button_font, bg="#639A97", fg="white", width=20, height=1)
    login_button.pack(pady=15)

    # Register Section
    register_frame = tk.Frame(root, bg="#95DBCD")
    register_frame.pack(side="bottom", pady=(0, 50))
    
    register_text = tk.Label(register_frame, text="Don't have an account yet?", font=label_font, bg="#95DBCD")
    register_text.pack()
    
    register_button = tk.Button(register_frame, text="Register", font=button_font, bg="#639A97", fg="white", width=20, height=1)
    register_button.pack(pady=10)

    root.mainloop()

create_login_ui()
