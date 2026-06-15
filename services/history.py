import os
import json
import shutil

HISTORY_FILE_NAME = '.organiser_history.json'

def save_history(directory_path, successful_moves):
    """
    Saves successful moves to a hidden history JSON file in the target directory.
    successful_moves format: {target_path: original_path}
    """
    history_file_path = os.path.join(directory_path, HISTORY_FILE_NAME)
    
    # We serialize the paths. Since they might be absolute, we just write them as is.
    try:
        with open(history_file_path, 'w', encoding='utf-8') as f:
            json.dump(successful_moves, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving history: {e}")
        return False

def load_history(directory_path):
    """
    Loads and returns the history data from .organiser_history.json.
    Returns None if no history exists or it is invalid.
    """
    history_file_path = os.path.join(directory_path, HISTORY_FILE_NAME)
    if not os.path.exists(history_file_path):
        return None
        
    try:
        with open(history_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
        return None

def undo_last_run(directory_path):
    """
    Reads the history log and moves files back to their original locations.
    Then, cleans up empty directories and deletes the history file.
    Returns: (successful_reverts, errors)
    """
    history = load_history(directory_path)
    if not history:
        return {}, ["No organization history found to undo."]

    reverted_moves = {}
    errors = []
    
    # history is a dict of {current_path (target_path): original_path}
    for current_path, original_path in history.items():
        if not os.path.exists(current_path):
            errors.append(f"File to restore not found: {current_path}")
            continue
            
        original_dir = os.path.dirname(original_path)
        try:
            # Recreate original folder if it was deleted
            os.makedirs(original_dir, exist_ok=True)
            shutil.move(current_path, original_path)
            reverted_moves[original_path] = current_path
        except Exception as e:
            errors.append(f"Failed to restore {os.path.basename(current_path)}: {str(e)}")

    # Clean up empty folders created during organization (the categories)
    # Category folders are immediate subdirectories of directory_path
    for current_path in history.keys():
        category_dir = os.path.dirname(current_path)
        # Verify it's a subdirectory of our directory_path
        if os.path.abspath(category_dir) != os.path.abspath(directory_path):
            # Check if directory is empty now
            if os.path.exists(category_dir) and not os.listdir(category_dir):
                try:
                    os.rmdir(category_dir)
                except Exception:
                    pass  # Ignore failure to delete dir (might not be empty or locked)

    # Delete history file
    history_file_path = os.path.join(directory_path, HISTORY_FILE_NAME)
    if os.path.exists(history_file_path):
        try:
            os.remove(history_file_path)
        except Exception as e:
            errors.append(f"Failed to remove history file: {str(e)}")

    return reverted_moves, errors
