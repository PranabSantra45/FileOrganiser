import os

# Map categories to their corresponding file extensions (lowercase)
EXTENSION_MAP = {
    'Images': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.bmp', '.svg'},
    'Videos': {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.3gp'},
    'Documents': {'.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.csv', '.md', '.rtf', '.odt', '.ods', '.odp', '.xls', '.doc', '.ppt'},
    'Audio': {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma'},
    'Archives': {'.zip', '.rar', '.tar', '.gz', '.7z', '.bz2'},
    'Installers': {'.apk', '.exe', '.msi', '.dmg'}
}

# The name of the history log file that scanner should ignore
HISTORY_FILE_NAME = '.organiser_history.json'

def get_category_for_extension(ext):
    """
    Returns the category name (e.g., 'Images') based on the extension.
    Returns 'Others' if the extension is not in the map.
    """
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return 'Others'

def scan_directory(directory_path):
    """
    Scans the given directory and categorizes files.
    Returns a dictionary structured as:
    {
        'Categories': {
            'Images': [file_paths...],
            'Videos': [file_paths...],
            ...
        },
        'TotalFiles': int,
        'Ignored': [file_paths...]
    }
    """
    result = {
        'Categories': {cat: [] for cat in list(EXTENSION_MAP.keys()) + ['Others']},
        'TotalFiles': 0,
        'Ignored': []
    }

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return result

    for entry in os.scandir(directory_path):
        # We only organize files, skip subdirectories
        if entry.is_file():
            filename = entry.name
            
            # Skip history file and any hidden file (starting with .)
            if filename == HISTORY_FILE_NAME or filename.startswith('.'):
                result['Ignored'].append(entry.path)
                continue

            _, ext = os.path.splitext(filename)
            category = get_category_for_extension(ext)
            result['Categories'][category].append(entry.path)
            result['TotalFiles'] += 1

    return result
