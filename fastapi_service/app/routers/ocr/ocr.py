from fastapi import APIRouter
from .model import ImageBase64
from celery.result import AsyncResult
from tasks import create_task

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    return { "task_status": task_result.status }

@router.get("/text/{task_id}")
async def get_text(task_id: str):
    task_result = AsyncResult(task_id)
    return { "text_ocr": task_result.result }

@router.post("/img")
async def create_item(image: ImageBase64):
    task = create_task.delay(image.img_body_base64)
    return { "task_id": task.id }