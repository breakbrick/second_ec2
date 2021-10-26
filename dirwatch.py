import datetime
import os
import threading
import time
from multiprocessing import Queue
from os import remove
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from multiprocessing import Pool
FILE_PROCESSING = "/samba/enclave/monitoring/"

class FileLoaderWatchdog(FileSystemEventHandler):
    ''' Watches a directory for creation of file
    '''

    def __init__(self, queue):
       self.queue = queue

    def process(self, event):
        '''
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        '''
        self.queue.put(event)

    def on_created(self, event):
        self.process(event)
        now = datetime.datetime.now()
        #print(f"hey for {event.src_path}")
        print ("\n{0} -- event {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))


def process_func(event):
    # time.sleep(3)
    now = datetime.datetime.now()
    print ("{0} -- Pulling {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
    splitted_file_path = event.src_path.split("/")
    action = splitted_file_path[4]
    # Check if the 5th folder is hash_generation
    if action == "hash_generation":
        # Read the hash value from the shared folder
        with open(event.src_path, "r") as f:
            hash_values = f.read()
        # Write the hash value to another folder
        with open("hash/hashes.txt", "a+") as t:
            t.write(hash_values + "\n")

        print("[DIRWATCH] Removing " + str(event.src_path))
        # Remove the file in the shared folder
        remove(event.src_path)
    # Check if the 5th folder is request_hash
    elif action == "request_hash":
        print("[DIRWATCH] splitted ", splitted_file_path)
        with open(event.src_path, "r") as read_dummy_file:
            retrieve_hash_file_name = read_dummy_file.read().rstrip()
        print("[DIRWATCH] The file name to retrieve hash: ", retrieve_hash_file_name)
        # Remove the file away
        print("[DIRWATCH] Removing the filename file ...")
        remove(event.src_path)
        # Open and read the file storing all hashes
        with open("hash/hashes.txt", "r") as read_hashes:
            # Check if the file_name obtained is inside the hash file
            for contents in read_hashes:
                # print("[DIRWATCH] All contents in file: ", contents)
                hashes, file_name = contents.strip().split("|",1)
                if retrieve_hash_file_name == file_name:
                    print("[DIRWATCH] Hash of the file found: ", hashes)
                    print("[DIRWATCH] Writing the hash found to file ...")
                    with open("/samba/enclave/return_hash/" + retrieve_hash_file_name.split(".")[0] + "_hash.txt", "w+") as wf:
                        wf.write(hashes)
                    break
                else:
                    print("[DIRWATCH] Unable to find the hash value for file " + retrieve_hash_file_name)
    else:
        print("[DIRWATCH] Wrong action!")

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def process_load_queue(q):
    '''This is the worker thread function. It is run as a daemon
       threads that only exit when the main thread ends.

       Args
       ==========
         q:  Queue() object
    '''
    while True:
        if not q.empty():
            #mp.set_start_method('spawn')
            event = q.get()
            process_func(event)
            # pool = Pool(processes=1)
            # pool.apply_async(process_func, (event,))
            ##p = Pool(5)
            #p.map(print_func,(event,))
            #print_func(event)
            #info('main line')
            #procs = []
            #proc = Process(target=print_func, args=(event,))
            #procs.append(proc)
            #proc.start()
            #for proc in procs:
             #   proc.join()
            #print ("{0} -- Pulling {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
            #time.sleep(5)
           # now2 = datetime.datetime.utcnow()
            #print ("{0} -- Replying {1} off the queue ...".format(now2.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
        else:
            time.sleep(1)



if __name__ == '__main__':

    # create queue
    watchdog_queue = Queue()


    # Set up a worker thread to process database load


    # setup watchdog to monitor directory for trigger files
    #args = sys.argv[1:]
    # path_watch = "D:\watcher"
    event_handler = FileLoaderWatchdog(watchdog_queue)
    observer = Observer()
    observer.schedule(event_handler, path=FILE_PROCESSING, recursive=True)
    observer.start()
    #pool=Pool(processes = 1)
    #pool.apply_async(process_load_queue, (watchdog_queue,))
    worker = threading.Thread(target=process_load_queue, args=(watchdog_queue,))

    worker.setDaemon(True)
    worker.start()
    #p = Pool(2)
    #p.map(observer,watchdog_queue)


    #asyncio.run(main())
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()