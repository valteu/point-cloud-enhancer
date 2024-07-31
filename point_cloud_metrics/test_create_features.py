import os
import pandas as pd
from feature_extract import get_feature_vector
import time

all_features = []
filenames = []

objpath = '../datasets/both_pingpong/sparse/0/points.ply'
features = get_feature_vector(objpath)
end = time.time()
all_features.append(features)
filenames.append('test_1')

feature_names = []
for feature_domain in ['l', 'a', 'b', 'curvature', 'anisotropy', 'linearity', 'planarity', 'sphericity']:
    for param in ["mean", "std", "entropy", "ggd1", "ggd2", "aggd1", "aggd2", "aggd3", "aggd4", "gamma1", "gamma2"]:
        feature_names.append(f"{feature_domain}_{param}")

feature_names = feature_names[:64]

features_df = pd.DataFrame(all_features, index=filenames, columns=feature_names)
features_df.to_csv("features.csv")

