import os
from services.scanner import scan_directory
from services.organizer import generate_dry_run_map, move_files
from services.history import save_history, undo_last_run, load_history

class OrganizerEngine:
    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.last_scan_results = None
        self.last_dry_run_map = None

    def scan(self):
        """
        Scans the target directory and updates internal scan results.
        Returns the scan results dict.
        """
        if not self.target_directory or not os.path.isdir(self.target_directory):
            raise ValueError("Invalid target directory path.")
            
        self.last_scan_results = scan_directory(self.target_directory)
        self.last_dry_run_map = None
        return self.last_scan_results

    def get_dry_run(self):
        """
        Generates and returns the dry run movement map (src -> dst).
        """
        if not self.last_scan_results:
            self.scan()
            
        self.last_dry_run_map = generate_dry_run_map(self.last_scan_results, self.target_directory)
        return self.last_dry_run_map

    def organize(self):
        """
        Executes the file organization based on the current dry run.
        Saves transaction to history.
        Returns (successful_moves, errors).
        """
        dry_run_map = self.get_dry_run()
        if not dry_run_map:
            return {}, ["No files found to organize."]
            
        successful_moves, errors = move_files(dry_run_map)
        
        # Save to history file if any moves were successful
        if successful_moves:
            save_history(self.target_directory, successful_moves)
            
        # Reset scanner cache since files have been moved
        self.last_scan_results = None
        self.last_dry_run_map = None
        
        return successful_moves, errors

    def undo(self):
        """
        Undoes the last organization run in the target directory.
        Returns (reverted_moves, errors).
        """
        if not self.target_directory or not os.path.isdir(self.target_directory):
            raise ValueError("Invalid target directory path.")
            
        reverted_moves, errors = undo_last_run(self.target_directory)
        
        # Reset scanner cache
        self.last_scan_results = None
        self.last_dry_run_map = None
        
        return reverted_moves, errors

    def is_undo_available(self):
        """
        Checks if there is a history file available to undo in the target directory.
        """
        if not self.target_directory or not os.path.isdir(self.target_directory):
            return False
        return load_history(self.target_directory) is not None
