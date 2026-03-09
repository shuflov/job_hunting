#!/usr/bin/env python3
"""
Populate the library database with sample books for testing
"""

import sqlite3

def add_sample_books():
    """Add some sample books to the database"""
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            status TEXT DEFAULT 'unread',
            added_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sample books
    sample_books = [
        ("The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy", "read"),
        ("1984", "George Orwell", 1949, "Dystopian", "read"),
        ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction", "unread"),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction", "read"),
        ("Dune", "Frank Herbert", 1965, "Science Fiction", "unread"),
        ("The Catcher in the Rye", "J.D. Salinger", 1951, "Fiction", "read"),
        ("Foundation", "Isaac Asimov", 1951, "Science Fiction", "unread"),
        ("Brave New World", "Aldous Huxley", 1932, "Dystopian", "read"),
        ("The Lord of the Rings", "J.R.R. Tolkien", 1954, "Fantasy", "unread"),
        ("Neuromancer", "William Gibson", 1984, "Cyberpunk", "unread"),
    ]
    
    cursor.executemany("""
        INSERT INTO books (title, author, year, genre, status)
        VALUES (?, ?, ?, ?, ?)
    """, sample_books)
    
    conn.commit()
    conn.close()
    
    print("✅ Added 10 sample books to the library!")
    print("Run 'python3 library_app.py' to start the app.")

if __name__ == "__main__":
    add_sample_books()
