class LoggerAdapter(logging.LoggerAdapter):
def __init__(self, prefix, logger):
super(LoggerAdapter, self).__init__(logger, {})
self.prefix = prefix

def process(self, msg, kwargs):
return '[%s] %s' % (self.prefix, msg), kwargs

if __name__ == '__main__':

with open('logging.json', 'rt') as f:
config = json.load(f)

logging.config.dictConfig(config)

logger = logging.getLogger("")

logger = LoggerAdapter("SAS", logger)
logger.info("test!!!") 

#결과: 2017-08-07 12:54:55,911 - root - INFO - [SAS] test!!!!


import logging
import threading
import time

def worker(arg):
    while not arg['stop']:
        logging.debug('Hi from myfunc')
        time.sleep(0.5)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    info = {'stop': False}
    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    while True:
        try:
            logging.debug('Hello from main')
            time.sleep(0.75)
        except KeyboardInterrupt:
            info['stop'] = True
            break
    thread.join()

if __name__ == '__main__':
    main()


import Queue
import threading
import traceback
import logging
import sys

class QueueListener(threading.Thread):

def __init__(self, queue, stream_h):
threading.Thread.__init__(self)
self.queue = queue
self.daemon = True
       self.logger = logging.getLogger("main")
self.logger.addHandler(self.handler) 
def run(self):
while True:
try:
record = self.queue.get()
self.logger.callHandlers(record)
except (KeyboardInterrupt, SystemExit):
raise
except EOFError:
break
except:
traceback.print_exc(file=sys.stderr)



class QueueHandler(logging.Handler):

def __init__(self, queue):
logging.Handler.__init__(self)
self.queue = queue

def emit(self, record):
self.queue.put(record)


if __name__ == '__main__': # 리스터 부분
logging_q = Queue.Queue(-1)
stream_h = logging.StreamHandler()
log_queue_reader = QueueListener(logging_q,stream_h)
log_queue_reader.start()
# 핸들러 부분 
handler = QueueHandler(logging_q)
root = logging.getLogger()
root.addHandler(handler)
     # 사용 
root.error("queue handler test!!")

