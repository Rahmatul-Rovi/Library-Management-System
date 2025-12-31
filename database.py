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

# ২. বই সেভ করার ফাংশন (এটা main.py থেকে কল হবে)
def add_book(title, author):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()
    print(f"Database logic: Book '{title}' added successfully!")

# ৩. ফাইলটা রান করলে ডাটাবেস যাতে তৈরি হয়
if __name__ == "__main__":
    initialize_db()
    print("Database and Table created successfully!")