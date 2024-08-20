import pipeline.data_preperation
import pipeline.face_clustering
import pipeline.pca_analysis
# import plotting
from flask_pymongo import PyMongo
from io import BytesIO
import zipfile
import datetime
from bson import ObjectId

# Initialize Flask-PyMongo
from app import mongo  # Import mongo from app

def run_clustering_pipeline(image_ids):
    detection_method = "hog"
    min_face_size = 20

    print("[INFO] Loading and encoding images...")
    data = pipeline.data_preperation.load_and_encode_images(image_ids, detection_method, min_face_size)

    encodings = [d["encoding"] for d in data]

    print("[INFO] Calculating explained variance...")
    n_components_values, explained_variances = pipeline.pca_analysis.calculate_explained_variance(encodings)

    optimal_components = pipeline.pca_analysis.determine_optimal_components(explained_variances, threshold=0.86)
    print(f"[INFO] Optimal number of components for PCA: {optimal_components}")

    print("[INFO] Applying PCA reduction...")
    reduced_data = pipeline.pca_analysis.apply_pca(encodings, n_components=optimal_components)

    labels, labelIDs = pipeline.face_clustering.cluster_faces(reduced_data)

    # Save faces to the database
    uploads_collection = mongo.db.uploads
    # for item in data:
    #     image_id = item["imageId"]
    #     image = uploads_collection.find_one({'_id': image_id})
    #     image_data = image['image_data']  # Fetch image data from the database

    #     uploads_collection.update_one(
    #         {'_id': image_id},
    #         {
    #             '$set': {
    #                 'encoding': item["encoding"],  # Store encoding with the image
    #             }
    #         }
    #     )

    # Save cluster results to the database
    clusters_collection = mongo.db.clusters
    for label in set(labels):
        cluster_images = [data[i]['imageId'] for i in range(len(data)) if labels[i] == label]
        
        # Create a zip file for the cluster
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for image_id in cluster_images:
                image = uploads_collection.find_one({'_id': ObjectId(image_id)})
                zipf.writestr(image['filename'], image['image_data'])
        
        # Save the zip file to the database
        zip_data = zip_buffer.getvalue()
        clusters_collection.insert_one({
            'cluster_label': f'cluster_{label}',
            'images': cluster_images,
            'zip_data': zip_data
        })
