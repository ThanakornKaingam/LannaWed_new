from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io

from app.services.predict_service import predict_image

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    result = predict_image(image)
    return result
