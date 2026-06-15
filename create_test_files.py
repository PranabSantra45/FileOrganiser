import os

def create_test_files():
    target_dir = os.path.join(os.path.dirname(__file__), 'test_files')
    os.makedirs(target_dir, exist_ok=True)
    
    files = {
        'photo1.jpg': 'dummy image',
        'photo2.png': 'dummy image 2',
        'report.pdf': 'dummy pdf',
        'notes.txt': 'dummy notes',
        'letter.docx': 'dummy word doc',
        'song.mp3': 'dummy audio',
        'backup.zip': 'dummy archive',
        'app_release.apk': 'dummy apk',
        'unknown_format.dat': 'dummy unknown file'
    }
    
    for filename, content in files.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"Test files created successfully in: {target_dir}")

if __name__ == '__main__':
    create_test_files()
