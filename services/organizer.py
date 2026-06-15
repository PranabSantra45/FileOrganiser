import os
import shutil

def get_unique_target_path(target_dir, filename):
    """
    Checks if a file already exists in target_dir. If so, appends a numeric suffix
    (e.g., file_1.ext, file_2.ext) to ensure it is unique.
    Returns the unique absolute target path.
    """
    base, ext = os.path.splitext(filename)
    target_path = os.path.join(target_dir, filename)
    counter = 1
    
    while os.path.exists(target_path):
        new_filename = f"{base}_{counter}{ext}"
        target_path = os.path.join(target_dir, new_filename)
        counter += 1
        
    return target_path

def generate_dry_run_map(scan_results, directory_path):
    """
    Generates a map of proposed file moves: {original_path: target_path}.
    Ensures that name collisions in the target folders are resolved.
    """
    move_map = {}
    categories = scan_results.get('Categories', {})
    
    # We want to process each category
    for category, files in categories.items():
        if not files:
            continue
        
        target_category_dir = os.path.join(directory_path, category)
        
        # Keep track of files we plan to move in this dry run run so we don't collide with our own proposed names
        proposed_names = set()
        
        for file_path in files:
            filename = os.path.basename(file_path)
            
            # Resolve collision inside target_category_dir
            base, ext = os.path.splitext(filename)
            temp_path = os.path.join(target_category_dir, filename)
            counter = 1
            
            # Check if file exists on disk OR is already proposed in this dry run
            while os.path.exists(temp_path) or temp_path in proposed_names:
                new_filename = f"{base}_{counter}{ext}"
                temp_path = os.path.join(target_category_dir, new_filename)
                counter += 1
                
            proposed_names.add(temp_path)
            move_map[file_path] = temp_path
            
    return move_map

def move_files(move_map):
    """
    Executes the file moves defined in move_map.
    Creates target directories as needed.
    Returns a dictionary of successful moves: {target_path: original_path}
    (to make undo operations straightforward) and a list of errors.
    """
    successful_moves = {}
    errors = []
    
    for src, dst in move_map.items():
        if not os.path.exists(src):
            errors.append(f"Source file not found: {src}")
            continue
            
        dst_dir = os.path.dirname(dst)
        try:
            # Create target folder if it doesn't exist
            os.makedirs(dst_dir, exist_ok=True)
            # Move file
            shutil.move(src, dst)
            successful_moves[dst] = src  # Store destination -> source to revert easily
        except Exception as e:
            errors.append(f"Failed to move {os.path.basename(src)}: {str(e)}")
            
    return successful_moves, errors
