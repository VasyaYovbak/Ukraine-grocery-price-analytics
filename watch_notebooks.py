import sys
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse

class NotebookConverterHandler(FileSystemEventHandler):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def on_modified(self, event):
        if event.src_path.endswith(".ipynb"):
            print(f"Detected change in {event.src_path}. Converting to .py...")
            self.convert_to_py(event.src_path)

    def convert_to_py(self, ipynb_path):
        # Створюємо шлях для збереження .py файлу у вказаній директорії
        output_file = os.path.join(self.output_dir, os.path.splitext(os.path.basename(ipynb_path))[0])
        
        # Використовуємо nbconvert для перетворення .ipynb в .py з вказанням шляху для збереження
        subprocess.run(["jupyter", "nbconvert", "--to", "script", "--output", output_file, ipynb_path])
        print(f"Conversion completed: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Watch and convert .ipynb to .py")
    parser.add_argument("notebook", help="Path to the .ipynb file to watch")
    parser.add_argument("output_dir", help="Directory where the .py file should be saved")

    args = parser.parse_args()

    # Переведення шляху до абсолютного
    notebook_path = os.path.abspath(args.notebook)
    output_dir = os.path.abspath(args.output_dir)

    # Перевірка, чи існує вказаний файл та директорія
    if not os.path.exists(notebook_path):
        print(f"Error: The file {notebook_path} does not exist.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: The directory {output_dir} does not exist.")
        sys.exit(1)

    event_handler = NotebookConverterHandler(output_dir)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(notebook_path), recursive=False)

    print(f"Watching for changes in {notebook_path}...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
