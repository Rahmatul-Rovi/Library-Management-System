import sqlite3

# ১. ডাটাবেস এবং টেবিল তৈরি করার ফাংশন
def initialize_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # Books Table তৈরি (বইয়ের মেইন লিস্ট)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'Available'
        )
    """)

    # Issued Books Table তৈরি (কার কাছে বই আছে তার হিসাব)
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
    conn.close()

# ২. নতুন বই সেভ করার ফাংশন
def add_book(title, author):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()
    print(f"Database logic: Book '{title}' added successfully!")

# ৩. সব বইয়ের লিস্ট নিয়ে আসার ফাংশন
def get_all_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# ৪. আইডি দিয়ে বই ডিলিট করার ফাংশন
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    # বই ডিলিট করলে যদি তা ইস্যু করা থাকে, সেই রেকর্ডও মুছে ফেলা ভালো
    cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
    print(f"Database logic: Book ID {book_id} deleted successfully!")

# ৫. নাম বা লেখকের নাম দিয়ে বই সার্চ করার ফাংশন
def search_books(query):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

# ৬. বই ধার দেওয়ার (Issue) ফাংশন
def issue_book(book_id, member_name, member_contact="N/A"):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # বইয়ের স্ট্যাটাস 'Issued' করে দেওয়া
    cursor.execute("UPDATE books SET status = 'Issued' WHERE id = ?", (book_id,))
    
    # তথ্য সেভ করা
    cursor.execute("INSERT INTO issued_books (book_id, member_name, member_contact) VALUES (?, ?, ?)", 
                   (book_id, member_name, member_contact))
    
    conn.commit()
    conn.close()
    print(f"Database logic: Book ID {book_id} issued to {member_name}")

# ৭. ইস্যু করা বইয়ের লিস্ট নিয়ে আসার ফাংশন
def get_issued_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT issued_books.issue_id, books.title, issued_books.member_name, issued_books.member_contact, books.id
        FROM issued_books 
        JOIN books ON issued_books.book_id = books.id
    """)
    data = cursor.fetchall()
    conn.close()
    return data

# ৮. বই ফেরত নেওয়ার (Return) ফাংশন
def return_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # ১. বইয়ের স্ট্যাটাস আবার 'Available' করে দেওয়া
    cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
    
    # ২. ইস্যু টেবিল থেকে ওই বইয়ের রেকর্ড ডিলিট করা
    cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
    
    conn.commit()
    conn.close()
    print(f"Database logic: Book ID {book_id} returned successfully!")

# ৯. ড্যাশবোর্ডের জন্য স্ট্যাটাস কাউন্ট করার ফাংশন
def get_stats():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Issued'")
    issued_books = cursor.fetchone()[0]
    conn.close()
    return total_books, issued_books

# ১০. নতুন: লাইব্রেরি রিপোর্ট এক্সপোর্ট করার ফাংশন (Text File)
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
        print(f"Error exporting: {e}")
        return False

# ফাইলটা সরাসরি রান করলে ডাটাবেস তৈরি হবে
if __name__ == "__main__":
    initialize_db()
    print("Database and Tables updated successfully!")