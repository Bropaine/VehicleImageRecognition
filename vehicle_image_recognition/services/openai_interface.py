import base64
import json
import os
from typing import List

import openai
import requests
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.responses import JSONResponse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


async def identify_image_content(files: List[UploadFile]):
    base64_images = []

    for index, file in enumerate(files):
        file_bytes = await file.read()
        base64_image = encode_image(file_bytes)
        base64_images.append((f"image_{str(index).zfill(2)}", base64_image))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    content = [
        {
            "type": "text",
            "text": (
                "You are an expert at identifying anomalies in a group of images, "
                "specifically in recognizing when an image is something other than a vehicle. "
                "Your primary task is to identify and classify images that contain a vehicle delivery receipt or a "
                "Bill of Lading (BOL). BOL will sometimes have outline images of vehicle orientations or will say "
                "BOL. Vehicle delivery receipts must have words like Received or Delivered on it and look outstanding "
                "from typical"
                "receipts such as maintenance or per diem receipts, which belong in the other category. You are also "
                "responsible for categorizing images that"
                "show damage to a"
                "vehicle, look for noticeable damage. You will also be responsible for identifying and categorizing "
                "images of vehicle gauges like odometer readings or fuel gauges."
                "Images that dont show any of the above listed items should be categorized as other"
                "The images will be sent in order, and I need a structured JSON output with a dictionary, formatted "
                "as follows:\n\n"
                "{\n  \"image_01\": \"vehicle\",\n  \"image_02\": \"delivery_receipt\",\n  \"image_03\": \"bol\","
                "\n  \"image_04\": \"other\"\n, \n  \"image_05\": \"damaged_vehicle\"\n, \n  \"image_06\": "
                "\"gauge_reading\"\n}\n\n"
                "Instructions:\n"
                "1. Analyze each image.\n"
                "2. Determine which images contain a BOL or a delivery receipt.\n"
                "3. Pay close attention to paperwork; some items that look like paper may be trash or useless.\n"
                "4. Be concise and methodical when classifying the images. Pay close attention to the paperwork and "
                "decipher what is a BOL or delivery receipt\n"
                "5. Provide the output in a structured JSON dictionary, maintaining the input order of the images.\n\n"
                "The output must be valid JSON structure and only valid JSON structure. "
                "The JSON structure string must only use double quotes "
                "Please ensure the output is clear, accurate, and follows the example format. ::: No Yapping ::: "
                "I only want the data structure in your response."
            )
        }
    ]

    for name, base64_image in base64_images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    payload = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Print response for debugging
    print("API Response Status:", response.status_code)
    response_text = response.content.decode('utf-8')
    print("API Response Content:", response_text)

    # Check if response is valid JSON
    try:
        response_content = json.loads(response_text)
        content_message = response_content['choices'][0]['message']['content'].strip()

        # Debug print to ensure the content is as expected
        print("Content Message:", content_message)

        # Convert the content message to a dictionary
        result_dict = json.loads(content_message)
        print("Result Dict:", result_dict)
        return JSONResponse(content=result_dict)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Response Text:", response_text)
        return JSONResponse(content={"error": "Invalid response from API"}, status_code=500)
    except Exception as e:
        print("General Error:", e)
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)