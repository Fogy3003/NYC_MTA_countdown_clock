from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import constants
import pytz
import logging
#import matplotlib.pyplot as plt
FONT = ImageFont.truetype("./fonts/retro.ttf", size=10.5)
FONT = ImageFont.load("fonts/mta.pil")
ny_timezone = pytz.timezone("America/New_York")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filename='renderer.log',
    filemode='a'
)

def text_width(text: str) -> int:
  width, _ = FONT.getsize(text)
  return width


def load_needed_bullets(line_id):   
    bullets = {}
    for id in set(line_id):
        image = Image.open(constants.train_image_path[id])
        r,g,b,a = image.split()
        image = Image.merge('RGB', (r,b,g))
        bullets[id] = image
        return bullets

def make_row(train, height=16, length=64*2):
    logging.debug(f"Entering make_row with train={train}")
    if train is None:
        row = Image.new('RGB', (length, height), color="black")
        draw = ImageDraw.Draw(row)
        logging.warning("Received None for train in make_row.")
        return [row]*30

    train_image = load_needed_bullets(train[0])[train[0]]
    # Create a blank row image
    row = Image.new('RGB', (length, height), color="black")
    draw = ImageDraw.Draw(row)

    # Load the 15x14 pixel train image
    row.paste(train_image.convert("RGB"), (0, 1,15,15))  # Place it at the start of the row

    # Calculate minutes until departure
    now = datetime.now(ny_timezone)
    departure_time = train[2].astimezone(ny_timezone)
    logging.debug(f"Departure time: {departure_time}, Now: {now}")
    time_diff = round((departure_time - now).total_seconds() //60)
    if time_diff < 0:
        logging.warning(f"Negative time_diff detected: {time_diff} for train {train}")
    time_text = f"{time_diff}m"
    time_text_bbox = draw.textbbox((0, 0), time_text, font=FONT)  # Get bounding box for time text
    time_text_width = time_text_bbox[2] - time_text_bbox[0]  # Calculate width of time text
    time_start_x = length - time_text_width
    # Add the departure time text to the end of the row
   
    draw.text((time_start_x, 3), time_text, font=FONT, fill="white"
)

    # Handle scrolling text if text exceeds available space
    text = train[1]
    text_start_x = train_image.width + 1  # Starting x position for the main text
    available_width = time_start_x - text_start_x
    text_bbox = draw.textbbox((0, 0), text, font=FONT)
    text_width = text_bbox[2] - text_bbox[0]
    if text_width <= available_width:
        # If text fits, just draw it
        draw.text((text_start_x, 3), text, font=FONT, fill="white")
    else:
        # Create a scrolling effect
        scroll_row_images = []
        scroll_length = text_width + available_width + 10  # Total scroll length including gap
        for offset in range(scroll_length):
            scroll_frame = row.copy()
            scroll_draw = ImageDraw.Draw(scroll_frame)
            scroll_draw.text((text_start_x - offset, 3), text, font=FONT, fill="white")
            scroll_frame.paste(train_image, (0, 1))
            scroll_row_images.append(scroll_frame)
            scroll_draw.text((time_start_x, 3), time_text, font=FONT, fill="white")
        logging.info(f"Scrolling text for train {train[0]}: '{text}'")
        return scroll_row_images

    # Return row image if no scrolling is needed
    logging.debug(f"Exiting make_row for train {train[0]}")
    return [row]*30

def combine_rows(row1, row2):
    # Get the dimensions of the rows
    width = max(row1.width, row2.width)  # Assume rows are the same width
    height = row1.height + row2.height   # Total height by stacking rows vertically

    # Create a blank image with the combined dimensions
    combined_image = Image.new("RGB", (width, height), color="black")

    # Paste the first row at the top
    combined_image.paste(row1, (0, 0))

    # Paste the second row below the first
    combined_image.paste(row2, (0, row1.height))

    return combined_image

def render(arrivals):
    logging.info(f"Rendering arrivals: {arrivals}")
    # route id, last stop, departure time
    ret_rows = []
    for train in arrivals:
        row = make_row(train)
        ret_rows.append(row)
    combined_images = []
    for i in range(30):
        combined_images.append(combine_rows(ret_rows[0][i], ret_rows[1][i]))
    logging.info("Render complete.")
    return combined_images

            


    

class Render():
    def __init__(self, line_id, rows=32, cols=128):
        self.rows = rows
        self.cols = cols
        self.bullets = load_needed_bullets(line_id)


        
    def load_and_recolor_image(self, image_path):
        # Load and resize image
        image = Image.open(image_path)
        r,g,b,a = image.split()
        image = Image.merge('RGB', (r,b,g))
        return image
    
    def combine_text_image(self, image, text, font_size=10.5):
        # Create a blank canvas to hold the image and text
        canvas = Image.new("RGB", (self.cols, self.rows//2))  # Adjust to half of matrix width for one item
        # Paste the image on the upper part of the canvas
        canvas.paste(image, (0, 1))
        # Draw the text next to the image
        draw = ImageDraw.Draw(canvas)
        #font = ImageFont.load("./mta.pil")
        font = ImageFont.truetype("./rainyhearts.ttf", font_size)
        # Define the position of the text (below the image)
        text_x = image.width + 2
        text_y = 3
        draw.text((text_x, text_y), text,font=font, fill=(255, 255, 255))

        return canvas

    def build_display(self, combined1, combined2):
        combined_image = Image.new("RGB", (self.cols, self.rows))
        # Paste the two combined images side-by-side
        combined_image.paste(combined1, (0, 0))
        combined_image.paste(combined2, (0, combined1.height))

        return combined_image
