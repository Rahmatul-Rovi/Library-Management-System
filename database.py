import sqlite3

def initialize_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # Books Table: Boi-er details rakhar jonno
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

if __name__ == "__main__":
    initialize_db()
    print("Database and Table created successfully!")

    def add_book(title, author):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added successfully!")