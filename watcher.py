import time
import os
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
import json
import hashlib

FILES = ' '    //  folder where files will be stored
os.makedirs('uploads',exist_ok=True)

SYNC_FOLDER =  os.path.join(FILES, " ")    // folder where log.json will be stored
os.makedirs(SYNC_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(SYNC_FOLDER,"log.json")    //log file

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

    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
        print("Log file written")
    except Exception as e:
        print("WRITE ERROR:", e)



class SyncHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or event.src_path.startswith(SYNC_FOLDER):
            return 
        append_to_log_file({
            "event" : "created",
            "path": event.src_path
        })
        print(f"Created: {event.src_path}")

    def on_modified(self, event):
        if event.is_directory or event.src_path.startswith(SYNC_FOLDER):
            return
        append_to_log_file({
            "event" : "modified",
            "path": event.src_path
        })
        print(f"Modified: {event.src_path}")
    
    def on_deleted(self, event):
        if event.is_directory or event.src_path.startswith(SYNC_FOLDER):
            return
        append_to_log_file({
            "event" : "deleted",
            "path": event.src_path
        })
        print(f"Deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory or event.src_path.startswith(SYNC_FOLDER):
            return
        append_to_log_file({
            "event" : "moved",
            "path": event.dest_path
        })
        print(f"{event.src_path} Moved to {event.dest_path}")

if __name__ == "__main__":
    print(LOG_FILE)
    print(os.path.abspath(LOG_FILE))

    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, FILES, recursive=True)
    observer.start()

    print("Watching folder for changes")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observation.......")
        observer.stop()

    observer.join()

