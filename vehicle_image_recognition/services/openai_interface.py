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


async def identify_image_content(files: List[UploadFile], prompt: str):
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
            "text": prompt
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