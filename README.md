# 📚 Terminal Library Manager

A fun, lightweight terminal-based UI for managing your personal book collection! Built with Python and Textual, this app brings the joy of keyboard-driven interfaces to book lovers who spend most of their time in the terminal.

## 🎯 About This Project

This is a **just-for-fun** project for anyone who:
- Lives in the terminal (WSL, Windows Terminal, or any Linux terminal)
- Loves keyboard-driven interfaces (no mouse needed!)
- Wants a simple way to track their reading list
- Appreciates clean, minimal TUI (Text User Interface) apps

Think of it as a lightweight alternative to Goodreads or LibraryThing, but entirely in your terminal with zero distractions!

## ✨ Features

- 📖 **View your entire library** in a clean, sortable table
- 🔍 **Search** books by title, author, or genre (real-time filtering)
- 📑 **Sort** by title, author, year, or newest first (ID)
- ➕ **Add books** via a modal dialog (Tab through fields, hit Enter)
- 🗑️ **Delete books** with confirmation dialog (safety first!)
- 📊 **Track reading status** - toggle between "read" and "unread"
- 🎨 **5 beautiful themes** (dark, light, nord, gruvbox, catppuccin) - saved automatically!
- ⌨️ **100% keyboard-driven** - optimized for speed and efficiency
- 💾 **SQLite database** - all your data persists between sessions
- 🔄 **Quick reset** - refresh to clear search and return to default view
- 🎮 **Command palette** (Ctrl+P) - discover all commands

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (most systems have this already)
- That's it! Just one dependency to install.

### Installation

#### On WSL/Linux:

```bash
# Install Python if needed
sudo apt update
sudo apt install python3 python3-pip

# Install Textual
pip3 install textual

# Or use requirements.txt
pip3 install -r requirements.txt
```

#### On Windows (PowerShell/CMD):

```powershell
# Install Textual
pip install textual

# Or use requirements.txt
pip install -r requirements.txt
```

### Running the App

```bash
python3 library_app.py
```

Or on Windows:
```powershell
python library_app.py
```

### Adding Sample Data (Optional)

To start with some books already loaded:

**Option 1: Using Python script**
```bash
python3 add_sample_data.py
```

**Option 2: Using SQL file**
```bash
sqlite3 library.db < add_books.sql
```

## ⌨️ Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `a` | Add Book | Opens dialog to add a new book |
| `d` | Delete Book | Deletes selected book (with confirmation) |
| `s` | Toggle Status | Switch between "read" and "unread" |
| `r` | Refresh | Reset to default view (clear search, sort by newest) |
| `t` | Toggle Theme | Cycle through 5 beautiful themes |
| `1` | Sort by Title | Alphabetical by book title |
| `2` | Sort by Author | Alphabetical by author name |
| `3` | Sort by Year | Sort by publication year |
| `/` | Search | Focus the search box |
| `↑↓` | Navigate | Move through your book list |
| `Tab` | Next Field | Move between input fields |
| `Ctrl+P` | Command Palette | Search all available commands |
| `q` | Quit | Exit the app |

## 🎨 Themes

Press `t` to cycle through:
1. **textual-dark** - Classic dark theme (default)
2. **textual-light** - Clean light theme for daytime
3. **nord** - Cool, calming blues
4. **gruvbox** - Warm, retro vibes
5. **catppuccin-mocha** - Soft pastel dark

Your theme choice is **automatically saved** and restored next time you open the app!

## 📖 How to Use

### Adding Books

1. Press **`a`** - A dialog pops up
2. Fill in the fields:
   - **Title** (required) → Tab
   - **Author** (required) → Tab
   - **Year** (optional) → Tab
   - **Genre** (optional) → Enter
3. Book added! ✅

### Searching

1. Press **`/`** or click in the search box
2. Type any text (searches title, author, genre)
3. Press **Enter** to filter
4. Press **`r`** to clear search and return to all books

### Managing Books

- **Navigate:** Use ↑↓ arrow keys
- **Change status:** Select a book, press `s` (toggles read/unread)
- **Delete:** Select a book, press `d`, confirm with arrows/Enter

### Sorting

- Press `1` for Title (A-Z)
- Press `2` for Author (A-Z)
- Press `3` for Year (oldest to newest)
- Default is newest books first (ID descending)

## 💾 Data Storage

The app creates two files in the same directory:

1. **`library.db`** - SQLite database with all your books
2. **`.library_config.json`** - Stores your preferences (theme)

Your data persists between sessions - close and reopen anytime!

## 🛠️ Technical Details

- **Language:** Python 3
- **UI Framework:** [Textual](https://github.com/Textualize/textual) (modern TUI framework)
- **Database:** SQLite3 (built into Python)
- **No external dependencies** except Textual

## 🎯 Why This Project?

Because sometimes you just want to:
- Track your books without opening a browser
- Stay in your terminal workflow
- Have a lightweight, distraction-free reading list
- Build something fun with cool TUI tech!

This app is inspired by tools like `tview` (Go), `ncurses`, and the philosophy that not everything needs to be a web app or Electron monstrosity. Sometimes, the terminal is all you need. 🖥️✨

## 📝 Database Schema

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    status TEXT DEFAULT 'unread',
    added_date TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🤝 Contributing

This is a fun hobby project! Feel free to fork it, modify it, or use it as inspiration for your own terminal apps.

## 📄 License

Do whatever you want with this code - it's a fun learning project! 🎉

---

**Happy reading! 📚**

Built with ❤️ and ☕ for terminal enthusiasts everywhere.