import customtkinter as ctk
from database import (initialize_db, add_book, get_all_books, 
                      delete_book, search_books, issue_book, 
                      get_issued_books, return_book, get_stats) # get_stats যোগ করা হয়েছে

# Initialize Database
initialize_db()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System Pro")
        self.geometry("680x1000") 

        # --- মেইন টাইটেল ---
        self.label = ctk.CTkLabel(self, text="Library Management System", font=("Arial", 26, "bold"))
        self.label.pack(pady=15)

        # --- ড্যাশবোর্ড সেকশন (Stats) ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.stats_frame.pack(pady=10, padx=20, fill="x")

        self.total_books_label = ctk.CTkLabel(self.stats_frame, text="Total Books: 0", font=("Arial", 14, "bold"), text_color="white")
        self.total_books_label.pack(side="left", padx=50, pady=10)

        self.issued_books_label = ctk.CTkLabel(self.stats_frame, text="Issued: 0", font=("Arial", 14, "bold"), text_color="#FFCC00")
        self.issued_books_label.pack(side="left", padx=50, pady=10)
        
        self.update_dashboard() # অ্যাপ খোলার সময় ডাটা লোড হবে

        # --- ১. সার্চ সেকশন ---
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by Title or Author", width=350)
        self.search_entry.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(self.search_frame, text="Search", width=100, command=self.search_book_ui, fg_color="purple")
        self.search_btn.pack(side="left", padx=10)

        # --- ২. বই যোগ করার সেকশন ---
        self.input_label = ctk.CTkLabel(self, text="Add New Book", font=("Arial", 16, "bold"))
        self.input_label.pack(pady=(10, 0))

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter Book Title", width=350)
        self.title_entry.pack(pady=5)

        self.author_entry = ctk.CTkEntry(self, placeholder_text="Enter Author Name", width=350)
        self.author_entry.pack(pady=5)

        self.save_btn = ctk.CTkButton(self, text="Save Book to Library", command=self.save_book_data)
        self.save_btn.pack(pady=10)

        # --- ৩. স্ট্যাটাস মেসেজ ---
        self.status_label = ctk.CTkLabel(self, text="System Ready", font=("Arial", 14), text_color="gray")
        self.status_label.pack(pady=5)

        # --- ৪. বই ধার দেওয়ার সেকশন ---
        self.issue_frame = ctk.CTkFrame(self, border_width=2, border_color="gray")
        self.issue_frame.pack(pady=10, padx=20, fill="x")

        self.issue_title = ctk.CTkLabel(self.issue_frame, text="Issue Book to Member", font=("Arial", 14, "bold"))
        self.issue_title.pack(pady=5)

        self.issue_book_id = ctk.CTkEntry(self.issue_frame, placeholder_text="Book ID", width=80)
        self.issue_book_id.pack(side="left", padx=10, pady=10)

        self.member_name = ctk.CTkEntry(self.issue_frame, placeholder_text="Member Name", width=180)
        self.member_name.pack(side="left", padx=5)

        self.member_contact = ctk.CTkEntry(self.issue_frame, placeholder_text="Contact No", width=150)
        self.member_contact.pack(side="left", padx=5)

        self.issue_btn = ctk.CTkButton(self.issue_frame, text="Issue", width=80, command=self.issue_book_ui, fg_color="green")
        self.issue_btn.pack(side="left", padx=10)

        # --- ৫. বই ফেরত দেওয়ার সেকশন ---
        self.return_frame = ctk.CTkFrame(self, border_width=2, border_color="#3B8ED0")
        self.return_frame.pack(pady=10, padx=20, fill="x")

        self.return_title = ctk.CTkLabel(self.return_frame, text="Return Book", font=("Arial", 14, "bold"))
        self.return_title.pack(side="left", padx=20, pady=10)

        self.return_id_entry = ctk.CTkEntry(self.return_frame, placeholder_text="Enter Book ID", width=150)
        self.return_id_entry.pack(side="left", padx=10)

        self.return_btn = ctk.CTkButton(self.return_frame, text="Confirm Return", width=120, command=self.return_book_ui)
        self.return_btn.pack(side="left", padx=20)

        # --- ৬. ডাটা দেখার বাটন সমূহ ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.view_btn = ctk.CTkButton(self.btn_frame, text="Show All Books", command=self.show_books, fg_color="orange", text_color="black")
        self.view_btn.pack(side="left", padx=10)

        self.issued_view_btn = ctk.CTkButton(self.btn_frame, text="View Issued Books", command=self.show_issued_books_ui, fg_color="teal")
        self.issued_view_btn.pack(side="left", padx=10)

        # --- ৭. মেইন ডিসপ্লে (টেক্সটবক্স) ---
        self.book_display = ctk.CTkTextbox(self, width=620, height=200, font=("Courier New", 13))
        self.book_display.pack(pady=10)

        # --- ৮. ডিলিট করার সেকশন ---
        self.delete_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.delete_frame.pack(pady=10)

        self.delete_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="ID", width=60)
        self.delete_entry.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(self.delete_frame, text="Delete Book", width=120, command=self.delete_book_ui, fg_color="red")
        self.delete_btn.pack(side="left")

    # --- ফাংশন সমূহ ---

    def update_dashboard(self):
        total, issued = get_stats()
        self.total_books_label.configure(text=f"Total Books: {total}")
        self.issued_books_label.configure(text=f"Issued: {issued}")

    def save_book_data(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title and author:
            add_book(title, author)
            self.status_label.configure(text=f"'{title}' saved!", text_color="lightgreen")
            self.title_entry.delete(0, 'end'); self.author_entry.delete(0, 'end')
            self.show_books()
            self.update_dashboard()
        else:
            self.status_label.configure(text="Fill all fields!", text_color="red")

    def issue_book_ui(self):
        bid = self.issue_book_id.get()
        mname = self.member_name.get()
        mcontact = self.member_contact.get()
        if bid and mname and mcontact:
            issue_book(bid, mname, mcontact)
            self.status_label.configure(text=f"ID {bid} issued to {mname}", text_color="cyan")
            self.issue_book_id.delete(0, 'end'); self.member_name.delete(0, 'end'); self.member_contact.delete(0, 'end')
            self.show_books()
            self.update_dashboard()
        else:
            self.status_label.configure(text="Fill all Issue fields!", text_color="red")

    def return_book_ui(self):
        bid = self.return_id_entry.get()
        if bid:
            return_book(bid)
            self.status_label.configure(text=f"Book ID {bid} Returned Successfully!", text_color="yellow")
            self.return_id_entry.delete(0, 'end')
            self.show_books()
            self.update_dashboard()
        else:
            self.status_label.configure(text="Enter ID to return!", text_color="red")

    def show_books(self):
        records = get_all_books()
        self.book_display.delete("1.0", "end")
        header = f"{'ID':<5} | {'Title':<25} | {'Author':<18} | {'Status'}\n"
        self.book_display.insert("end", header + "-"*70 + "\n")
        for b in records:
            self.book_display.insert("end", f"{b[0]:<5} | {b[1]:<25} | {b[2]:<18} | {b[3]}\n")

    def show_issued_books_ui(self):
        records = get_issued_books()
        self.book_display.delete("1.0", "end")
        self.book_display.insert("end", "--- List of Currently Issued Books ---\n\n")
        header = f"{'I_ID':<5} | {'Book Title':<25} | {'Member Name':<15} | {'Contact'}\n"
        self.book_display.insert("end", header + "-"*75 + "\n")
        for r in records:
            self.book_display.insert("end", f"{r[0]:<5} | {r[1]:<25} | {r[2]:<15} | {r[3]}\n")

    def search_book_ui(self):
        query = self.search_entry.get()
        if query:
            results = search_books(query)
            self.book_display.delete("1.0", "end")
            self.book_display.insert("end", f"Results for: {query}\n" + "-"*40 + "\n")
            for b in results:
                self.book_display.insert("end", f"{b[0]:<5} | {b[1]:<25} | {b[2]:<18} | {b[3]}\n")
        else:
            self.show_books()

    def delete_book_ui(self):
        bid = self.delete_entry.get()
        if bid:
            delete_book(bid)
            self.status_label.configure(text=f"Book ID {bid} deleted!", text_color="orange")
            self.delete_entry.delete(0, 'end')
            self.show_books()
            self.update_dashboard()

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()