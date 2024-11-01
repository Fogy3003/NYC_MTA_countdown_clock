from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import constants
import matplotlib.pyplot as plt

FONT = ImageFont.truetype("./fonts/rainyhearts.ttf", size=10)


def text_width(text: str) -> int:
  width, _ = FONT.getsize(text)
  return width


def load_needed_bullets(line_id):   
    bullets = {}
    for id in set(line_id):
        bullets[id] = Image.open(constants.train_image_path[id])
        return bullets

def make_row(train, height=16, length=64):
    font = ImageFont.truetype("./fonts/rainyhearts.ttf", 10.5)
    train_image = load_needed_bullets(train[0])[train[0]]
    # Create a blank row image
    row = Image.new('RGB', (length, height), color="black")
    draw = ImageDraw.Draw(row)

    # Load the 15x14 pixel train image
    row.paste(train_image.convert("RGB"), (0, 1,15,15))  # Place it at the start of the row

    # Calculate minutes until departure
    now = datetime.now()
    departure_time = train[2]
    time_diff = int((departure_time - now).total_seconds() / 60)
    time_text = f"{time_diff}m"
    time_text_bbox = draw.textbbox((0, 0), time_text, font=font)  # Get bounding box for time text
    time_text_width = time_text_bbox[2] - time_text_bbox[0]  # Calculate width of time text
    time_start_x = length - time_text_width
    # Add the departure time text to the end of the row
   
    draw.text((time_start_x, 1), time_text, font=font, fill="white"
)

    # Handle scrolling text if text exceeds available space
    text = train[1]
    text_start_x = train_image.width + 1  # Starting x position for the main text
    available_width = time_start_x - text_start_x
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    if text_width <= available_width:
        # If text fits, just draw it
        draw.text((text_start_x, 1), text, font=font, fill="white")
    else:
        # Create a scrolling effect
        scroll_row_images = []
        scroll_length = text_width + available_width + 10  # Total scroll length including gap
        for offset in range(scroll_length):
            scroll_frame = row.copy()
            scroll_draw = ImageDraw.Draw(scroll_frame)
            scroll_draw.text((text_start_x - offset, 1), text, font=font, fill="white")
            scroll_frame.paste(train_image, (0, 1))
            scroll_row_images.append(scroll_frame)
            scroll_draw.text((time_start_x, 1), time_text, font=font, fill="white")
        return scroll_row_images

    # Return row image if no scrolling is needed
    return [row]


def render(arrivals):
    # route id, last stop, departure time
    for train in arrivals:
        row = make_row(train)
        for i, frame in enumerate(row):
            frame.save(f"train_row_frame_{i}.png")
        break


    

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