import os
from kivy.config import Config
# Set window size before importing other Kivy modules
Config.set('graphics', 'width', '380')
Config.set('graphics', 'height', '680')
Config.set('graphics', 'resizable', '0')

from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.clock import Clock
from ui.dashboard import CategoryCard, FilePreviewItem
from ui.dialogs import FolderPickerDialog, show_alert_dialog, show_confirm_dialog
from organizer_engine import OrganizerEngine


# Category styling configuration (vivid accent colors for dark mode)
CATEGORY_STYLES = {
    'Images': {'icon': 'image', 'color': [0.13, 0.59, 0.95, 1]},       # Bright Blue
    'Videos': {'icon': 'video', 'color': [0.91, 0.12, 0.39, 1]},       # Pinkish Red
    'Documents': {'icon': 'file-document', 'color': [0.3, 0.69, 0.31, 1]}, # Vivid Green
    'Audio': {'icon': 'music', 'color': [0.61, 0.15, 0.69, 1]},        # Vibrant Purple
    'Archives': {'icon': 'zip-box', 'color': [1, 0.6, 0.0, 1]},         # Vivid Orange
    'Installers': {'icon': 'android', 'color': [0.0, 0.74, 0.83, 1]},   # Neon Cyan
    'Others': {'icon': 'file-question', 'color': [0.62, 0.62, 0.62, 1]} # Grey
}

def get_file_icon(filename):
    _, ext = os.path.splitext(filename.lower())
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.bmp', '.svg']:
        return "file-image-outline"
    elif ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm']:
        return "file-video-outline"
    elif ext in ['.pdf']:
        return "file-pdf-box"
    elif ext in ['.doc', '.docx', '.odt']:
        return "file-word-box"
    elif ext in ['.xls', '.xlsx', '.ods']:
        return "file-excel-box"
    elif ext in ['.ppt', '.pptx', '.odp']:
        return "file-powerpoint-box"
    elif ext in ['.txt', '.rtf', '.csv', '.md']:
        return "file-document-outline"
    elif ext in ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']:
        return "file-music-outline"
    elif ext in ['.zip', '.rar', '.tar', '.gz', '.7z', '.bz2']:
        return "file-zip-box"
    elif ext in ['.apk']:
        return "android"
    else:
        return "file-outline"

class FileOrganizerApp(MDApp):
    target_dir = StringProperty("")

    def build(self):
        self.title = "Smart FileFlow"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Dark"
        self.engine = None
        self.folder_picker = FolderPickerDialog(self.on_folder_selected)
        
        # Load the ScreenManager layout
        root = Builder.load_file('organizer.kv')
        root.transition = FadeTransition(duration=0.6)
        return root

    def select_quick_folder(self, folder_name):
        home = os.path.expanduser("~")
        path = os.path.join(home, folder_name)
        if os.path.exists(path):
            self.target_dir = path
            self.on_dir_text_change(path)
        else:
            show_alert_dialog(
                "Directory Not Found", 
                f"The folder '{folder_name}' was not found at:\n{path}"
            )

    def on_start(self):
        # Initialize the Category cards with 0 files
        self.update_stats_ui({})
        
        # Propose default directory (Downloads folder)
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(downloads_path):
            self.target_dir = downloads_path
            self.on_dir_text_change(downloads_path)
            
        # Transition from welcome screen to main screen after 2.5 seconds
        Clock.schedule_once(self.transition_to_main, 2.5)

    def transition_to_main(self, dt):
        if self.root:
            self.root.current = "main_screen"


    def open_folder_picker(self):
        self.folder_picker.show(self.target_dir)

    def on_folder_selected(self, path):
        self.target_dir = path
        self.on_dir_text_change(path)

    def on_dir_text_change(self, text):
        # Enable or disable buttons based on text path validity
        if os.path.exists(text) and os.path.isdir(text):
            self.root.ids.dir_input.error = False
            self.root.ids.btn_scan.disabled = False
            self.engine = OrganizerEngine(text)
            
            # Check if undo is available in this folder
            if self.engine.is_undo_available():
                self.root.ids.btn_undo.disabled = False
            else:
                self.root.ids.btn_undo.disabled = True
        else:
            self.root.ids.dir_input.error = True
            self.root.ids.btn_scan.disabled = True
            self.root.ids.btn_organize.disabled = True
            self.root.ids.btn_undo.disabled = True
            self.engine = None

    def trigger_scan(self):
        if not self.engine:
            return
        
        try:
            # 1. Scan directory
            results = self.engine.scan()
            
            # 2. Update stats cards
            self.update_stats_ui(results.get('Categories', {}))
            
            # 3. Generate Dry Run Preview
            dry_run_map = self.engine.get_dry_run()
            self.update_preview_ui(dry_run_map)
            
            # 4. Handle organize button state
            if dry_run_map:
                self.root.ids.btn_organize.disabled = False
            else:
                self.root.ids.btn_organize.disabled = True
                
        except Exception as e:
            show_alert_dialog("Error Scanning", f"An error occurred during scan:\n{str(e)}")

    def update_stats_ui(self, categories_data):
        """
        Dynamically builds/updates the cards in the statistics grid.
        """
        grid = self.root.ids.stats_grid
        grid.clear_widgets()
        
        for category, style in CATEGORY_STYLES.items():
            count = len(categories_data.get(category, []))
            card = CategoryCard(
                category_name=category,
                file_count=count,
                icon_name=style['icon'],
                bg_color=style['color']
            )
            grid.add_widget(card)

    def update_preview_ui(self, dry_run_map):
        """
        Populates the scrollable preview pane with proposed moves.
        """
        preview_container = self.root.ids.preview_list
        preview_container.clear_widgets()
        
        if not dry_run_map:
            # Add back the default label
            label = self.root.ids.empty_preview_label
            label.text = "No files found to organize. Directory is clean!"
            preview_container.add_widget(label)
            return

        # Disable the default label and show files
        for i, (src, dst) in enumerate(dry_run_map.items()):
            filename = os.path.basename(src)
            # Show target path relative to target_dir for cleaner display
            rel_dst = os.path.relpath(dst, self.target_dir)
            icon = get_file_icon(filename)
            
            item = FilePreviewItem(
                filename=filename,
                target_path=rel_dst,
                index=i,
                icon_name=icon
            )
            preview_container.add_widget(item)



    def trigger_organize(self):
        if not self.engine:
            return
            
        dry_run_map = self.engine.get_dry_run()
        num_files = len(dry_run_map)
        
        def confirm():
            try:
                successful_moves, errors = self.engine.organize()
                
                # Show result dialog
                num_success = len(successful_moves)
                if errors:
                    err_msg = "\n".join(errors[:5])
                    if len(errors) > 5:
                        err_msg += f"\n...and {len(errors) - 5} more."
                    show_alert_dialog(
                        "Organization Completed with Errors", 
                        f"Moved {num_success} files.\nErrors:\n{err_msg}"
                    )
                else:
                    show_alert_dialog(
                        "Success", 
                        f"Successfully organized {num_success} files!"
                    )
                
                # Refresh UI
                self.trigger_scan()
                self.root.ids.btn_undo.disabled = False
                
            except Exception as e:
                show_alert_dialog("Error Organizing", str(e))

        show_confirm_dialog(
            title="Confirm Organization",
            text=f"Are you sure you want to organize {num_files} files into categories?",
            on_confirm=confirm
        )

    def trigger_undo(self):
        if not self.engine:
            return
            
        def confirm():
            try:
                reverted_moves, errors = self.engine.undo()
                num_reverted = len(reverted_moves)
                
                if errors:
                    err_msg = "\n".join(errors[:5])
                    show_alert_dialog("Undo Completed with Errors", f"Reverted {num_reverted} files.\nErrors:\n{err_msg}")
                else:
                    show_alert_dialog("Success", f"Successfully reverted {num_reverted} files!")
                
                # Refresh UI
                self.trigger_scan()
                self.root.ids.btn_undo.disabled = True
                
            except Exception as e:
                show_alert_dialog("Error Reverting", str(e))

        show_confirm_dialog(
            title="Confirm Undo",
            text="Are you sure you want to revert the last organization? Files will be moved back to their original spots.",
            on_confirm=confirm
        )

    def show_help(self):
        show_alert_dialog(
            title="How to Use",
            text=(
                "1. Select a folder you want to clean up using the folder button.\n"
                "2. Click SCAN to inspect what files are present and see a dry run preview of moves.\n"
                "3. Review the proposed changes in the preview panel.\n"
                "4. Click ORGANIZE to move files into category subdirectories (Images, Documents, etc.).\n"
                "5. If you change your mind, click UNDO LAST to revert the last run."
            )
        )

if __name__ == '__main__':
    FileOrganizerApp().run()
