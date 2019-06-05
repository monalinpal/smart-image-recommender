
import numpy as np
import h5py
import argparse
from keras.models import load_model
from sklearn.metrics import pairwise_distances
import cv2
from imutils import build_montages
import sys
import keras.backend as K
import os
import keras

def image_find(imagename):

    def euclidean_distance(a,b):
        return K.sqrt(K.sum(K.square((a-b)), axis=1))

    def get_triplets(data, labels):
        pos_label, neg_label = np.random.choice(labels, 2, replace=False)

        pos_indexes = np.where(labels == pos_label)[0]
        neg_indexes = np.where(labels == neg_label)[0]

        np.random.shuffle(pos_indexes)
        np.random.shuffle(neg_indexes)

        anchor = data[pos_indexes[0]]
        positive = data[pos_indexes[-1]]
        negative = data[neg_indexes[0]]

        return (anchor, positive, negative)

    def extract_features(hdf5_path):
        db = h5py.File(hdf5_path,mode="r")
        features = db["features"][:]
        labels = db["labels"][:]

        return (features, labels)

    def triplet_loss(y_true, anchor_positive_negative_tensor):
        anchor = anchor_positive_negative_tensor[:,:,0]
        positive = anchor_positive_negative_tensor[:,:,1]
        negative = anchor_positive_negative_tensor[:,:,2]

        Dp = euclidean_distance(anchor, positive)
        Dn = euclidean_distance(anchor, negative)

        return K.maximum(0.0, 1+K.mean(Dp-Dn))

    args={}
    args["image"]="images2\\"+str(imagename)
    args["model"]=os.path.abspath(os.path.dirname(__file__))+"/myntra_vgg16_large.model"
    args["features_db"]=os.path.abspath(os.path.dirname(__file__))+"/myntra_vgg16_large.hdf5"

    image_ids = h5py.File(args["features_db"], mode="r")["image_ids"][:]

    def get_image_index():
        filename = str(args["image"])
        return np.where(image_ids == filename)[0][0]

    def get_image_path(index):
        image_id_index=str(image_ids[index]).split("\\")[-1]
        return os.path.abspath(os.path.dirname(__file__))+"/images2/"+str(image_id_index)

    model = load_model(args["model"], custom_objects={"triplet_loss":triplet_loss})
    features, labels = extract_features(args["features_db"])

    embeddings = model.predict([features, features, features])
    embeddings = embeddings[:,:,2]

    image_id = get_image_index()
    query = embeddings[image_id]

    distances = pairwise_distances(query.reshape(1,-1), embeddings)
    indices = np.argsort(distances)[0][:8]
    images = [cv2.imread(get_image_path(index)) for index in indices]
    images = [cv2.resize(image, (200,200)) for image in images]
    result = build_montages(images, (200, 200), (4,2))[0]

    cv2.imwrite(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','static','recommend','images','output.png')),result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    keras.backend.clear_session()