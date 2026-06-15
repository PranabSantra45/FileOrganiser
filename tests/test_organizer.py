import os
import shutil
import tempfile
import unittest
from services.scanner import scan_directory
from services.organizer import generate_dry_run_map, move_files
from services.history import save_history, load_history, undo_last_run
from organizer_engine import OrganizerEngine

class TestOrganizer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        
        # Create some dummy files
        self.files = {
            'photo1.jpg': 'image content',
            'photo2.PNG': 'image content',
            'doc1.pdf': 'pdf content',
            'doc2.docx': 'docx content',
            'song.mp3': 'audio content',
            'archive.zip': 'zip content',
            'installer.apk': 'apk content',
            'unknown.xyz': 'unknown content'
        }
        
        for name, content in self.files.items():
            path = os.path.join(self.test_dir, name)
            with open(path, 'w') as f:
                f.write(content)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_scanner_categorization(self):
        results = scan_directory(self.test_dir)
        
        self.assertEqual(results['TotalFiles'], 8)
        self.assertEqual(len(results['Categories']['Images']), 2)
        self.assertEqual(len(results['Categories']['Documents']), 2)
        self.assertEqual(len(results['Categories']['Audio']), 1)
        self.assertEqual(len(results['Categories']['Archives']), 1)
        self.assertEqual(len(results['Categories']['Installers']), 1)
        self.assertEqual(len(results['Categories']['Others']), 1)

    def test_dry_run_and_execution(self):
        engine = OrganizerEngine(self.test_dir)
        scan_results = engine.scan()
        
        # Check that dry run generates correct target paths
        dry_run_map = engine.get_dry_run()
        self.assertEqual(len(dry_run_map), 8)
        
        # Verify target folders in dry run
        for src, dst in dry_run_map.items():
            filename = os.path.basename(src)
            if filename == 'photo1.jpg':
                self.assertTrue(dst.endswith(os.path.join('Images', 'photo1.jpg')))
            elif filename == 'doc1.pdf':
                self.assertTrue(dst.endswith(os.path.join('Documents', 'doc1.pdf')))
            elif filename == 'unknown.xyz':
                self.assertTrue(dst.endswith(os.path.join('Others', 'unknown.xyz')))

        # Execute organization
        successful_moves, errors = engine.organize()
        self.assertEqual(len(successful_moves), 8)
        self.assertEqual(len(errors), 0)
        
        # Verify that original files are gone and new files exist
        for src, dst in dry_run_map.items():
            self.assertFalse(os.path.exists(src))
            self.assertTrue(os.path.exists(dst))
            
        # Verify history is saved
        self.assertTrue(engine.is_undo_available())

    def test_undo_functionality(self):
        engine = OrganizerEngine(self.test_dir)
        engine.scan()
        dry_run_map = engine.get_dry_run()
        
        # Organize first
        engine.organize()
        self.assertTrue(engine.is_undo_available())
        
        # Undo organization
        reverted_moves, errors = engine.undo()
        self.assertEqual(len(reverted_moves), 8)
        self.assertEqual(len(errors), 0)
        
        # Verify files are back in original paths
        for src in dry_run_map.keys():
            self.assertTrue(os.path.exists(src))
            
        # Verify category folders are cleaned up (deleted since they are empty)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'Images')))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'Documents')))
        
        # Verify history is deleted
        self.assertFalse(engine.is_undo_available())

    def test_filename_collision_handling(self):
        # Create a file in Images folder that matches a source file's name
        images_dir = os.path.join(self.test_dir, 'Images')
        os.makedirs(images_dir)
        existing_photo_path = os.path.join(images_dir, 'photo1.jpg')
        with open(existing_photo_path, 'w') as f:
            f.write('already here')
            
        engine = OrganizerEngine(self.test_dir)
        engine.scan()
        
        # Dry run map should rename photo1.jpg to photo1_1.jpg
        dry_run_map = engine.get_dry_run()
        src_photo1 = os.path.join(self.test_dir, 'photo1.jpg')
        expected_dst = os.path.join(images_dir, 'photo1_1.jpg')
        self.assertEqual(dry_run_map[src_photo1], expected_dst)
        
        # Execute and check
        successful_moves, errors = engine.organize()
        self.assertEqual(len(errors), 0)
        self.assertTrue(os.path.exists(expected_dst))
        self.assertTrue(os.path.exists(existing_photo_path))

if __name__ == '__main__':
    unittest.main()
