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
with open('main_app/data/imagenet.json', 'r') as file:
    imagenet_labels = json.load(file)

# Convert the loaded JSON into a more usable format
category_to_names = {}
for entry in imagenet_labels:
    category = entry['category']
    name = entry['name']
    if category not in category_to_names:
        category_to_names[category] = []
    category_to_names[category].append(name)

# Display available categories to the user
print("Available categories:")
for i, key in enumerate(category_to_names.keys(), 1):
    print(f"{i}. {key}")

# Prompt the user to select a category
key_choice = int(input("Enter the number of the category you want to select: "))
selected_key = list(category_to_names.keys())[key_choice - 1]

# Display the values associated with the chosen category
print(f"Values for {selected_key}:")
for value in category_to_names[selected_key]:
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

# Print the results
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    # Iterate over the decoded predictions with an index
    # 'i' is the index, starting from 0
    # 'imagenet_id' is the ImageNet ID of the predicted class
    # 'label' is the human-readable label of the predicted class
    # 'score' is the confidence score of the prediction

    # Print the index (i+1), label, and score of each prediction
    # '{i+1}' converts the index to 1-based instead of 0-based
    # '{label}' is the human-readable label of the predicted class
    # '{score:.2f}' formats the score to 2 decimal places
    print(f"{i+1}: {label} ({score:.2f})")

if is_object:
    print("Correct!")
else:
    print("Incorrect! Please try again.")
