import customtkinter as ctk
from database import initialize_db, add_book, get_all_books, delete_book # database থেকে সব ইমপোর্ট করলাম

# Initialize Database
initialize_db()

# App Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("600x750") # হাইট বাড়িয়েছি যাতে সব বাটন ফিট হয়

        # ১. টাইটেল
        self.label = ctk.CTkLabel(self, text="Library Management System", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # ২. ইনপুট সেকশন (বই যোগ করার জন্য)
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter Book Title", width=300)
        self.title_entry.pack(pady=10)

        self.author_entry = ctk.CTkEntry(self, placeholder_text="Enter Author Name", width=300)
        self.author_entry.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save Book to Database", command=self.save_book_data)
        self.save_btn.pack(pady=20)

        # ৩. স্ট্যাটাস লেবেল (মেসেজ দেখানোর জন্য)
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.pack(pady=5)

        # ৪. বই দেখার সেকশন
        self.view_btn = ctk.CTkButton(self, text="Show All Books", command=self.show_books, fg_color="orange", text_color="black")
        self.view_btn.pack(pady=10)

        self.book_display = ctk.CTkTextbox(self, width=500, height=180)
        self.book_display.pack(pady=10)

        # ৫. ডিলিট করার সেকশন
        self.delete_label = ctk.CTkLabel(self, text="Enter Book ID to Delete:", font=("Arial", 12))
        self.delete_label.pack(pady=(20, 0))

        self.delete_entry = ctk.CTkEntry(self, placeholder_text="e.g. 1", width=100)
        self.delete_entry.pack(pady=5)

        self.delete_btn = ctk.CTkButton(self, text="Delete Book", command=self.delete_book_ui, fg_color="red")
        self.delete_btn.pack(pady=10)

    # ফাংশন: বই সেভ করা
    def save_book_data(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        
        if title != "" and author != "":
            add_book(title, author)
            self.status_label.configure(text=f"'{title}' added successfully!", text_color="lightgreen")
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
            self.show_books() # লিস্ট আপডেট হবে
        else:
            self.status_label.configure(text="Error: Please fill all fields!", text_color="red")

    # ফাংশন: বইয়ের লিস্ট দেখানো
    def show_books(self):
        books = get_all_books()
        self.book_display.delete("1.0", "end")
        
        header = f"{'ID':<5} | {'Title':<20} | {'Author':<15} | {'Status'}\n"
        self.book_display.insert("end", header)
        self.book_display.insert("end", "-"*60 + "\n")
        
        for book in books:
            book_str = f"{book[0]:<5} | {book[1]:<20} | {book[2]:<15} | {book[3]}\n"
            self.book_display.insert("end", book_str)

    # ফাংশন: বই ডিলিট করা
    def delete_book_ui(self):
        book_id = self.delete_entry.get()
        
        if book_id != "":
            delete_book(book_id)
            self.status_label.configure(text=f"Book ID {book_id} deleted!", text_color="orange")
            self.delete_entry.delete(0, 'end')
            self.show_books() # ডিলিট হওয়ার পর লিস্ট রিফ্রেশ হবে
        else:
            self.status_label.configure(text="Error: Enter an ID to delete", text_color="red")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()