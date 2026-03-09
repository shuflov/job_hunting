# 📚 Terminal Library Manager

A simple, keyboard-driven terminal UI for managing your book collection!

## Features

- 📖 View all your books in a clean table
- 🔍 Search books by title, author, or genre
- 📑 Sort by title, author, or year
- ➕ Add new books
- 🗑️ Delete books
- 📊 Track reading status (read/unread)
- ⌨️ 100% keyboard-driven (no mouse needed!)
- 💾 SQLite database storage

## Installation

### On WSL/Linux:

```bash
# Install Python if you don't have it
sudo apt update
sudo apt install python3 python3-pip

# Install the required library
pip3 install textual

# Or use the requirements file
pip3 install -r requirements.txt
```

### On Windows:

```powershell
# Make sure Python is installed, then:
pip install textual

# Or use the requirements file
pip install -r requirements.txt
```

## Running the App

```bash
python3 library_app.py
```

Or on Windows:
```powershell
python library_app.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `a` | Add a new book |
| `d` | Delete selected book |
| `s` | Toggle read/unread status |
| `r` | Refresh the table |
| `1` | Sort by Title |
| `2` | Sort by Author |
| `3` | Sort by Year |
| `/` | Focus search box |
| `↑↓` | Navigate through books |
| `Tab` | Move between input fields |
| `q` | Quit the app |

## How to Use

1. **Adding Books**: Press `a` or click in the input fields on the right panel
   - Fill in Title and Author (required)
   - Year and Genre are optional
   - Press Enter or click "Add Book"

2. **Searching**: Press `/` to focus the search box
   - Type your search term
   - Press Enter to filter books
   - Clear the search box and press Enter to show all books

3. **Managing Books**:
   - Use ↑↓ arrow keys to select a book
   - Press `s` to toggle between "read" and "unread"
   - Press `d` to delete the selected book

4. **Sorting**: Press `1`, `2`, or `3` to sort by different columns

## Database

The app creates a `library.db` SQLite file in the same directory where you run it. Your books are stored here permanently, so you can close and reopen the app without losing data.

## Tips

- The app works great in any terminal (Windows Terminal, WSL, etc.)
- It's fully keyboard-driven, so you never need to touch your mouse
- The search is case-insensitive and searches across title, author, and genre
- Book status is color-coded: green for "read", yellow for "unread"

Enjoy managing your library! 📚
