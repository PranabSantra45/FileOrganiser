# Smart FileFlow (v1.0.1)

Smart FileFlow is a premium, responsive cross-platform file organizer utility built using Python, Kivy, and KivyMD. Designed with a custom modern **Sleek Dark Mode** interface, it allows users to scan directories, view live dry-run previews of proposed moves, categorize files by their extensions, and organize them into standard folders with full **Undo** transaction support.

The application is fully optimized to run on both **Desktop** (Windows, macOS, Linux) and **Android devices** (targeting Android 13+ / API 34).

---

## Features

- **Obsidian Dark Theme**: A visually striking UI styled in deep charcoal (`#121620`) with neon cyan and gradient accents.
- **Dynamic File Scanning**: Automatically groups files into categories: `Images`, `Videos`, `Documents`, `Audio`, `Archives`, `Installers`, and `Others`.
- **One-Tap Quick Shortcuts**: Fast-click cards to instantly access common Android folders (Downloads, Pictures, Documents, Music) with built-in existence checks.
- **Dry-Run Preview**: A scrollable preview pane that displays proposed paths (`[Filename] ➔ [Category]/[Filename]`) before committing the changes.
- **Conflict Resolution**: Smart renaming logic (e.g., `photo_1.jpg`) to prevent file collisions during organization.
- **Undo last Run**: Transaction history logs allow the user to revert the last organization run instantly, returning files to their original paths.
- **Android Scoped Storage Bridge**: Full support for Android 11+ All Files Access (`MANAGE_EXTERNAL_STORAGE`) permissions using a Java bridge (`pyjnius`).
- **Lazy Dialog Initializer**: Deferral of complex UI widget constructions until requested, protecting the app from launch-time OpenGL context crashes on Android.
- **Automated Tests**: Unit test suite verifying scanner classification, renaming, dry-run mapping, and undo systems.

## Screens

<img width="200" height="400" alt="Screenshot_20260616-002453" src="https://github.com/user-attachments/assets/0da71588-3a44-4bcb-ab55-eb99ac27d317" />
<img width="200" height="400" alt="Screenshot_20260616-002507" src="https://github.com/user-attachments/assets/c5963dcd-a106-4fbb-ae88-87083c6a4221" />
<img width="200" height="400" alt="Screenshot_20260616-004531" src="https://github.com/user-attachments/assets/1581cc58-8107-4be9-91de-a6712d2b33ee" />

---

## Project Structure

```
File Organizer/
│
├── main.py               # Application entry point & permission controllers
├── organizer.kv          # Declarative Kivy Layout markup (styling & widgets)
├── organizer_engine.py   # Facade class coordinating history, scanner & mover
│
├── services/
│   ├── scanner.py        # File classification by extensions
│   ├── organizer.py      # Dry-run mapper & collision-free file mover
│   └── history.py        # Transaction logger (.organiser_history.json) & Undo logic
│
├── ui/
│   ├── dashboard.py      # Custom UI widgets (CategoryCard, FilePreviewItem)
│   └── dialogs.py        # Custom dialogs (Folder Picker, confirm, alert)
│
├── tests/
│   └── test_organizer.py # Automated test suite running in isolated directories
│
├── buildozer.spec        # Build configuration specifications for Android packaging
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

---

## Desktop Setup & Running

### Prerequisites
* Python 3.10 to 3.11 installed.

### Setup
1. **Clone the repository** and navigate to the folder:
   ```bash
   cd "File Organizer"
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv "file organiser venv"
   ```

3. **Install Dependencies**:
   * **Windows (PowerShell)**:
     ```powershell
     & ".\file organiser venv\Scripts\pip" install -r requirements.txt
     ```
   * **Linux/macOS**:
     ```bash
     source "file organiser venv/bin/activate"
     pip install -r requirements.txt
     ```

4. **Run the Application**:
   * **Windows (PowerShell)**:
     ```powershell
     & ".\file organiser venv\Scripts\python" main.py
     ```
   * **Linux/macOS**:
     ```bash
     python main.py
     ```

5. **Run the Test Suite**:
   ```bash
   python -m unittest tests/test_organizer.py
   ```

---

## Android Compilation & Installation

The application uses **Buildozer** and **python-for-android** to package Kivy into a native Android APK.

### Target Specifications
* **Target SDK**: API 34 (Android 14)
* **Minimum SDK**: API 21 (Android 5.0)
* **Required Libraries**: `kivy==2.3.1`, `kivymd==1.2.0`, `pyjnius`, `android`, `pillow`
* **Declared Permissions**: `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `MANAGE_EXTERNAL_STORAGE` (All Files Access)

### Building via GitHub Actions (Recommended)
1. Commit and push changes to your `main` branch.
2. The GitHub Actions workflow **Build Android APK** will trigger automatically.
3. Once completed, navigate to the run summary page on GitHub and download the compiled `Smart-FileFlow-v1.0.0-debug` zip artifact.

### Installing and Running on Android
1. Transfer the extracted `.apk` file to your Android phone.
2. Install the APK. (If prompted by Google Play Protect, choose **Install anyway**).
3. **Grant Storage Permissions**:
   * On startup, after the splash screen finishes, the app will transition to the dashboard and display a permission dialog.
   * Tap **Confirm** to be redirected to Android's native system settings screen.
   * Toggle **Allow access to manage all files** for **Smart FileFlow**, then press back to return to the app.
4. **Organize Folders**:
   * Tap the **Folder Picker Icon** (starts at `/storage/emulated/0`) to select any folder.
   * Alternatively, use a **Quick Shortcut** card to instantly load common folders.
   * Click **SCAN** to review proposed changes, and **ORGANIZE** to structure your files!
