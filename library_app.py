#!/usr/bin/env python3
"""
Terminal Library Manager - A simple TUI app for managing your book collection
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Header, Footer, DataTable, Static, Input, Button, Label
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import events


class LibraryDatabase:
    """Handle all database operations"""
    
    def __init__(self, db_path="library.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the books table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()
    
    def add_book(self, title, author, year=None, genre=None, status='unread'):
        """Add a new book to the library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, year, genre, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, year, genre, status))
        conn.commit()
        conn.close()
    
    def get_all_books(self, sort_by='title', search_term=None):
        """Retrieve all books, optionally filtered and sorted"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT id, title, author, year, genre, status FROM books"
        params = []
        
        if search_term:
            query += " WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?"
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern]
        
        # Handle sort_by (can include DESC)
        valid_columns = ['title', 'author', 'year', 'genre', 'status', 'id', 'id DESC']
        if sort_by in valid_columns:
            query += f" ORDER BY {sort_by}"
        
        cursor.execute(query, params)
        books = cursor.fetchall()
        conn.close()
        return books
    
    def update_status(self, book_id, status):
        """Update the reading status of a book"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))
        conn.commit()
        conn.close()
    
    def delete_book(self, book_id):
        """Delete a book from the library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()


class Config:
    """Handle app configuration and preferences"""
    
    def __init__(self, config_path=".library_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load config from file or create default"""
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "theme": "textual-dark"
        }
    
    def save_config(self):
        """Save config to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        """Get a config value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a config value and save"""
        self.config[key] = value
        self.save_config()


class AddBookDialog(ModalScreen[dict]):
    """Modal dialog for adding a new book"""
    
    CSS = """
    AddBookDialog {
        align: center middle;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $accent;
        background: $surface;
        padding: 1 2;
    }
    
    #dialog-title {
        width: 100%;
        text-align: center;
        background: $accent;
        color: $text;
        padding: 1;
        margin-bottom: 1;
    }
    
    .input-row {
        height: auto;
        margin-bottom: 1;
    }
    
    .input-label {
        width: 12;
        padding-top: 1;
    }
    
    Input {
        width: 1fr;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label("📚 Add New Book", id="dialog-title")
            
            with Horizontal(classes="input-row"):
                yield Label("Title*:", classes="input-label")
                yield Input(placeholder="Book title", id="title-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Author*:", classes="input-label")
                yield Input(placeholder="Author name", id="author-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Year:", classes="input-label")
                yield Input(placeholder="Publication year", id="year-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Genre:", classes="input-label")
                yield Input(placeholder="Genre", id="genre-input")
            
            with Horizontal(id="button-container"):
                yield Button("Add Book", variant="primary", id="add-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the title input when dialog opens"""
        self.query_one("#title-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "add-btn":
            self.add_book()
        else:
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in any input field"""
        # If we're in the last field (genre), add the book
        if event.input.id == "genre-input":
            self.add_book()
        else:
            # Otherwise move to next field
            inputs = ["title-input", "author-input", "year-input", "genre-input"]
            current_idx = inputs.index(event.input.id)
            if current_idx < len(inputs) - 1:
                self.query_one(f"#{inputs[current_idx + 1]}", Input).focus()
    
    def add_book(self) -> None:
        """Collect data and dismiss with result"""
        title = self.query_one("#title-input", Input).value.strip()
        author = self.query_one("#author-input", Input).value.strip()
        year = self.query_one("#year-input", Input).value.strip()
        genre = self.query_one("#genre-input", Input).value.strip()
        
        if not title or not author:
            # Could add error display here
            return
        
        result = {
            "title": title,
            "author": author,
            "year": int(year) if year.isdigit() else None,
            "genre": genre or None
        }
        
        self.dismiss(result)


class ConfirmDeleteDialog(ModalScreen[bool]):
    """Modal dialog for confirming book deletion"""
    
    CSS = """
    ConfirmDeleteDialog {
        align: center middle;
    }
    
    #confirm-dialog {
        width: 50;
        height: auto;
        border: thick $error;
        background: $surface;
        padding: 1 2;
    }
    
    #confirm-title {
        width: 100%;
        text-align: center;
        background: $error;
        color: $text;
        padding: 1;
        margin-bottom: 1;
    }
    
    #confirm-message {
        width: 100%;
        text-align: center;
        padding: 1;
        margin-bottom: 1;
    }
    
    #confirm-book-info {
        width: 100%;
        text-align: center;
        color: $warning;
        padding: 1;
        margin-bottom: 1;
    }
    
    #confirm-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    #confirm-buttons Button {
        margin: 0 1;
    }
    """
    
    def __init__(self, book_title: str, book_author: str):
        super().__init__()
        self.book_title = book_title
        self.book_author = book_author
    
    def compose(self) -> ComposeResult:
        with Container(id="confirm-dialog"):
            yield Label("⚠️  Delete Book?", id="confirm-title")
            yield Static("Are you sure you want to delete:", id="confirm-message")
            yield Static(f'"{self.book_title}"\nby {self.book_author}', id="confirm-book-info")
            
            with Horizontal(id="confirm-buttons"):
                yield Button("Delete", variant="error", id="confirm-yes")
                yield Button("Cancel", variant="primary", id="confirm-no")
    
    def on_mount(self) -> None:
        """Focus the Cancel button by default (safer)"""
        self.query_one("#confirm-no", Button).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "confirm-yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
    
    def on_key(self, event) -> None:
        """Handle keyboard shortcuts"""
        if event.key == "y":
            self.dismiss(True)
            event.prevent_default()
        elif event.key == "n" or event.key == "escape":
            self.dismiss(False)
            event.prevent_default()
        elif event.key == "left":
            # Focus Delete button
            self.query_one("#confirm-yes", Button).focus()
            event.prevent_default()
        elif event.key == "right":
            # Focus Cancel button
            self.query_one("#confirm-no", Button).focus()
            event.prevent_default()


class LibraryApp(App):
    """A Textual app to manage your book library"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        layout: horizontal;
        height: 100%;
    }
    
    #books-panel {
        width: 70%;
        border: solid $primary;
        padding: 1;
    }
    
    #control-panel {
        width: 30%;
        border: solid $accent;
        padding: 1;
    }
    
    DataTable {
        height: 100%;
    }
    
    .control-section {
        margin-bottom: 1;
        border: solid $boost;
        padding: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    .info-text {
        color: $text-muted;
        margin-bottom: 1;
    }
    
    .command-item {
        margin-bottom: 1;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("a", "add_book", "Add Book"),
        Binding("d", "delete_book", "Delete"),
        Binding("s", "toggle_status", "Toggle Status"),
        Binding("r", "refresh", "Refresh"),
        Binding("t", "toggle_theme", "Toggle Theme"),
        Binding("1", "sort_title", "Sort: Title"),
        Binding("2", "sort_author", "Sort: Author"),
        Binding("3", "sort_year", "Sort: Year"),
        Binding("slash", "focus_search", "Search"),
    ]
    
    def __init__(self):
        super().__init__()
        self.db = LibraryDatabase()
        self.config = Config()
        self.current_sort = 'id DESC'
        self.search_term = None
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        
        with Container(id="main-container"):
            with Vertical(id="books-panel"):
                yield Static("📚 My Library", classes="info-text")
                yield DataTable(id="books-table")
            
            with Vertical(id="control-panel"):
                yield Static("🔍 Search", classes="info-text")
                yield Input(placeholder="Type to search...", id="search-input")
                
                with Vertical(classes="control-section"):
                    yield Static("ℹ️  Info", classes="info-text")
                    yield Static("Use ↑↓ to select books", id="info")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the data table when the app starts"""
        # Load saved theme
        saved_theme = self.config.get("theme", "textual-dark")
        self.theme = saved_theme
        
        table = self.query_one("#books-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("ID", "Title", "Author", "Year", "Genre", "Status")
        self.refresh_table()
    
    def refresh_table(self):
        """Refresh the books table with current data"""
        table = self.query_one("#books-table", DataTable)
        
        # Save current cursor position
        current_row = table.cursor_row if table.row_count > 0 else 0
        
        table.clear()
        
        books = self.db.get_all_books(sort_by=self.current_sort, search_term=self.search_term)
        
        for book in books:
            # Add row with styled status
            status_display = f"[green]{book[5]}[/green]" if book[5] == "read" else f"[yellow]{book[5]}[/yellow]"
            table.add_row(
                str(book[0]),  # ID
                book[1],       # Title
                book[2],       # Author
                str(book[3]) if book[3] else "-",  # Year
                book[4] if book[4] else "-",       # Genre
                status_display  # Status
            )
        
        # Restore cursor position
        if table.row_count > 0 and current_row >= 0:
            # Make sure we don't go past the end if rows were deleted
            restore_row = min(current_row, table.row_count - 1)
            table.move_cursor(row=restore_row)
    
    def action_add_book(self) -> None:
        """Show the add book dialog"""
        def handle_result(result):
            if result:
                self.db.add_book(
                    result["title"],
                    result["author"],
                    result["year"],
                    result["genre"]
                )
                self.refresh_table()
                self.query_one("#info", Static).update(f"✅ Added: {result['title']}")
        
        self.push_screen(AddBookDialog(), handle_result)
    
    def action_delete_book(self) -> None:
        """Delete the currently selected book (with confirmation)"""
        table = self.query_one("#books-table", DataTable)
        if table.cursor_row < 0 or table.row_count == 0:
            return
        
        row_key = table.get_row_at(table.cursor_row)
        book_id = int(row_key[0])
        title = row_key[1]
        author = row_key[2]
        
        def handle_confirm(confirmed: bool):
            if confirmed:
                self.db.delete_book(book_id)
                self.refresh_table()
                self.query_one("#info", Static).update(f"🗑️  Deleted: {title}")
            else:
                self.query_one("#info", Static).update("❌ Delete cancelled")
        
        self.push_screen(ConfirmDeleteDialog(title, author), handle_confirm)
    
    def action_toggle_status(self) -> None:
        """Toggle the reading status of the selected book"""
        table = self.query_one("#books-table", DataTable)
        if table.cursor_row < 0 or table.row_count == 0:
            return
        
        row_key = table.get_row_at(table.cursor_row)
        book_id = int(row_key[0])
        current_status = row_key[5].replace("[green]", "").replace("[yellow]", "").replace("[/green]", "").replace("[/yellow]", "")
        
        new_status = "read" if current_status == "unread" else "unread"
        self.db.update_status(book_id, new_status)
        self.refresh_table()
        self.query_one("#info", Static).update(f"📖 Status: {new_status}")
    
    def action_refresh(self) -> None:
        """Refresh the table - reset to default sort and clear search"""
        self.current_sort = 'id DESC'
        self.search_term = None
        self.query_one("#search-input", Input).value = ""
        self.refresh_table()
        self.query_one("#info", Static).update("🔄 Reset to default view")
    
    def action_sort_title(self) -> None:
        """Sort books by title"""
        self.current_sort = 'title'
        self.refresh_table()
        self.query_one("#info", Static).update("📑 Sorted by Title")
    
    def action_sort_author(self) -> None:
        """Sort books by author"""
        self.current_sort = 'author'
        self.refresh_table()
        self.query_one("#info", Static).update("📑 Sorted by Author")
    
    def action_sort_year(self) -> None:
        """Sort books by year"""
        self.current_sort = 'year'
        self.refresh_table()
        self.query_one("#info", Static).update("📑 Sorted by Year")
    
    def action_focus_search(self) -> None:
        """Focus the search input"""
        self.query_one("#search-input", Input).focus()
    
    def action_toggle_theme(self) -> None:
        """Toggle between dark and light themes"""
        current_theme = self.theme
        
        # Cycle through available themes
        if current_theme == "textual-dark":
            new_theme = "textual-light"
        elif current_theme == "textual-light":
            new_theme = "nord"
        elif current_theme == "nord":
            new_theme = "gruvbox"
        elif current_theme == "gruvbox":
            new_theme = "catppuccin-mocha"
        else:
            new_theme = "textual-dark"
        
        self.theme = new_theme
        self.config.set("theme", new_theme)
        self.query_one("#info", Static).update(f"🎨 Theme: {new_theme}")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submissions"""
        if event.input.id == "search-input":
            self.search_term = event.value.strip() or None
            self.refresh_table()
            self.query_one("#info", Static).update(f"🔍 Search: {self.search_term or 'All'}")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()