# 💼 Terminal Job Hunting Manager

A lightweight, keyboard-driven terminal app for tracking your job applications! Built with Python and Textual, this app helps you stay organized during your job search without leaving the terminal.

## 🎯 About This Project

Track all your job applications in one place with a clean, distraction-free terminal interface. Perfect for:
- Developers who live in the terminal
- Anyone tired of spreadsheets for job tracking
- People who want a quick, local solution (no cloud, no signups)
- Terminal enthusiasts who appreciate keyboard-driven workflows

## ✨ Features

- 💼 **Track job applications** with company, position, location, and salary
- 📊 **Smart status tracking** - cycle through: open → interview → offer → closed
- 🔍 **Search** by company, position, or location
- 📑 **Sort** by company, position, or salary
- ➕ **Quick add** via modal dialog (Tab through fields)
- 🗑️ **Safe delete** with confirmation
- 🎨 **5 themes** (auto-saved between sessions)
- ⌨️ **100% keyboard-driven** - no mouse needed
- 💾 **SQLite database** - portable, no setup required
- 🚀 **Lightweight** - just Python + one dependency

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- That's it!

### Installation

```bash
# Install Textual
pip3 install textual

# Or use requirements.txt
pip3 install -r requirements.txt
```

### Running the App

```bash
python3 job_hunting_app.py
```

### Adding Sample Data (Optional)

```bash
# Python script
python3 add_sample_jobs.py

# Or SQL file
sqlite3 job_hunting.db < add_jobs.sql
```

## ⌨️ Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `a` | Add Job | Add a new job application |
| `d` | Delete | Delete selected job (with confirmation) |
| `s` | Toggle Status | Cycle: open → interview → offer → closed |
| `r` | Refresh | Reset view (clear search, sort by newest) |
| `t` | Toggle Theme | Switch between 5 themes |
| `1` | Sort by Company | Alphabetical by company |
| `2` | Sort by Position | Alphabetical by position |
| `3` | Sort by Salary | Sort by salary range |
| `/` | Search | Focus search box |
| `↑↓` | Navigate | Move through applications |
| `Tab` | Next Field | Move between form fields |
| `Ctrl+P` | Command Palette | Search all commands |
| `q` | Quit | Exit app |

## 📊 Status Workflow

Press `s` to cycle through statuses:

1. **open** (yellow) - Just applied
2. **interview** (blue) - Interview scheduled/in progress
3. **offer** (green) - Received an offer
4. **closed** (red) - Rejected or declined

## 🎨 Themes

Press `t` to cycle through:
1. **textual-dark** - Default dark theme
2. **textual-light** - Clean light theme
3. **nord** - Cool blues
4. **gruvbox** - Warm retro
5. **catppuccin-mocha** - Soft pastels

Your theme preference is saved automatically!

## 📖 Usage Guide

### Adding a Job Application

1. Press **`a`**
2. Fill in:
   - **Company** (required) → Tab
   - **Position** (required) → Tab
   - **Location** (optional) → Tab
   - **Salary** (optional, e.g., "$80k-100k") → Enter
3. Done! ✅

### Tracking Progress

- Select a job with ↑↓
- Press `s` to update status as you progress
- Status colors help you see at a glance:
  - 🟡 Open applications
  - 🔵 Active interviews
  - 🟢 Offers received
  - 🔴 Closed/rejected

### Searching & Organizing

- Press `/` to search by company, position, or location
- Press `1`, `2`, `3` to sort
- Press `r` to reset and view all (newest first)

## 💾 Data Storage

Creates two files in the app directory:

1. **`job_hunting.db`** - SQLite database with all your applications
2. **`.job_hunting_config.json`** - Theme preference

Both files are portable - copy them anywhere!

## 🛠️ Technical Details

- **Language:** Python 3
- **UI:** Textual (modern TUI framework)
- **Database:** SQLite3 (built into Python)
- **Dependencies:** Just textual

### Database Schema

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    status TEXT DEFAULT 'open',
    added_date TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Why This App?

Job hunting can be overwhelming. Spreadsheets are clunky. Web apps are distracting. Sometimes you just want a simple, focused tool that:
- Starts instantly
- Works offline
- Respects your privacy (all data local)
- Fits your terminal workflow
- Gets out of your way

## 📝 Tips

- **Stay organized:** Update statuses as soon as things change
- **Track everything:** Even rejections are useful data
- **Use search:** Quickly find that company you interviewed with last week
- **Backup your data:** Just copy `job_hunting.db` - it's that simple!

## 🔒 Privacy

Everything is stored locally. No cloud, no tracking, no accounts. Your job search data belongs to you.

## 🤝 .gitignore Recommendations

```
job_hunting.db
.job_hunting_config.json
__pycache__/
*.pyc
```

Keep your personal applications private while sharing the code!

---

**Good luck with your job hunt! 💼**

Built with ❤️ for terminal enthusiasts and job seekers everywhere.