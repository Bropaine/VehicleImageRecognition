# API reference

[README](../README.md) · [Setup](SETUP.md) · [Architecture](ARCHITECTURE.md)

Base URL: `http://127.0.0.1:8000`.

## Upload contract

Both routes accept `multipart/form-data` with one or more repeated `files` fields. Upload order is retained when building the model request. The server reads each entire file into memory and labels its inline data URL as `image/jpeg`; JPEG samples best match the existing payload construction.

Do not send a JSON file-path list or manually set a multipart boundary.

## Classify image content

`POST /identify_image_content/`

POSIX shell example; on Windows use `curl.exe` and equivalent file paths:

```sh
curl -X POST http://127.0.0.1:8000/identify_image_content/ \
  -F 'files=@samples/vehicle.jpg' \
  -F 'files=@samples/receipt.jpg'
```

The `samples/` paths are illustrative files you supply, not committed fixtures.

Prompt-requested labels:

| Label | Intended meaning |
| --- | --- |
| `vehicle` | Vehicle image |
| `delivery_receipt` | Vehicle delivery receipt |
| `bol` | Bill of lading |
| `damaged_vehicle` | Visible vehicle damage |
| `gauge_reading` | Odometer or fuel-gauge image |
| `other` | Other content |

Illustrative model output:

```json
{
  "image_01": "vehicle",
  "image_02": "delivery_receipt"
}
```

## Classify orientation

`POST /identify_vehicle_orientation/`

```sh
curl -X POST http://127.0.0.1:8000/identify_vehicle_orientation/ \
  -F 'files=@samples/front.jpg' \
  -F 'files=@samples/side.jpg'
```

The prompt requests `front`, `back`, `left_side`, `right_side`, or `other`. For side views, left/right means the direction the vehicle's front points within the image, rather than the physical driver/passenger side.

## Response behavior

The service JSON-decodes the model's text and returns it directly. It does not validate category membership, key numbering, result count, or a response schema.

The prompt examples begin at `image_01`, while internal labels are constructed from index zero and are not included as explicit labels in the payload. Treat output key numbering as model-defined. The browser currently displays values by returned object order.

## Errors and practical limits

- FastAPI validates the multipart request and requires the `files` field.
- A JSON decoding error returns HTTP 500 with `{"error":"Invalid response from API"}`.
- Other exceptions inside the response-parsing block return HTTP 500 with `{"error":"An error occurred"}`.
- The outbound HTTP call occurs before that parsing block; connection failures are not covered by its custom error responses.
- No explicit request timeout, retry policy, upload-size limit, or batch-size limit is configured.
- The hard-coded model output budget is 300 tokens. Large batches can exceed that budget.

For integration work, start with small batches and inspect raw responses rather than assuming a complete, validated result for every image.
