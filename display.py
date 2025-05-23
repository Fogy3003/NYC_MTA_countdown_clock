import time, datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flow import get_arrivals
from renderer import render

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
  while True:
    new_arrivals = get_arrivals()
    now_minute = datetime.datetime.now().minute
    if cached_arrivals != new_arrivals or cached_time != now_minute:
      cached_arrivals = new_arrivals
      cached_time = now_minute
      images = render(cached_arrivals)
    if images:
      print("displaying")
      for image in images:
        matrix.SetImage(image)
        time.sleep(1.0/24.0)
    else:
      print("polling")
      time.sleep(10) # poll until get image
