from pydantic import BaseModel

class ImageBase64(BaseModel):
    image_base64: str