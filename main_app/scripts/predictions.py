import cv2
import numpy as np
import tensorflow as tf
import json

# Load the pre-trained ResNet50 model
model = tf.keras.applications.ResNet50(weights='imagenet')

# Function to preprocess images
def preprocess_image(image_path):
    # Read an image from the specified file path
    image = cv2.imread(image_path)

    # Resizes the image to 224x224 pixels, which is the required input size for ResNet50
    image = cv2.resize(image, (224, 224))

    # Converts the image from BGR color space (default in OpenCV) to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # TODO Check if this works with grayscale images
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Converts the image to a floating-point tensor with values in the range [0, 255]
    image = np.expand_dims(image, axis=0)

    # Preprocesses the image for the ResNet50 model by scaling pixel values appropriately
    image = tf.keras.applications.resnet50.preprocess_input(image)

    # Returns the preprocessed image ready for prediction
    return image

# Function to decode predictions
def decode_predictions(preds):
    return tf.keras.applications.resnet50.decode_predictions(preds, top=3)[0] # Decodes the prediction into a human-readable format

# Load the ImageNet labels from the JSON file
with open('main_app/scripts/predictions.py', 'r') as file:
    imagenet_labels = json.load(file)

# Display available keys to the user
print("Available categories:")
for i, key in enumerate(imagenet_labels.keys(), 1):
    print(f"{i}. {key}")

# Prompt the user to select a key
key_choice = int(input("Enter the number corresponding to the category you want to check: "))
selected_key = list(imagenet_labels.keys())[key_choice - 1]

# Display the values associated with the chosen key
print(f"Values for {selected_key}:")
for value in imagenet_labels[selected_key]:
    print(value)

# Prompt the user to select a value
object_name = input("Enter the name of the object you want to check from the list above: ")

# Preprocess the image
image_path = input("Enter the filename of the photo: ")
preprocessed_image = preprocess_image(image_path)

# Make predictions
predictions = model.predict(preprocessed_image)

# Decode predictions
decoded_predictions = decode_predictions(predictions)

# Check if the top predictions match the specified object
is_object = any(
    object_name.lower() == pred[1].lower() for pred in decoded_predictions
)

if is_object:
    print("Correct!")
else:
    print("Incorrect! Please try again.")