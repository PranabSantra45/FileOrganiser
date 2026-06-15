# Smart File Organizer (v1)

A clean, responsive cross-platform desktop application built using Python, Kivy, and KivyMD, designed with a mobile Android Material Design interface. It scans a target folder, categorizes files by their extensions, and moves them to organized subdirectories. It also features a dry-run preview mode and an undo function to revert file operations.

## 🚀 Features

- **Extension Scanning**: Categorizes files into standard groups: `Images`, `Videos`, `Documents`, `Audio`, `Archives`, `Installers`, and `Others`.
- **Stats Dashboard**: Colored Material cards showing the file counts per category.
- **Dry Run Preview**: Displays a scrollable list of proposed file moves before executing them.
- **Safe Execution**: Renames files with numeric suffixes (e.g. `file_1.png`) if there is a filename collision in the target folder.
- **Undo Operation**: Restores files back to their original locations and cleans up empty category folders.
- **Unit Tests**: Full test suite validating the scanner, organizer, and history services.

---

## 📂 Project Structure

```
File Organizer/
│
├── main.py               # Application entry point and UI controller
├── organizer.kv          # Kivy declarative styling and UI layout
├── organizer_engine.py   # Backend Facade class coordinating services
│
├── services/
│   ├── scanner.py        # File scanning and classification logic
│   ├── organizer.py      # Dry run mapping and file moves execution
│   └── history.py        # History tracking (.organiser_history.json) and undo logic
│
├── ui/
│   ├── dashboard.py      # Custom UI widgets (CategoryCard, FilePreviewItem)
│   └── dialogs.py        # Custom dialogs (Folder Picker, confirm, alert)
│
├── tests/
│   └── test_organizer.py # Automated unit testing suite
│
├── assets/               # Folder for application media resources
├── requirements.txt      # List of dependencies (kivy, kivymd)
└── .gitignore            # Git ignored files (virtual envs, test files, logs)
```

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.10 or higher installed on your computer.

### Setup and Running

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd "File Organizer"
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv "file organiser venv"
   ```

3. **Install Dependencies**:
   - On Windows (PowerShell):
     ```powershell
     & ".\file organiser venv\Scripts\pip" install -r requirements.txt
     ```
   - On Linux/macOS:
     ```bash
     source "file organiser venv/bin/activate"
     pip install -r requirements.txt
     ```

4. **Run Unit Tests**:
   - On Windows (PowerShell):
     ```powershell
     & ".\file organiser venv\Scripts\python" -m unittest tests/test_organizer.py
     ```
   - On Linux/macOS:
     ```bash
     python -m unittest tests/test_organizer.py
     ```

5. **Run the Application**:
   - On Windows (PowerShell):
     ```powershell
     & ".\file organiser venv\Scripts\python" main.py
     ```
   - On Linux/macOS:
     ```bash
     python main.py
     ```
