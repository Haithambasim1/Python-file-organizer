import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# الإعدادات: غير المسار للمجلد اللي بدك تراقبه
WATCH_DIRECTORY = os.path.expanduser("~/Downloads")

# تصنيف الامتدادات
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
    'Media': ['.mp4', '.mp3', '.mov', '.wav', '.mkv'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts_and_Code': ['.py', '.js', '.html', '.css', '.cpp', '.json', '.sql']
}

class MoveHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def process(self, file_path):
        filename = os.path.basename(file_path)
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        for folder, extensions in FILE_TYPES.items():
            if extension in extensions:
                dest_path = os.path.join(WATCH_DIRECTORY, folder)
                os.makedirs(dest_path, exist_ok=True)
                
                # معالجة إذا الملف موجود مسبقاً بنفس الاسم
                final_destination = os.path.join(dest_path, filename)
                if os.path.exists(final_destination):
                    name, ext = os.path.splitext(filename)
                    final_destination = os.path.join(dest_path, f"{name}_{int(time.time())}{ext}")

                try:
                    time.sleep(1) # تأمين استقرار الملف قبل النقل
                    shutil.move(file_path, final_destination)
                    print(f"[+] Moved: {filename} to {folder}")
                except Exception as e:
                    print(f"[!] Error moving {filename}: {e}")

if __name__ == "__main__":
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    
    print(f"🚀 Organizer started! Monitoring: {WATCH_DIRECTORY}")
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping script...")
    observer.join()
                
