import os
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window

class FolderPickerDialog:
    """
    Wrapper around KivyMD's MDFileManager to select directories.
    """
    def __init__(self, select_callback, exit_callback=None):
        self.select_callback = select_callback
        self.exit_callback = exit_callback
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            selector='folder'
        )

    def show(self, path=None):
        if not path or not os.path.exists(path):
            path = os.path.expanduser("~")
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        self.select_callback(path)

    def exit_manager(self, *args):
        self.file_manager.close()
        if self.exit_callback:
            self.exit_callback()

def show_alert_dialog(title, text, on_dismiss=None):
    """
    Shows a simple informational alert dialog.
    """
    dialog = None
    
    def dismiss(*args):
        dialog.dismiss()
        if on_dismiss:
            on_dismiss()

    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDFlatButton(
                text="OK",
                on_release=dismiss
            ),
        ],
    )
    dialog.open()
    return dialog

def show_confirm_dialog(title, text, on_confirm, on_cancel=None):
    """
    Shows a confirmation dialog with Yes and Cancel buttons.
    """
    dialog = None

    def confirm_action(*args):
        dialog.dismiss()
        on_confirm()

    def cancel_action(*args):
        dialog.dismiss()
        if on_cancel:
            on_cancel()

    dialog = MDDialog(
        title=title,
        text=text,
        buttons=[
            MDFlatButton(
                text="CANCEL",
                text_color=[0.5, 0.5, 0.5, 1],
                on_release=cancel_action
            ),
            MDRaisedButton(
                text="CONFIRM",
                on_release=confirm_action
            ),
        ],
    )
    dialog.open()
    return dialog
