import time
#from matrix_display import init_matrix
from flow import  get_arrivals
from renderer import render

def main():
  
  #matrix = init_matrix()
  time.sleep(2) # wait for first data pull

  images = []
  cached_arrivals = None
  while True:
    new_arrivals = get_arrivals()
    if cached_arrivals != new_arrivals:
      cached_arrivals = new_arrivals
      image = render(cached_arrivals)
      #if images:
      #print("displaying")
      #for image in images:
      #matrix.SetImage(image)
      #time.sleep(1.0/30.0)
    else:
      print("polling")
      time.sleep(3) # poll until get image


if __name__ == "__main__":
    main()
