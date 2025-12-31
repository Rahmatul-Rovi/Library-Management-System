import customtkinter as ctk
from database import initialize_db, add_book, get_all_books, delete_book, search_books

# Initialize Database
initialize_db()

# App Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        self.geometry("600x850") # ফিচার বাড়ায় হাইট একটু বাড়িয়ে দিলাম

        # ১. মেইন টাইটেল
        self.label = ctk.CTkLabel(self, text="Library Management System", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # ২. সার্চ সেকশন (সবার উপরে রাখলে সুবিধা)
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by Title or Author", width=300)
        self.search_entry.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(self.search_frame, text="Search", width=100, command=self.search_book_ui, fg_color="purple")
        self.search_btn.pack(side="left", padx=10)

        # ৩. ইনপুট সেকশন (বই যোগ করার জন্য)
        self.input_label = ctk.CTkLabel(self, text="Add New Book", font=("Arial", 16, "bold"))
        self.input_label.pack(pady=(10, 0))

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter Book Title", width=300)
        self.title_entry.pack(pady=10)

        self.author_entry = ctk.CTkEntry(self, placeholder_text="Enter Author Name", width=300)
        self.author_entry.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save Book to Database", command=self.save_book_data)
        self.save_btn.pack(pady=15)

        # ৪. স্ট্যাটাস লেবেল (মেসেজ দেখানোর জন্য)
        self.status_label = ctk.CTkLabel(self, text="Welcome!", font=("Arial", 14), text_color="gray")
        self.status_label.pack(pady=5)

        # ৫. বই দেখার সেকশন
        self.view_btn = ctk.CTkButton(self, text="Show All Books", command=self.show_books, fg_color="orange", text_color="black")
        self.view_btn.pack(pady=10)

        self.book_display = ctk.CTkTextbox(self, width=540, height=200)
        self.book_display.pack(pady=10)

        # ৬. ডিলিট করার সেকশন
        self.delete_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.delete_frame.pack(pady=20)

        self.delete_label = ctk.CTkLabel(self.delete_frame, text="Enter Book ID to Delete:", font=("Arial", 12))
        self.delete_label.pack(side="left", padx=10)

        self.delete_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="ID", width=60)
        self.delete_entry.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(self.delete_frame, text="Delete", width=80, command=self.delete_book_ui, fg_color="red")
        self.delete_btn.pack(side="left", padx=10)

    # --- ফাংশন সমূহ ---

    def save_book_data(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title != "" and author != "":
            add_book(title, author)
            self.status_label.configure(text=f"'{title}' added successfully!", text_color="lightgreen")
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
            self.show_books()
        else:
            self.status_label.configure(text="Error: Please fill all fields!", text_color="red")

    def show_books(self):
        books = get_all_books()
        self.display_records(books)

    def search_book_ui(self):
        query = self.search_entry.get()
        if query != "":
            results = search_books(query)
            self.display_records(results, is_search=True)
        else:
            self.show_books()

    def display_records(self, records, is_search=False):
        self.book_display.delete("1.0", "end")
        if is_search:
            self.book_display.insert("end", f"Showing results for search...\n")
        
        header = f"{'ID':<5} | {'Title':<25} | {'Author':<20} | {'Status'}\n"
        self.book_display.insert("end", header)
        self.book_display.insert("end", "-"*70 + "\n")
        
        if not records:
            self.book_display.insert("end", "\n   No records found!")
        else:
            for book in records:
                book_str = f"{book[0]:<5} | {book[1]:<25} | {book[2]:<20} | {book[3]}\n"
                self.book_display.insert("end", book_str)

    def delete_book_ui(self):
        book_id = self.delete_entry.get()
        if book_id != "":
            delete_book(book_id)
            self.status_label.configure(text=f"Book ID {book_id} deleted!", text_color="orange")
            self.delete_entry.delete(0, 'end')
            self.show_books()
        else:
            self.status_label.configure(text="Error: Enter ID", text_color="red")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()