import customtkinter as ctk
from database import (initialize_db, add_book, get_all_books, 
                      delete_book, search_books, issue_book, 
                      get_issued_books, return_book, get_stats, export_books_to_file)

# Initialize Database
initialize_db()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System Pro")
        self.geometry("700x950") 

        # --- মেইন টাইটেল ---
        self.label = ctk.CTkLabel(self, text="Library Management System", font=("Arial", 28, "bold"))
        self.label.pack(pady=15)

        # --- ড্যাশবোর্ড সেকশন (Stats) ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        self.stats_frame.pack(pady=10, padx=20, fill="x")

        self.total_books_label = ctk.CTkLabel(self.stats_frame, text="Total Books: 0", font=("Arial", 16, "bold"))
        self.total_books_label.pack(side="left", padx=60, pady=15)

        self.issued_books_label = ctk.CTkLabel(self.stats_frame, text="Issued: 0", font=("Arial", 16, "bold"), text_color="#FFCC00")
        self.issued_books_label.pack(side="left", padx=60, pady=15)
        
        self.update_dashboard()

        # --- ১. সার্চ সেকশন ---
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by Title or Author", width=400)
        self.search_entry.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(self.search_frame, text="Search", width=100, command=self.search_book_ui, fg_color="purple")
        self.search_btn.pack(side="left", padx=10)

        # --- ২. বই যোগ করার সেকশন ---
        self.add_frame = ctk.CTkFrame(self)
        self.add_frame.pack(pady=10, padx=20, fill="x")

        self.title_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Book Title", width=220)
        self.title_entry.pack(side="left", padx=10, pady=10)

        self.author_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Author", width=180)
        self.author_entry.pack(side="left", padx=5)

        self.save_btn = ctk.CTkButton(self.add_frame, text="Add Book", width=100, fg_color="green", command=self.save_book_data)
        self.save_btn.pack(side="left", padx=10)

        # --- ৩. স্ট্যাটাস মেসেজ ---
        self.status_label = ctk.CTkLabel(self, text="System Ready", font=("Arial", 14), text_color="gray")
        self.status_label.pack(pady=5)

        # --- ৪. বই ধার দেওয়ার সেকশন (Issue) ---
        self.issue_frame = ctk.CTkFrame(self, border_width=1, border_color="gray")
        self.issue_frame.pack(pady=10, padx=20, fill="x")

        self.issue_book_id = ctk.CTkEntry(self.issue_frame, placeholder_text="Book ID", width=70)
        self.issue_book_id.pack(side="left", padx=10, pady=10)

        self.member_name = ctk.CTkEntry(self.issue_frame, placeholder_text="Member Name", width=180)
        self.member_name.pack(side="left", padx=5)

        self.issue_btn = ctk.CTkButton(self.issue_frame, text="Issue Book", width=100, command=self.issue_book_ui)
        self.issue_btn.pack(side="left", padx=10)

        # --- ৫. অপারেশন বাটনস (Return & Export) ---
        self.op_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.op_frame.pack(pady=10)

        self.return_id_entry = ctk.CTkEntry(self.op_frame, placeholder_text="ID to Return", width=100)
        self.return_id_entry.pack(side="left", padx=5)

        self.return_btn = ctk.CTkButton(self.op_frame, text="Confirm Return", width=130, fg_color="#3B8ED0", command=self.return_book_ui)
        self.return_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(self.op_frame, text="Export List (.txt)", width=130, fg_color="teal", command=self.export_data_ui)
        self.export_btn.pack(side="left", padx=5)

        # --- ৬. ডাটা ডিসপ্লে ---
        self.view_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.view_frame.pack(pady=5)
        
        self.view_btn = ctk.CTkButton(self.view_frame, text="Show All Books", command=self.show_books, fg_color="orange", text_color="black", width=150)
        self.view_btn.pack(side="left", padx=10)

        self.issued_view_btn = ctk.CTkButton(self.view_frame, text="View Issued Books", command=self.show_issued_books_ui, fg_color="gray", width=150)
        self.issued_view_btn.pack(side="left", padx=10)

        self.book_display = ctk.CTkTextbox(self, width=640, height=250, font=("Courier New", 13))
        self.book_display.pack(pady=10)

        # --- ৭. ডিলিট সেকশন ---
        self.delete_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.delete_frame.pack(pady=10)

        self.delete_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="ID", width=60)
        self.delete_entry.pack(side="left", padx=10)

        self.delete_btn = ctk.CTkButton(self.delete_frame, text="Delete Book", width=120, command=self.delete_book_ui, fg_color="red")
        self.delete_btn.pack(side="left")

    # --- Functions ---

    def update_dashboard(self):
        total, issued = get_stats()
        self.total_books_label.configure(text=f"Total Books: {total}")
        self.issued_books_label.configure(text=f"Issued: {issued}")

    def save_book_data(self):
        title, author = self.title_entry.get(), self.author_entry.get()
        if title and author:
            add_book(title, author)
            self.status_label.configure(text=f"'{title}' added!", text_color="lightgreen")
            self.title_entry.delete(0, 'end'); self.author_entry.delete(0, 'end')
            self.show_books(); self.update_dashboard()
        else: self.status_label.configure(text="Fill Title and Author!", text_color="red")

    def issue_book_ui(self):
        bid, name = self.issue_book_id.get(), self.member_name.get()
        if bid and name:
            issue_book(bid, name)
            self.status_label.configure(text=f"ID {bid} issued to {name}", text_color="cyan")
            self.issue_book_id.delete(0, 'end'); self.member_name.delete(0, 'end')
            self.show_books(); self.update_dashboard()
        else: self.status_label.configure(text="Enter ID and Member Name!", text_color="red")

    def return_book_ui(self):
        bid = self.return_id_entry.get()
        if bid:
            return_book(bid)
            self.status_label.configure(text=f"Book ID {bid} Returned!", text_color="yellow")
            self.return_id_entry.delete(0, 'end')
            self.show_books(); self.update_dashboard()

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
        self.book_display.insert("end", "--- Currently Issued Books ---\n\n")
        header = f"{'I_ID':<5} | {'Title':<25} | {'Member Name':<15} | {'Contact'}\n"
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

    def delete_book_ui(self):
        bid = self.delete_entry.get()
        if bid:
            delete_book(bid)
            self.status_label.configure(text=f"ID {bid} deleted!", text_color="orange")
            self.delete_entry.delete(0, 'end')
            self.show_books(); self.update_dashboard()

    def export_data_ui(self):
        if export_books_to_file():
            self.status_label.configure(text="List exported to 'library_report.txt'", text_color="lightgreen")
        else:
            self.status_label.configure(text="Export Failed!", text_color="red")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()