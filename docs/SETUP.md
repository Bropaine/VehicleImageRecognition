# Local setup

[README](../README.md) · [API](API.md) · [Architecture](ARCHITECTURE.md)

## Prepare Python

Use a Python 3 installation with virtual-environment support. The repository does not declare or test a supported Python version matrix.

From the repository root:

```sh
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```sh
source .venv/bin/activate
```

Install the committed requirements and ensure multipart support is available:

```sh
python -m pip install -r requirements.txt
python -m pip install python-multipart
```

`python-multipart` is needed by the uploaded-file routes but is not explicitly listed in `requirements.txt`. The manifest uses historical version ranges, including FastAPI 0.111, Uvicorn 0.30, OpenAI 1.35, and Starlette 0.37.

## Configure the key

Create a local `.env` in the repository root:

```dotenv
OPENAI_API_KEY=replace-with-your-own-key
```

Alternatively, set the environment variable before launching. Keep real keys out of committed files. The code reads the key with `python-dotenv` and sends requests to OpenAI Chat Completions with the hard-coded model `gpt-4o`.

## Start with the correct working directory

The static files are committed under `vehicle_image_recognition/static/`, while the application looks for a directory named `static` relative to the current working directory.

Use this invocation from the repository root after activating the environment:

```sh
cd vehicle_image_recognition
python -m uvicorn vehicle_image_recognition.main:app --app-dir .. --host 127.0.0.1 --port 8000
```

`--app-dir ..` makes the package importable while the working directory satisfies the static-file lookup. Running the same module directly from the repository root without addressing this path mismatch can fail at startup.

## Try the interface

1. Open `http://127.0.0.1:8000/`.
2. Select a small batch of JPEG images.
3. Choose content or orientation classification with the toggle.
4. Submit the batch and inspect the returned labels.

For raw requests, use [the multipart examples](API.md) or FastAPI's `/docs` page. Review the request and response in the browser network panel when diagnosing a failed call.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `Directory 'static' does not exist` | Incorrect working directory |
| Cannot import `vehicle_image_recognition` | Missing `--app-dir ..` when running from the package directory |
| Multipart dependency error | Install `python-multipart` in the active environment |
| Generic 500 response | Inspect upstream response and server logs; key/model access or output parsing may have failed |
| Browser labels look wrong or incomplete | Output is model-generated and not schema-validated; inspect raw JSON |

The service prints upstream responses and parsed output to the terminal. Use suitable sample images when sharing diagnostic logs.

## Verification scope

`tests/__init__.py` and `setup.py` are empty placeholders. No automated test command or benchmark result is provided by this repository. The setup instructions were checked against source paths; live API execution requires your own credentials.
