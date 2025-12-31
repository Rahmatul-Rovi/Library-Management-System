import customtkinter as ctk
from database import initialize_db

# Initialize Database
initialize_db()

# App Appearance Settings
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("600x400")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Welcome to Library System", font=("Arial", 24))
        self.label.pack(pady=40)

        self.btn_start = ctk.CTkButton(self, text="Get Started", command=self.start_action)
        self.btn_start.pack(pady=20)

    def start_action(self):
        print("Project Shuru Holo!")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()