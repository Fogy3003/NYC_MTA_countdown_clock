import time
import logging
#from matrix_display import init_matrix
from flow import  get_arrivals
from renderer import render

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filename='renderer.log',
    filemode='a'
)

def main():
  
  #matrix = init_matrix()
  time.sleep(2) # wait for first data pull

  images = []
  cached_arrivals = None
  try:
    while True:
      new_arrivals = get_arrivals()
      if cached_arrivals != new_arrivals:
        cached_arrivals = new_arrivals
        image = render(cached_arrivals)
        logging.info("Image rendered and updated.")
        #if images:
        #print("displaying")
        #for image in images:
        #matrix.SetImage(image)
        #time.sleep(1.0/30.0)
      else:
        logging.info("Polling for images.")
        time.sleep(3) # poll until get image
  except Exception as e:
    logging.error(f"Exception in services main loop: {e}", exc_info=True)


if __name__ == "__main__":
    main()
