from typing import List
from fastapi import APIRouter, File, UploadFile, FastAPI
from vehicle_image_recognition.services.openai_interface import identify_image_content
from vehicle_image_recognition.prompts import IDENTIFY_IMAGE_CONTENT_PROMPT, IDENTIFY_VEHICLE_ORIENTATION_PROMPT

router = APIRouter()

app = FastAPI()


@router.post("/identify_image_content/")
async def upload_images(files: List[UploadFile] = File(...)):
    prompt = IDENTIFY_IMAGE_CONTENT_PROMPT

    response = await identify_image_content(files, prompt)

    print("identify image response: " + str(response.status_code))

    return response


@router.post("/identify_vehicle_orientation/")
async def upload_images(files: List[UploadFile] = File(...)):
    prompt = IDENTIFY_VEHICLE_ORIENTATION_PROMPT

    response = await identify_image_content(files, prompt)

    print("identify image response: " + str(response.status_code))

    return response
