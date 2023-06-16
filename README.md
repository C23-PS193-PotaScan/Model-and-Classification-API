# Model-and-Classification-API

for classification-API final on dev-deploy branch

This repository contains the documentation for the Model and Classification API. The API allows users to classify potato leaf diseases based on uploaded images.

## API Base URL
The base URL for accessing the API is: https://model-and-classification-api-fbaiidjkha-uc.a.run.app/

## Available Endpoints
**GET /**

This endpoint is used to test the API connectivity. It returns a success message.

Method: GET

URL: https://model-and-classification-api-fbaiidjkha-uc.a.run.app/

**Response:**

```json
{
  "response": "success!"
}
```

**POST /upload**

This endpoint is used to classify potato leaf diseases. Users need to upload an image file of a potato leaf for classification.

**Method: POST**

URL: https://model-and-classification-api-fbaiidjkha-uc.a.run.app/upload

**Parameters:**

`file`: Image file of the potato leaf (multipart/form-data)

**Response:**

```json
{
  "message": "gambar terkirim",
  "response": "Potato Late Blight"
}
```
The response includes a message confirming the successful upload of the image and the classified disease name.
