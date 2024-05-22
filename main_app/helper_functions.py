from django.http import JsonResponse
import base64
import json
from main_app.scripts.predictions import predict_image
from rest_framework.response import Response

def upload_image(image_data, label_data):
    try:
        if not image_data or not label_data:
            return {'error': 'Image and label data are required.'}
        # Decode the image data
        image_data = base64.b64decode(image_data.split(',')[1])
        with open('uploaded_image.jpg', 'wb') as f:
            f.write(image_data)
        # Simulate prediction result
        result = predict_image('uploaded_image.jpg', label_data)
        # Convert any float32 to float
        result['predictions'] = [prediction for prediction in result['predictions']]
        if 'is_object_present' in result:
            result['is_object_present'] = result['is_object_present']
        return {'filePath': 'uploaded_image.jpg', 'predictions': result['predictions'], 'is_object_present': result.get('is_object_present')}
    except Exception as e:
        return {'error': str(e)}







