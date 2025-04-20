import argparse
import os
import subprocess
import sys
from dense_reconstruction_cli import as_function


def run_command(command, cwd=None):
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True, cwd=cwd)

datasets = [
    "electro",
    "meadow",
    "playground",
    "courtyard",
    "facade",
    "office",
    "relief",
    "terrace",
    "delivery_area",
    "kicker",
    "pipes",
    "relief_2",
    "terrains"
]

images = [
    "enh_1"
]

for dataset in datasets:
    for image in images:
        as_function(dataset, image)
