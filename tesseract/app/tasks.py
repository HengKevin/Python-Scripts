import os
import time
import base64
import pytesseract
from celery import Celery

app = Celery('tasks', broker="redis://redis_fastapi:6379/0")

@app.task(name="start_ocr_processing")
def start_ocr_preprocess(img: str):
    with open("img.jpg", "wb") as f:
        f.write(base64.b64decode(img))
    text = pytesseract.image_to_string("img.jpg")
    time.sleep(5)
    os.remove("img.jpg")
    return text