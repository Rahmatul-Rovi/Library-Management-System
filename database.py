import sqlite3

# ১. ডাটাবেস এবং টেবিল তৈরি করার ফাংশন
def initialize_db():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        
        # Books Table তৈরি
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                status TEXT DEFAULT 'Available'
            )
        """)

        # Issued Books Table তৈরি
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_name TEXT,
                member_contact TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        """)
        conn.commit()
    print("Database Initialized.")

# ২. নতুন বই সেভ করার ফাংশন
def add_book(title, author):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()

# ৩. সব বইয়ের লিস্ট নিয়ে আসার ফাংশন
def get_all_books():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

# ৪. আইডি দিয়ে বই ডিলিট করার ফাংশন
def delete_book(book_id):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
        conn.commit()

# ৫. নাম বা লেখকের নাম দিয়ে বই সার্চ করার ফাংশন
def search_books(query):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                       ('%' + query + '%', '%' + query + '%'))
        return cursor.fetchall()

# ৬. বই ধার দেওয়ার (Issue) ফাংশন
def issue_book(book_id, member_name, member_contact="N/A"):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = 'Issued' WHERE id = ?", (book_id,))
        cursor.execute("INSERT INTO issued_books (book_id, member_name, member_contact) VALUES (?, ?, ?)", 
                       (book_id, member_name, member_contact))
        conn.commit()

# ৭. ইস্যু করা বইয়ের লিস্ট নিয়ে আসার ফাংশন
def get_issued_books():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT issued_books.issue_id, books.title, issued_books.member_name, issued_books.member_contact, books.id
            FROM issued_books 
            JOIN books ON issued_books.book_id = books.id
        """)
        return cursor.fetchall()

# ৮. বই ফেরত নেওয়ার (Return) ফাংশন
def return_book(book_id):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
        cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
        conn.commit()

# ৯. ড্যাশবোর্ডের জন্য স্ট্যাটাস কাউন্ট করার ফাংশন
def get_stats():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Issued'")
        issued = cursor.fetchone()[0]
        return total, issued

# ১০. লাইব্রেরি রিপোর্ট এক্সপোর্ট করার ফাংশন
def export_books_to_file():
    books = get_all_books()
    try:
        with open("library_report.txt", "w", encoding="utf-8") as f:
            f.write("========== LIBRARY BOOKS REPORT ==========\n\n")
            f.write(f"{'ID':<5} | {'Title':<30} | {'Author':<20} | {'Status'}\n")
            f.write("-" * 75 + "\n")
            for b in books:
                f.write(f"{b[0]:<5} | {b[1]:<30} | {b[2]:<20} | {b[3]}\n")
            f.write("\n==========================================\n")
        return True
    except Exception as e:
        print(f"Export Error: {e}")
        return False

if __name__ == "__main__":
    initialize_db()