import time
import os
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
import json
import hashlib

SYNC_FOLDER = 'uploads'
os.makedirs('uploads',exist_ok=True)
LOG_FILE = os.path.join(SYNC_FOLDER, ".sync", "log.json")

def append_to_log_file(entry):
    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

class SyncHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Created: {event.src_path}")
    
    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified: {event.src_path}")
    
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Deleted: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"{event.src_path} Moved to {event.dest_path}")

if __name__ == "__main__":
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, SYNC_FOLDER, recursive=True)
    observer.start()

    print("Watching folder for changes")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observation.......")
        observer.stop()

    observer.join()

