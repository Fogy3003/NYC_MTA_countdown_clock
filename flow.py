import threading
import logging


lock = threading.Lock()
arrivals = []

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filename='renderer.log',
    filemode='a'
)

def set_arrivals(new_arrivals):
  global arrivals
  try:
    lock.acquire()
    arrivals = new_arrivals
    logging.info(f"Arrivals set: {new_arrivals}")
  except Exception as e:
    logging.error(f"Exception in set_arrivals: {e}", exc_info=True)
  finally:
    lock.release()

def get_arrivals():
  global arrivals
  try:
    lock.acquire()
    ret_val = arrivals
    logging.info(f"Arrivals retrieved: {ret_val}")
    return ret_val
  except Exception as e:
    logging.error(f"Exception in get_arrivals: {e}", exc_info=True)
    return []
  finally:
    lock.release()