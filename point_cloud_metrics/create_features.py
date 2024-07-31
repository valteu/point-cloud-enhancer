import os
import sys
import pandas as pd
from feature_extract import get_feature_vector
import time

def create_features(directory):
    # ply_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.ply')]

    ply_files = [directory + '/sparse/0/points.ply']

    all_features = []
    filenames = []

    # TODO clean paths
    for ply_file in ply_files:
        objpath = ply_file
        print(f"Processing {objpath}")
        start = time.time()
        try:
            features = get_feature_vector(objpath)
        except Exception as e:
            print(f"Failed to get features for {objpath} with error: {e}")
            continue
        end = time.time()
        time_cost = end - start
        print(f"Time cost: {time_cost} sec.")
        all_features.append(features)
        filenames.append(os.path.splitext(os.path.basename(ply_file))[0])

    feature_names = []
    for feature_domain in ['l', 'a', 'b', 'curvature', 'anisotropy', 'linearity', 'planarity', 'sphericity']:
        for param in ["mean", "std", "entropy", "ggd1", "ggd2", "aggd1", "aggd2", "aggd3", "aggd4", "gamma1", "gamma2"]:
            feature_names.append(f"{feature_domain}_{param}")

    feature_names = feature_names[:64]

    output_dir = os.path.join(directory, "point_cloud_metrics")
    os.makedirs(output_dir, exist_ok=True)
    features_df = pd.DataFrame(all_features, index=filenames, columns=feature_names)
    print(features_df)
    features_df.to_csv("point_cloud_metrics/features.csv")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python create_features.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    create_features(directory)
