import os
import time
import requests
import json
from routers.ocr.model import PreProsImgResponse
from celery import Celery

app = Celery('tasks', broker="redis://redis_fastapi:6379/0")

def check_until_done(url):
    attempts = 0
    while True:
        response = requests.get(url)
        if response.status_code == 200 and response.json()["task_status"] == "PENDING" and attempts < 60:
            time.sleep(1)
            attempts += 1
        
        elif response.status_code == 200 and response.json()['task_status'] == "SUCCESS":
            return True
        else:
            return False

def convert_img_to_bin(img):
    response = requests.post(url = "http://img_prepro:8000/api/v1/img_prep/img", json={'img_body_base64': img})
    task = response.json()
    if check_until_done("http://img_prepro:8000/api/v1/img_prep/status" + f"/{task['task_id']}"):
        url = "http://img_prepro:8000/api/v1/img_prep/img" + f"/{task['task_id']}"
        response = requests.get(url)
        return response.json()['img']
    raise Exception("Error while converting image to binary")

def get_orc_text(img):
    response = requests.post(url = "http://tesseract:8000/api/v1/tesseract/img", json={'img_body_base64': img})
    task = response.json()
    if check_until_done("http://tesseract:8000/api/v1/tesseract/status" + f"/{task['task_id']}"):
        url = "http://tesseract:8000/api/v1/tesseract/text" + f"/{task['task_id']}"
        response = requests.get(url)
        return response.json()['text']
    raise Exception("Error while converting image to binary")


@app.task(name="create_task")
def create_task(img: str):
    try:
        bin_img = convert_img_to_bin(img)
        text = get_orc_text(bin_img)
        return text
    except Exception as e:
        print(e)
        return {"error": str(e)}
