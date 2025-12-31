import sqlite3

# ১. ডাটাবেস এবং টেবিল তৈরি করার ফাংশন
def initialize_db():
    conn = sqlite3.connect("library.db")
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
    
    conn.commit()
    conn.close()

# ২. বই সেভ করার ফাংশন
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
    conn.commit()
    conn.close()
    print(f"Database logic: Book ID {book_id} deleted successfully!")

# ৫. নাম বা লেখকের নাম দিয়ে বই সার্চ করার ফাংশন
def search_books(query):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    # LIKE ব্যবহার করা হয়েছে যাতে নামের অংশ বিশেষ লিখলেও খুঁজে পাওয়া যায়
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

# ফাইলটা সরাসরি রান করলে ডাটাবেস তৈরি হবে
if __name__ == "__main__":
    initialize_db()
    print("Database and Table created successfully!")