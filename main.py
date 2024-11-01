import sys, threading

from train_data_parser import pull_data_to_flow
from services import main as services_main
from display import main as ui_main

if __name__ == "__main__":
    try:
        print("Press CTRL-C to stop.")
        item = 0
        while True:
            t0 = threading.Thread(target=pull_data_to_flow, args=(["A"], ["A03S"]), daemon=True)
            t0.start()

            t1 = threading.Thread(target=services_main, args=(), daemon=True)
            t1.start()

            t2 = threading.Thread(target=ui_main, args=(), daemon=True)
            t2.start()
            
            t0.join
            t1.join()
            t2.join()

    except KeyboardInterrupt:
        sys.exit(0)