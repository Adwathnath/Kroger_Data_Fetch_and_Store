import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from access_json import *
from delete_info import *

#to monitor changes in data.json
class FileHandler(FileSystemEventHandler):

    def __init__(self, file_path):
        self.file_path = file_path

    def process_json_file(self, event, event_type):
        print(f"Event detected: {event.event_type} on {event.src_path}")
        if event.src_path == self.file_path:
            print(f"File {event.src_path} was {event.event_type}")
            data = None
            try:
                with open(event.src_path) as f:
                    data = json.load(f)
        
            except Exception as e:
                print(f"Failed to read the JSON file: {e}")
            #call to transform json data
            access(data, event_type)


    def on_created(self, event):
        print(f"File Created : {event.src_path}")
        event_type ="created"
        time.sleep(1)
        self.process_json_file(event, event_type)

    def on_modified(self, event):
        print(f"File modified : {event.src_path}")
        event_type ="modified"
        self.process_json_file(event, event_type)
    
    def on_deleted(self, event):
        del_info()
        print(f"File deleted: {event.src_path}")
        

        

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, 'data.json')
    directory_to_watch = os.path.dirname(path)

    print(f"Monitoring file: {path}")
    print(f"Monitoring directory: {directory_to_watch}")

    #setting up  observer
    event_handler = FileHandler(path)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()

    print(f"Monitoring changes in {path}...")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()