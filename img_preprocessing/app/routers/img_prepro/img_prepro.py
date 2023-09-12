from fastapi import APIRouter
from .model import ImageBase64
from tasks import start_img_preprocessing
from celery.result import AsyncResult

router = APIRouter(
    prefix="/api/v1/img_prep",
    tags=["img_prep"]
)

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    return { "task_status": task_result.status }

@router.get("/img/{task_id}")
async def get_img(task_id: str):
    task_result = AsyncResult(task_id)
    return { "img": task_result.result }

@router.post("/img")
async def create_item(img: ImageBase64):
    task = start_img_preprocessing.delay(img.img_body_base64)
    return { "task_id": task.id }