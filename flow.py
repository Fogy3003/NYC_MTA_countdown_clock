import threading


lock = threading.Lock()
arrivals = []

def set_arrivals(new_arrivals):
  global arrivals
  lock.acquire()
  arrivals = new_arrivals
  lock.release()

def get_arrivals():
  global arrivals
  lock.acquire()
  ret_val = arrivals
  lock.release()
  return ret_val