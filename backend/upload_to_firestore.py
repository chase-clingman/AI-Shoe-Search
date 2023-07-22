# RoamerAI
# Python script to upload data to the Firestore database
# Author: Chase Clingman
# Date: 5/24/23

import json
import firebase_admin
from firebase_admin import credentials, firestore

from collections import defaultdict

# Load your service account key JSON file
cred = credentials.Certificate('./firebase.json')

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Load your JSON data from the file
with open('./shoes.json', 'r') as f:
    json_data = json.load(f)

# # Function to upload data to Firestore
# def upload_data(data):
#     for item in data:
#         # You can use the 'Building Title' as the document ID or use Firestore's auto-generated IDs
#         doc_ref = db.collection('shoes').document()
#         doc_ref.set(item)

# # Call the function to upload the data
# upload_data(json_data)


def count_documents_and_images():
    # Get the cleaned collection
    cleaned_ref = db.collection('shoes')

    # Retrieve all documents from the collection
    docs = cleaned_ref.stream()

    # Initialize counters
    document_count = 0
    image_count = 0

    # Iterate through each document
    for doc in docs:
        document_count += 1
        doc_data = doc.to_dict()

        # Check if the 'Images' field exists in the document
        if 'Image URL' in doc_data:
            image_count += len(doc_data['Image URL'])

    return document_count, image_count

# Call the function and print the results
doc_count, img_count = count_documents_and_images()
print(f'Total number of documents: {doc_count}')
print(f'Total number of images: {img_count}')




# def group_documents_by_building_title():
#     # Get the cleaned collection
#     cleaned_ref = db.collection('cleaned 2')

#     # Retrieve all documents from the collection
#     docs = cleaned_ref.stream()

#     # Initialize a dictionary to group the documents by Building Title
#     grouped_docs = defaultdict(list)

#     # Iterate through each document
#     for doc in docs:
#         doc_data = doc.to_dict()

#         # Check if the 'Building Title' field exists in the document
#         if 'Building Title' in doc_data:
#             building_title = doc_data['Building Title']
#             grouped_docs[building_title].append(doc_data)

#     return grouped_docs

# # Call the function and print the results
# grouped_documents = group_documents_by_building_title()
# for building_title, docs in grouped_documents.items():
#     if len(docs) > 1:
#         print(f'Building Title: {building_title}')
#         print(f'Number of documents with the same Building Title: {len(docs)}')
#         print()

# def remove_duplicates():
#     # Get all documents from the 'cleaned' collection
#     docs = db.collection('cleaned 2').stream()

#     # Store the document IDs of duplicates
#     duplicates = []

#     # Store unique 'Building Title' values
#     unique_building_titles = {}

#     for doc in docs:
#         building_title = doc.to_dict().get('Building Title')

#         # If the 'Building Title' is already in the unique_building_titles dictionary, 
#         # add the document ID to the duplicates list
#         if building_title in unique_building_titles:
#             unique_building_titles[building_title].append(doc.id)
#             duplicates.extend(unique_building_titles[building_title][1:])
#         else:
#             unique_building_titles[building_title] = [doc.id]

#     # Delete duplicate documents
#     for doc_id in duplicates:
#         db.collection('cleaned 2').document(doc_id).delete()
#         print(f"Deleted document with ID: {doc_id}")

# # Call the function to remove duplicates
# remove_duplicates()