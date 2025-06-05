#!/bin/bash

# Replace 'your_image.jpg' with the path to your image file
IMAGE_PATH="your_image.jpg"

# Replace 'http://localhost:8000' with your actual API endpoint if different
API_URL="http://localhost:8000/predict"

# Send the POST request with the image file
curl -v -X POST \
  -F "file=@${IMAGE_PATH}" \
  "${API_URL}" 