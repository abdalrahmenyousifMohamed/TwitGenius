import os
import io
import base64
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Function to list all image files in a directory
def list_image_files(directory):
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".png"):  # Adjust the file extension as needed
            image_files.append(filename)
    return image_files

# Function to load the next image in the sequence
def load_next_image(image_files):
    # Increment the image counter
    if "image_counter" not in load_next_image.__dict__:
        load_next_image.image_counter = 0
    else:
        load_next_image.image_counter = (load_next_image.image_counter + 1) % len(image_files)

    # Define the directory where images are stored
    image_directory = "images"  # Update with the path to your image directory
    
    # Determine the image file path
    image_filename = image_files[load_next_image.image_counter]
    image_path = os.path.join(image_directory, image_filename)

    # Check if the image exists
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            img_data = image_file.read()
            img_base64 = base64.b64encode(img_data).decode()
            return f"data:image/png;base64,{img_base64}"
    else:
        return None

@app.get('/')
async def get_img(request: Request, background_tasks: BackgroundTasks):
    # List all image files in the directory
    image_directory = "images"  # Update with the path to your image directory
    image_files = list_image_files(image_directory)

    if not image_files:
        image_url = None
    else:
        # Load the next image in the sequence
        image_url = load_next_image(image_files)

    # Render the HTML template and pass the image URL
    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url})
