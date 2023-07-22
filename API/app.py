# RoamerAI
# Flask app to serve the backend API
# Uses CLIP and Sentence Transformers to perform image and text search
# Author: Chase Clingman
# Date: 5/24/23
# Version: 1.0

# Import necessary libraries and modules
import json
# from firebase_admin import credentials, firestore, initialize_app, storage
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import clip
from PIL import Image
import numpy as np
import pickle

from typing import List
from io import BytesIO

from PIL import UnidentifiedImageError

from sentence_transformers import SentenceTransformer, util

import re

# import intel_extension_for_pytorch as ipex

# Create Flask web server application
app = Flask(__name__)
# Enable Cross Origin Resource Sharing
CORS(app)

# The following commented lines are related to Firebase authentication. They have been left out because they require sensitive credentials.

# Load the model and preprocess from CLIP and optimize the model with intel_extension_for_pytorch (ipex)
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
# model = ipex.optimize(model)

# Configure Cross-Origin Resource Sharing (CORS)


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# Define helper functions

# Function to get top results based on similarity score


def get_top_results(top_results, similarity_score, image_url, image_data):
    # If the document id isn't in the top results, add it
    doc_id = image_data.get("doc_id", None)
    if doc_id not in top_results:
        top_results[doc_id] = {"similarity_score": similarity_score,
                               "image_url": image_url, "doc_data": image_data}
        top_results = dict(sorted(top_results.items(
        ), key=lambda x: x[1]["similarity_score"], reverse=True)[:10])
    return top_results

# Function to load preprocessed images from a pickle file


def load_processed_images_from_pickle(file_path):
    with open(file_path, 'rb') as f:
        processed_images = pickle.load(f)
    return processed_images


processed_images = load_processed_images_from_pickle('processed_images.pkl')

# Load the text model from Sentence Transformers
text_model = SentenceTransformer('msmarco-distilbert-base-tas-b')

# Function to load embeddings from a pickle file


def load_embeddings_from_pickle(file_path):
    with open(file_path, 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings


corpus_embeddings = load_embeddings_from_pickle('corpus_embeddings.pkl')


# Define the route for search
@app.route("/search", methods=["POST"])
def search():
    if "query" not in request.json:
        return jsonify({"error": "No query provided"}), 400

    # query = request.json["query"]


    input_text = request.json["query"]
    input_text = clip.tokenize([input_text]).to(device)

    with torch.no_grad():
        input_text_features = model.encode_text(input_text)

        top_results = {}

        image_features = torch.cat(
            [processed_image["image_features"] for processed_image in processed_images], dim=0)

        # Compute similarity scores
        similarity = input_text_features @ image_features.T
        similarity = similarity.cpu().numpy()

        # Get top results
        for i, processed_image in enumerate(processed_images):
            similarity_score = float(similarity[0][i])
            top_results = get_top_results(
                top_results, similarity_score, processed_image["image_url"], processed_image["image_data"])

    # Apply the filters on the top_results
    # filters = request.json.get("filters", {})
    # results = [result for result in top_results.values(
    # ) if filter_results(result, filters)]

    return jsonify(list(top_results.values()))  # Return the filtered results as a JSON response
# Define the route for processing image


@app.route("/process_image", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]
    input_image = preprocess(Image.open(image)).unsqueeze(0).to(device)

    with torch.no_grad():
        input_image_features = model.encode_image(input_image)

        top_results = {}

        image_features = torch.cat(
            [processed_image["image_features"] for processed_image in processed_images], dim=0)

        # Compute similarity scores
        similarity = input_image_features @ image_features.T
        similarity = similarity.cpu().numpy()

        # Get top results
        for i, processed_image in enumerate(processed_images):
            similarity_score = float(similarity[0][i])
            top_results = get_top_results(
                top_results, similarity_score, processed_image["image_url"], processed_image["image_data"])

    return jsonify(list(top_results.values()))


if __name__ == "__main__":
    app.run(debug=True)
