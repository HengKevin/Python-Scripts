from fastapi import APIRouter
from .model import ImageBase64
from tasks import start_ocr_preprocess
from celery.result import AsyncResult

router = APIRouter(
    prefix="/api/v1/tesseract",
    tags=["tesseract"],
)

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task = AsyncResult(task_id)
    return {"task_status": task.state}

@router.get("/text/{task_id}")
async def get_text(task_id: str):
    task = AsyncResult(task_id)
    return { "text_tesseract": task.result }

@router.post("/img")
async def create_item(img: ImageBase64):
    task = start_ocr_preprocess.delay(img.image_base64)
    return { "task_id": task.id }