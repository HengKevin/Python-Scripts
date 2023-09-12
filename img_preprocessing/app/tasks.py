import os
import base64
import io
import cv2
import numpy as np
from celery import Celery
from PIL import Image

app = Celery('tasks', broker="redis://redis_fastapi:6379/0")

@app.task(name="start_img_preprocessing")
def start_img_preprocessing(img_str: str):
    imgData = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(imgData))
    cv2_img = np.array(img)

    # Convert RGB to BGR
    gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2GRAY)

    # Apply thresholding
    bin_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    _, im_arr = cv2.imencode('.jpg', bin_img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    jpg_as_str = base64.b64encode(im_bytes)

    return jpg_as_str.decode()