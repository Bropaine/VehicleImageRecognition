from typing import List
from fastapi import APIRouter, File, UploadFile, FastAPI
from vehicle_image_recognition.services.openai_interface import identify_image_content

router = APIRouter()

app = FastAPI()


@router.post("/identify_image_content/")
async def upload_images(files: List[UploadFile] = File(...)):
    response = await identify_image_content(files)

    print("identify image response: " + str(response.status_code))

    return response
