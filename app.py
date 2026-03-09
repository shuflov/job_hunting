#!/usr/bin/env python3
"""
Terminal Job Hunting Manager - A simple TUI app for managing your job applications
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DataTable, Static, Input, Button, Label
from textual.binding import Binding
from textual.screen import ModalScreen


class JobDatabase:
    """Handle all database operations"""
    
    def __init__(self, db_path="job_hunting.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the jobs table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                location TEXT,
                salary TEXT,
                status TEXT DEFAULT 'open',
                applied_date TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                added_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_job(self, company, position, location=None, salary=None, status='open', applied_date=None, notes=None):
        """Add a new job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Use current date if not provided
        if not applied_date:
            applied_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT INTO jobs (company, position, location, salary, status, applied_date, last_updated, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (company, position, location, salary, status, applied_date, applied_date, notes))
        conn.commit()
        conn.close()
    
    def get_all_jobs(self, sort_by='company', search_term=None):
        """Retrieve all jobs, optionally filtered and sorted"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT id, company, position, location, salary, status, applied_date, last_updated, notes FROM jobs"
        params = []
        
        if search_term:
            query += " WHERE company LIKE ? OR position LIKE ? OR location LIKE ? OR notes LIKE ?"
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern, search_pattern]
        
        # Handle sort_by (can include DESC)
        valid_columns = ['company', 'position', 'location', 'salary', 'status', 'applied_date', 'last_updated', 'id', 'id DESC']
        if sort_by in valid_columns:
            query += f" ORDER BY {sort_by}"
        
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    
    def update_status(self, job_id, status):
        """Update the status of a job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE jobs SET status = ?, last_updated = ? WHERE id = ?", (status, last_updated, job_id))
        conn.commit()
        conn.close()
    
    def update_notes(self, job_id, notes):
        """Update the notes for a job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE jobs SET notes = ?, last_updated = ? WHERE id = ?", (notes, last_updated, job_id))
        conn.commit()
        conn.close()
    
    def delete_job(self, job_id):
        """Delete a job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        conn.close()


class Config:
    """Handle app configuration and preferences"""
    
    def __init__(self, config_path=".job_hunting_config.json"):
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


class AddJobDialog(ModalScreen[dict]):
    """Modal dialog for adding a new job application"""
    
    CSS = """
    AddJobDialog {
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
            yield Label("💼 Add New Job Application", id="dialog-title")
            
            with Horizontal(classes="input-row"):
                yield Label("Company*:", classes="input-label")
                yield Input(placeholder="Company name", id="company-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Position*:", classes="input-label")
                yield Input(placeholder="Position title", id="position-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Location:", classes="input-label")
                yield Input(placeholder="City, Country", id="location-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Salary:", classes="input-label")
                yield Input(placeholder="e.g., $80k-100k", id="salary-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Applied:", classes="input-label")
                yield Input(placeholder="YYYY-MM-DD (leave empty for today)", id="applied-input")
            
            with Horizontal(classes="input-row"):
                yield Label("Notes:", classes="input-label")
                yield Input(placeholder="Interview date, contact info, etc.", id="notes-input")
            
            with Horizontal(id="button-container"):
                yield Button("Add Job", variant="primary", id="add-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the company input when dialog opens"""
        self.query_one("#company-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "add-btn":
            self.add_job()
        else:
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in any input field"""
        # If we're in the last field (notes), add the job
        if event.input.id == "notes-input":
            self.add_job()
        else:
            # Otherwise move to next field
            inputs = ["company-input", "position-input", "location-input", "salary-input", "applied-input", "notes-input"]
            current_idx = inputs.index(event.input.id)
            if current_idx < len(inputs) - 1:
                self.query_one(f"#{inputs[current_idx + 1]}", Input).focus()
    
    def add_job(self) -> None:
        """Collect data and dismiss with result"""
        company = self.query_one("#company-input", Input).value.strip()
        position = self.query_one("#position-input", Input).value.strip()
        location = self.query_one("#location-input", Input).value.strip()
        salary = self.query_one("#salary-input", Input).value.strip()
        applied_date = self.query_one("#applied-input", Input).value.strip()
        notes = self.query_one("#notes-input", Input).value.strip()
        
        if not company or not position:
            # Could add error display here
            return
        
        result = {
            "company": company,
            "position": position,
            "location": location or None,
            "salary": salary or None,
            "applied_date": applied_date or None,
            "notes": notes or None
        }
        
        self.dismiss(result)


class ConfirmDeleteDialog(ModalScreen[bool]):
    """Modal dialog for confirming job deletion"""
    
    CSS = """
    ConfirmDeleteDialog {
        align: center middle;
    }
    
    #confirm-dialog {
        width: 50;
        height: auto;
        border: $error;
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
    
    #confirm-job-info {
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
    
    def __init__(self, position: str, company: str):
        super().__init__()
        self.position = position
        self.company = company
    
    def compose(self) -> ComposeResult:
        with Container(id="confirm-dialog"):
            yield Label("⚠️  Delete Job Application?", id="confirm-title")
            yield Static("Are you sure you want to delete:", id="confirm-message")
            yield Static(f'"{self.position}"\nat {self.company}', id="confirm-job-info")
            
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


class EditNotesDialog(ModalScreen[str]):
    """Modal dialog for editing job notes"""
    
    CSS = """
    EditNotesDialog {
        align: center middle;
    }
    
    #edit-dialog {
        width: 60;
        height: auto;
        border: thick $accent;
        background: $surface;
        padding: 1 2;
    }
    
    #edit-title {
        width: 100%;
        text-align: center;
        background: $accent;
        color: $text;
        padding: 1;
        margin-bottom: 1;
    }
    
    #edit-job-info {
        width: 100%;
        text-align: center;
        color: $text-muted;
        padding: 1;
        margin-bottom: 1;
    }
    
    #notes-input {
        width: 100%;
        height: 5;
    }
    
    #edit-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    #edit-buttons Button {
        margin: 0 1;
    }
    """
    
    def __init__(self, position: str, company: str, current_notes: str = ""):
        super().__init__()
        self.position = position
        self.company = company
        self.current_notes = current_notes
    
    def compose(self) -> ComposeResult:
        with Container(id="edit-dialog"):
            yield Label("📝 Edit Notes", id="edit-title")
            yield Static(f"{self.position} at {self.company}", id="edit-job-info")
            yield Input(value=self.current_notes, placeholder="Add notes (interview dates, contact info, etc.)", id="notes-input")
            
            with Horizontal(id="edit-buttons"):
                yield Button("Save", variant="primary", id="save-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")
    
    def on_mount(self) -> None:
        """Focus the notes input"""
        self.query_one("#notes-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "save-btn":
            notes = self.query_one("#notes-input", Input).value.strip()
            self.dismiss(notes)
        else:
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Save on Enter"""
        if event.input.id == "notes-input":
            notes = event.input.value.strip()
            self.dismiss(notes)


class JobHuntingApp(App):
    """A Textual app to manage your job applications"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #top-bar {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    
    .info-text {
        width: 1fr;
        color: $text-muted;
        padding-top: 1;
    }
    
    #search-input {
        width: 40;
    }
    
    DataTable {
        width: 100%;
        height: 1fr;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_job", "Add"),
        Binding("d", "delete_job", "Del"),
        Binding("s", "toggle_status", "Stat"),
        Binding("n", "edit_notes", "Note"),
        Binding("r", "refresh", "Refresh"),
        Binding("t", "toggle_theme", "Theme"),
        Binding("h", "toggle_hide_closed", "Hide Closed"),
        Binding("1", "sort_company", "Company"),
        Binding("2", "sort_position", "Position"),
        Binding("3", "sort_applied", "Applied"),
        Binding("4", "sort_salary", "Sal"),
        Binding("5", "sort_status", "Stat"),
        Binding("slash", "focus_search", "Search"),
    ]
    
    def __init__(self):
        super().__init__()
        self.db = JobDatabase()
        self.config = Config()
        self.current_sort = 'id DESC'
        self.search_term = None
        self.hide_closed = False  # Track if we're hiding closed jobs
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal(id="top-bar"):
                yield Static("💼 My Job Applications", classes="info-text")
                yield Input(placeholder="Search...", id="search-input")
            yield DataTable(id="jobs-table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the data table when the app starts"""
        # Load saved theme
        saved_theme = self.config.get("theme", "textual-dark")
        self.theme = saved_theme
        
        table = self.query_one("#jobs-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("ID", "Company", "Position", "Location", "Salary", "Applied", "Updated", "Status", "Notes")
        table.focus()  # Focus table by default, not search
        self.refresh_table()
    
    def on_data_table_row_highlighted(self, event) -> None:
        """Optional: could add status bar info here later"""
        pass
    
    def refresh_table(self):
        """Refresh the jobs table with current data"""
        table = self.query_one("#jobs-table", DataTable)
        
        # Save current cursor position
        current_row = table.cursor_row if table.row_count > 0 else 0
        
        table.clear()
        
        jobs = self.db.get_all_jobs(sort_by=self.current_sort, search_term=self.search_term)
        
        for job in jobs:
            # Filter out closed jobs if hide_closed is enabled
            if self.hide_closed and job[5] == "closed":
                continue
            
            # Add row with styled status
            status = job[5]
            if status == "open":
                status_display = f"[yellow]{status}[/yellow]"
            elif status == "closed":
                status_display = f"[red]{status}[/red]"
            elif status == "interview":
                status_display = f"[blue]{status}[/blue]"
            elif status == "offer":
                status_display = f"[green]{status}[/green]"
            else:
                status_display = status
            
            # Format applied date (show only date, not time)
            applied_date = job[6] if job[6] else "-"
            if applied_date != "-" and " " in applied_date:
                applied_date = applied_date.split()[0]
            
            # Format last_updated date (show only date, not time)
            last_updated = job[7] if job[7] else "-"
            if last_updated != "-" and " " in last_updated:
                last_updated = last_updated.split()[0]
            
            # Show full notes (truncate if too long)
            notes = job[8] if job[8] else "-"
            if len(notes) > 50:
                notes = notes[:47] + "..."
            
            table.add_row(
                str(job[0]),  # ID
                job[1],       # Company
                job[2],       # Position
                job[3] if job[3] else "-",  # Location
                job[4] if job[4] else "-",  # Salary
                applied_date, # Applied date
                last_updated, # Last updated date
                status_display,  # Status
                notes         # Notes
            )
        
        # Restore cursor position
        if table.row_count > 0 and current_row >= 0:
            # Make sure we don't go past the end if rows were deleted
            restore_row = min(current_row, table.row_count - 1)
            table.move_cursor(row=restore_row)
    
    def action_add_job(self) -> None:
        """Show the add job dialog"""
        def handle_result(result):
            if result:
                self.db.add_job(
                    result["company"],
                    result["position"],
                    result["location"],
                    result["salary"],
                    'open',  # default status
                    result["applied_date"],
                    result["notes"]
                )
                self.refresh_table()
        
        self.push_screen(AddJobDialog(), handle_result)
    
    def action_delete_job(self) -> None:
        """Delete the currently selected job (with confirmation)"""
        table = self.query_one("#jobs-table", DataTable)
        if table.cursor_row < 0 or table.row_count == 0:
            return
        
        row_key = table.get_row_at(table.cursor_row)
        job_id = int(row_key[0])
        company = row_key[1]
        position = row_key[2]
        
        def handle_confirm(confirmed: bool):
            if confirmed:
                self.db.delete_job(job_id)
                self.refresh_table()
        
        self.push_screen(ConfirmDeleteDialog(position, company), handle_confirm)
    
    def action_toggle_status(self) -> None:
        """Cycle through job application statuses"""
        table = self.query_one("#jobs-table", DataTable)
        if table.cursor_row < 0 or table.row_count == 0:
            return
        
        row_key = table.get_row_at(table.cursor_row)
        job_id = int(row_key[0])
        
        # Remove color formatting from status (now at index 7)
        current_status = row_key[7]
        for color in ["[yellow]", "[/yellow]", "[red]", "[/red]", "[blue]", "[/blue]", "[green]", "[/green]"]:
            current_status = current_status.replace(color, "")
        
        # Cycle through statuses: open -> interview -> offer -> closed -> open
        status_cycle = {
            "open": "interview",
            "interview": "offer",
            "offer": "closed",
            "closed": "open"
        }
        
        new_status = status_cycle.get(current_status, "open")
        self.db.update_status(job_id, new_status)
        self.refresh_table()
    
    def action_edit_notes(self) -> None:
        """Edit notes for the selected job"""
        table = self.query_one("#jobs-table", DataTable)
        if table.cursor_row < 0 or table.row_count == 0:
            return
        
        row_key = table.get_row_at(table.cursor_row)
        job_id = int(row_key[0])
        company = row_key[1]
        position = row_key[2]
        
        # Get current notes from database
        jobs = self.db.get_all_jobs()
        current_notes = ""
        for job in jobs:
            if job[0] == job_id:
                current_notes = job[8] if job[8] else ""
                break
        
        def handle_result(notes):
            if notes is not None:  # None means cancelled
                self.db.update_notes(job_id, notes)
                self.refresh_table()
        
        self.push_screen(EditNotesDialog(position, company, current_notes), handle_result)
    
    def action_refresh(self) -> None:
        """Refresh the table - reset to default sort and clear search"""
        self.current_sort = 'id DESC'
        self.search_term = None
        self.hide_closed = False
        self.query_one("#search-input", Input).value = ""
        self.update_title()
        self.refresh_table()
    
    def action_toggle_hide_closed(self) -> None:
        """Toggle hiding closed jobs"""
        self.hide_closed = not self.hide_closed
        self.update_title()
        self.refresh_table()
    
    def update_title(self):
        """Update the title to show current filter status"""
        title = "💼 My Job Applications"
        if self.hide_closed:
            title += " (Active Only)"
        self.query_one(".info-text", Static).update(title)
    
    def action_sort_company(self) -> None:
        """Sort jobs by company"""
        self.current_sort = 'company'
        self.refresh_table()
    
    def action_sort_position(self) -> None:
        """Sort jobs by position"""
        self.current_sort = 'position'
        self.refresh_table()
    
    def action_sort_applied(self) -> None:
        """Sort jobs by applied date"""
        self.current_sort = 'applied_date DESC'
        self.refresh_table()
    
    def action_sort_salary(self) -> None:
        """Sort jobs by salary"""
        self.current_sort = 'salary'
        self.refresh_table()
    
    def action_sort_status(self) -> None:
        """Sort jobs by status"""
        self.current_sort = 'status'
        self.refresh_table()
    
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
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submissions"""
        if event.input.id == "search-input":
            self.search_term = event.value.strip() or None
            self.refresh_table()


if __name__ == "__main__":
    app = JobHuntingApp()
    app.run()