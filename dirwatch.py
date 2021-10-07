import configparser
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
from watchdog.observers.api import EventQueue
from watchdog.observers.polling import PollingObserver as Observer
from os import stat
from os import remove
from os.path import join
from os.path import basename
from os.path import normpath
from os.path import dirname
from pathlib import Path

# Prepare file paths
# path = Path(__file__).resolve().parent
# config_path = join(path, "client_path_config.ini")
# config = configparser.ConfigParser()
# config.read(config_path)
# file_processing = join(path, config.get('FileProcessing', 'client_file_dir'))
file_processing = "/samba/enclave/"

pending_queue = []

class OnCreateRunner(FileSystemEventHandler):
    def on_created(self, event):
        pending_queue.append(event.src_path)


if __name__ == "__main__":
    event_handler = OnCreateRunner()
    observer = Observer()
    observer.schedule(event_handler, file_processing, recursive=True)

    observer.start()

    print("[DIRWATCH] Watching ", file_processing)

    try:
        while True:
            while len(pending_queue) > 0:
                print("\n[DIRWATCH] Pending queue: ", pending_queue)

                file_path = pending_queue.pop()
                print("[DIRWATCH] File path: ", file_path)

                if stat(file_path).st_size == 0:
                    print("[DIRWATCH] Empty file detected!")
                else:
                    splitted_file_path = file_path.split("/")
                    print(splitted_file_path)

                    if len(splitted_file_path) < 0:
                        print("opps")
                    else:
                        action = splitted_file_path[3]
                        received_file_name = splitted_file_path[5]
                        # Check if the 3rd folder is hash_generation
                        if action == "hash_generation":
                            with open(file_path, "r") as f:
                                hash_values = f.read()
                            with open("/hash/hashes.txt", "a+") as t:
                                t.write(hash_values + "\n")

                            print("Removing " + str(file_path))
                            remove(file_path)
                        # Check if the 3rd folder is verify_hash
                        elif action == "verify_hash":
                            print("Verify hash...")
                            if received_file_name == "dummy.txt":
                                print("i need to retrieve hash file")
                                with open(file_path, "r") as read_dummy_file:
                                    retrieve_hash_file_name = read_dummy_file.read()
                                print("The file name to retrieve hash: ", retrieve_hash_file_name)
                                remove(file_path)
                                with open("hash/hashes.txt", "r") as read_hashes:
                                    next(read_hashes)
                                    for contents in read_hashes:
                                        print("[DIRWATCH] All contents in file: ", contents)
                                        hashes, file_name = contents.strip().split("|",1)
                                        if retrieve_hash_file_name == file_name:
                                            print("[DIRWATCH] File name found in: ", contents)
                                            with open(file_processing + "/verify_hash/return_hash/hash.txt", "w+") as wf:
                                                wf.write(hashes)
                            elif received_file_name == "hashes.txt":
                                print("do nothing")
                                pass
                            else:
                                print("lala")


    except KeyboardInterrupt:
        observer.stop()

    observer.join()