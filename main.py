import customtkinter as ctk
from database import initialize_db, add_book # database.py থেকে ফাংশনগুলো আনলাম

# Initialize Database (অ্যাপ শুরুতেই ডাটাবেস চেক করবে)
initialize_db()

# App Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("600x500") # হাইট একটু বাড়িয়ে দিলাম

        # ১. ওয়েলকাম মেসেজ
        self.label = ctk.CTkLabel(self, text="Library Management System", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # ২. বইয়ের নাম ইনপুট বক্স
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter Book Title", width=300)
        self.title_entry.pack(pady=10)

        # ৩. লেখকের নাম ইনপুট বক্স
        self.author_entry = ctk.CTkEntry(self, placeholder_text="Enter Author Name", width=300)
        self.author_entry.pack(pady=10)

        # ৪. ডাটা সেভ করার বাটন
        self.save_btn = ctk.CTkButton(self, text="Save Book to Database", command=self.save_book_data)
        self.save_btn.pack(pady=20)

        # ৫. স্ট্যাটাস দেখার জন্য ছোট একটা লেবেল (সফল হলে মেসেজ দেখাবে)
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.pack(pady=10)

    # বই সেভ করার ফাংশন
    def save_book_data(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        
        if title != "" and author != "":
            # database.py এর add_book ফাংশন কল করছি
            add_book(title, author)
            
            # টার্মিনালে মেসেজ প্রিন্ট
            print(f"Success: {title} by {author} saved!")
            
            # স্ক্রিনে সাকসেস মেসেজ দেখানো
            self.status_label.configure(text=f"'{title}' added successfully!", text_color="lightgreen")
            
            # ইনপুট বক্স খালি করে দেওয়া
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
        else:
            self.status_label.configure(text="Error: Please fill all fields!", text_color="red")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()