import datetime
import os
import threading
import time
from multiprocessing import Queue
from os import remove
from os import rename
from os import stat
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from check import check_hash_is_written

from multiprocessing import Pool
FILE_PROCESSING = "/samba/enclave/monitoring/"
pending_queue = []

class FileLoaderWatchdog(FileSystemEventHandler):
    ''' Watches a directory for creation of file
    '''
    def on_moved(self, event):
        # self.process(event)
        now = datetime.datetime.now()
        #print(f"hey for {event.src_path}")
        print ("\n{0} -- Event type {1}: {2} renamed to {3} ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.event_type, event.src_path, event.dest_path))
        pending_queue.append(event.dest_path)


if __name__ == '__main__':
    event_handler = FileLoaderWatchdog()
    observer = Observer()
    observer.schedule(event_handler, path=FILE_PROCESSING, recursive=True)
    observer.start()
    try:
        while True:
            while len(pending_queue) > 0:
                file_path = pending_queue.pop(0)
                splitted_file_path = file_path.split("/")
                action = splitted_file_path[4]
                # Check if the 5th folder is hash_generation
                if action == "hash_generation":
                    # Read the hash value from the shared folder
                    with open(file_path, "r") as f:
                        hash_values = f.read()

                    # Check if the file content is empty
                    if hash_values == "":
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Empty file detected: " + str(file_path))
                    else:
                        # Write the hash value to another folder
                        with open("hash/hashes.txt", "a+") as t:
                            t.write(hash_values + "\n")
                            # t.write(" \n") # Test check on missing hash values

                        if check_hash_is_written(file_path):
                            print("[DIRWATCH] Removing " + str(file_path))
                            # Remove the file in the shared folder
                            remove(file_path)
                # Check if the 5th folder is request_hash
                elif action == "request_hash":
                    print("[DIRWATCH] splitted ", splitted_file_path)
                    with open(file_path, "r") as read_dummy_file:
                        retrieve_hash_file_name = read_dummy_file.read()
                    
                    print("[DIRWATCH] The file name to retrieve hash: ", retrieve_hash_file_name)
                    # Remove the file away
                    print("[DIRWATCH] Removing the filename file ...")
                    remove(file_path)
                    # Open and read the file storing all hashes
                    with open("hash/hashes.txt", "r") as read_hashes:
                        # Check if the file_name obtained is inside the hash file
                        line = next((l for l in read_hashes if retrieve_hash_file_name in l), None)
                        if line == None:
                            print("[DIRWATCH] Unable to find the hash value for file " + retrieve_hash_file_name)
                        else:
                            print("Hash for " + retrieve_hash_file_name + ": " + str(line[:64]))
                            print("Writing to file at: " + "/samba/enclave/return_hash/" + retrieve_hash_file_name.split(".")[0] + "_hash.txt")
                            with open("/samba/enclave/return_hash/" + retrieve_hash_file_name.split(".")[0] + "_hash.txt.tmp", "w+") as wf:
                                # wf.write(line[:64])
                                wf.write(line)
                            rename("/samba/enclave/return_hash/" + retrieve_hash_file_name.split(".")[0] + "_hash.txt.tmp", "/samba/enclave/return_hash/" + retrieve_hash_file_name.split(".")[0] + "_hash.txt")
                else:
                    print("[DIRWATCH] Wrong action!")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()