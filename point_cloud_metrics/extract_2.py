import os
import pandas as pd
from feature_extract import get_feature_vector
import time

def create_features(directory='../pointclouds_pce/'):

    ply_files = [f for f in os.listdir(directory) if f.endswith('.ply')]

    all_features = []
    filenames = []

    for ply_file in ply_files:
        objpath = os.path.join(directory, ply_file)
        print(f"Processing {objpath}")
        start = time.time()
        features = get_feature_vector(objpath)
        end = time.time()
        time_cost = end - start
        print(f"Time cost: {time_cost} sec.")
        all_features.append(features)
        filenames.append(os.path.splitext(ply_file)[0])

    feature_names = []
    for feature_domain in ['l', 'a', 'b', 'curvature', 'anisotropy', 'linearity', 'planarity', 'sphericity']:
        for param in ["mean", "std", "entropy", "ggd1", "ggd2", "aggd1", "aggd2", "aggd3", "aggd4", "gamma1", "gamma2"]:
            feature_names.append(f"{feature_domain}_{param}")

    feature_names = feature_names[:64]

    features_df = pd.DataFrame(all_features, index=filenames, columns=feature_names)
    features_df.to_csv("features.csv")

if __name__ == '__main__':
    create_features()
