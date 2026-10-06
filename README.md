# Vehicle Image Recognition

**A FastAPI prototype that turns batches of vehicle-delivery images into structured AI classifications.**

[Getting started](docs/SETUP.md) · [API reference](docs/API.md) · [Architecture](docs/ARCHITECTURE.md)

| Stack | Project scope |
| --- | --- |
| Python · FastAPI · Uvicorn · OpenAI vision · HTML/CSS/JavaScript | Historical AI integration prototype |

## Overview

Vehicle-delivery workflows contain more than photographs of cars: delivery receipts, bills of lading, damage photos, and gauge readings can arrive in the same batch. This application provides two classification workflows behind a small REST API and a browser interface.

**Content classification** asks the model to distinguish vehicles, delivery receipts, bills of lading, damaged vehicles, gauge readings, and other images. **Orientation classification** asks for front, back, left-side, right-side, or other views.

Built by **Jared Hall**, this repository demonstrates multimodal AI integration, multipart API design, prompt-driven structured output, and a simple frontend-to-backend workflow.

## How it works

```mermaid
flowchart LR
    UI[Browser or API client] --> API[FastAPI multipart endpoint]
    API --> Encode[Base64 image payloads]
    Encode --> Model[OpenAI Chat Completions]
    Model --> Parse[Parse model JSON]
    Parse --> UI
```

- Upload multiple images in one request.
- Choose content or orientation classification.
- Build a multimodal request using a task-specific prompt and inline images.
- Return the model's JSON dictionary to the caller.
- Preview images and display classification labels in the browser.

## Run locally

Create and activate a Python virtual environment in the repository root, then:

```sh
python -m pip install -r requirements.txt
python -m pip install python-multipart
```

Set `OPENAI_API_KEY` in your environment or a local `.env`. Start from the package directory so the application's relative static-file paths resolve:

```sh
cd vehicle_image_recognition
python -m uvicorn vehicle_image_recognition.main:app --app-dir .. --host 127.0.0.1 --port 8000
```

Open the browser interface at `http://127.0.0.1:8000/` or the interactive API docs at `http://127.0.0.1:8000/docs`. Classification calls send uploaded images to OpenAI and require a working key and model access.

[Complete setup and troubleshooting →](docs/SETUP.md)

## API at a glance

| Method | Path | Task |
| --- | --- | --- |
| POST | `/identify_image_content/` | Classify delivery-image content |
| POST | `/identify_vehicle_orientation/` | Classify vehicle view orientation |

Both accept repeated multipart fields named `files`. See the [API reference](docs/API.md) for examples and response limitations.

## Current scope

This is a prototype with prompt-defined output, not an evaluated classification system. It has no committed executable tests or accuracy benchmark. The request implementation uses synchronous HTTP inside an async route and has no explicit timeout, upload-size limits, authentication, or schema validation for model results.

The source hard-codes `gpt-4o` and labels every inline image as JPEG. These constraints and the older dependency ranges are covered in the [architecture notes](docs/ARCHITECTURE.md).

## Author

**Jared Hall** · [GitHub](https://github.com/Bropaine) · [LinkedIn](https://www.linkedin.com/in/jared-hall-171596233/)
