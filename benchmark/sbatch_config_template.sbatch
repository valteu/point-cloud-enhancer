#!/bin/bash
#SBATCH --job-name=colmap_gpu_job
#SBATCH --partition=gpupro
#SBATCH --gpus=a40:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=valentin.teutschbein@student.hpi.uni-potsdam.de

PROJECT="$HOME/point-cloud-enhancer"

srun \
  --container-image="$HOME/colmap-gpu.sqsh" \
  --container-mounts="$PROJECT:$PROJECT" \
  --container-workdir="$PROJECT/benchmark" \
  --gpus=a40:1 \
  --cpus-per-task=16 \
  --mem=32G \
  --time=24:00:00 \
  --partition=gpupro \
  python3 run_benchmark_resized.py

