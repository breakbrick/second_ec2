import os
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
import multiprocessing as mp
from multiprocessing import Process
from multiprocessing import Queue
import threading

from multiprocessing import Pool
PROCESSES = mp.cpu_count() - 1
NUMBER_OF_TASKS = 10
FILE_PROCESSING = "/samba/enclave/"
class FileLoaderWatchdog(FileSystemEventHandler):
    ''' Watches a nominated directory and when a * type  file is
        moved

    '''

    def __init__(self, queue):
       #PatternMatchingEventHandler.__init__(self, patterns=patterns)
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
        now = datetime.datetime.utcnow()
        #print(f"hey for {event.src_path}")
        print ("{0} -- event {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))


def print_func(event):
    time.sleep(5)
    now = datetime.datetime.utcnow()
    print ("{0} -- Pulling {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))

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
            pool = Pool(processes=1)
            pool.apply_async(print_func, (event,))
            print("[process] ", event.src_path)
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
    patt = ["*"]
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