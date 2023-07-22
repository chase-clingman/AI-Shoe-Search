# Import necessary libraries
import json
import requests
import pickle
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Import necessary modules for PyTorch and CLIP model
import torch
import clip

# Import Firebase admin SDK
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage

# Check if CUDA is available and set the device accordingly
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Load the Firebase configuration
with open("firebase_config.json") as f:
    firebase_config = json.load(f)

# Load the Firebase service account credentials
cred = credentials.Certificate("firebase.json")

# Initialize the Firebase Admin SDK with storageBucket configuration
firebase_app = initialize_app(cred, {
    'storageBucket': firebase_config["storageBucket"]
})

# Initialize Firestore and Storage references
bucket = storage.bucket(app=firebase_app)
db = firestore.client()

# Define a function to load and process images from the Firestore database
def load_and_process_images(db):
    processed_images = []

    shoes_ref = db.collection('shoes')
    docs = shoes_ref.stream()

    # Loop over each document in the Firestore collection
    for doc in docs:
        image_data = {**doc.to_dict(), "doc_id": doc.id}

        # Look for keys that start with "Image" and process them
        if "Image URL" in image_data:
            image_url = image_data["Image URL"]
            if image_url:
                if not image_url.startswith("https"):
                    print(f"Skipping non-https image at {image_url}.")
                    continue
                
                # Try to open the image and preprocess it
                try:
                    image_tensor = preprocess(Image.open(requests.get(image_url, stream=True).raw)).unsqueeze(0).to(device)
                    
                    # Compute image features with CLIP
                    with torch.no_grad():
                        image_features = model.encode_image(image_tensor)
                    
                    # Append the processed image to the list
                    processed_images.append({
                        "image_tensor": image_tensor,  # Store the original 4D tensor
                        "image_features": image_features,
                        "image_url": image_url,
                        "image_data": image_data})
                except UnidentifiedImageError:
                    print(f"Unable to process image at {image_url}. Skipping...")

    # Save the processed_images to a Pickle file for later use
    with open('processed_images.pkl', 'wb') as f:
        pickle.dump(processed_images, f)

    return processed_images

# Call the function to load and preprocess images
processed_images = load_and_process_images(db)
print(processed_images)
print(type(processed_images))

# Import the SentenceTransformer library
from sentence_transformers import SentenceTransformer, util

# Load the SentenceTransformer model
text_model = SentenceTransformer('msmarco-distilbert-base-tas-b')

# To encode the text remove the superfluous text and add to a list
property_contexts = []
fields = ['Price', 'Shoe Name']

# Extract the relevant fields from the image data
for i in processed_images:
    context = []
    for field in fields:
        try:
            context.append(str(i['image_data'][field]).strip())
        except KeyError:
            continue
    property_contexts.append(' '.join(context))

# Compute embeddings for all contexts using the SentenceTransformer model
corpus_embeddings = text_model.encode(property_contexts, convert_to_tensor=True)

# Save the embeddings to a Pickle file for later use
with open('corpus_embeddings.pkl', 'wb') as f:
    pickle.dump(corpus_embeddings, f)
