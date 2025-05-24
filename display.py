import time, datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flow import get_arrivals
from renderer import render
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filename='renderer.log',
    filemode='a'
)

def main():
  # Configuration for the matrix
  options = RGBMatrixOptions()
  options.brightness = 30
  options.rows = 32
  options.cols = 64
  options.chain_length = 2
  options.parallel = 1
  # Should be set in DEFAULT_HARDWARE but just in case
  options.hardware_mapping = "regular"

  matrix = RGBMatrix(options = options)
  time.sleep(2) # wait for first data pull

  images = []
  cached_arrivals = None
  cached_time = datetime.datetime.now().minute
  try:
    while True:
      new_arrivals = get_arrivals()
      now_minute = datetime.datetime.now().minute
      if cached_arrivals != new_arrivals or cached_time != now_minute:
        cached_arrivals = new_arrivals
        cached_time = now_minute
        images = render(cached_arrivals)
        logging.info("Images rendered and updated.")
      if images:
        logging.info("Displaying images on matrix.")
        for image in images:
          matrix.SetImage(image)
          time.sleep(1.0/24.0)
      else:
        logging.info("Polling for images.")
        time.sleep(10) # poll until get image
  except Exception as e:
    logging.error(f"Exception in display main loop: {e}", exc_info=True)
