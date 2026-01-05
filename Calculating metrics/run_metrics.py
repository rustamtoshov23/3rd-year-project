"""Simple CLI to run `metrics.Metrics` on two image/array files.

Usage example (zsh):
    source "Calculating metrics/.venv/bin/activate"
    python run_metrics.py truth.tif pred.tif --model-name mymodel --outdir ./out

Supported input formats:
- .npy (NumPy arrays)
- .tif / .tiff (read with tifffile)
- others supported by skimage.io.imread

Notes:
- If the inputs are 2D arrays, they will be wrapped into a batch dimension.
- If you want more custom behavior (thresholding, relabel, 3D), edit this script.
"""

import argparse
import os
import sys

import numpy as np
from skimage import io
import tifffile

# Ensure the package path includes this folder so "import metrics" works
sys.path.insert(0, os.path.dirname(__file__))
from metrics import Metrics


def load_array(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.npy':
        return np.load(path)
    if ext in ('.tif', '.tiff'):
        return tifffile.imread(path)
    # fallback to skimage for other formats
    return io.imread(path)


def ensure_batch(arr):
    arr = np.asarray(arr)
    # If 2D (x,y) or 3D (x,y,chan) treat as single frame and add batch dim
    if arr.ndim in (2, 3):
        return np.expand_dims(arr, 0)
    return arr


def main():
    p = argparse.ArgumentParser(description='Run segmentation metrics on two files')
    p.add_argument('truth', help='Path to ground-truth file (.npy, .tif, ... )')
    p.add_argument('pred', help='Path to predicted file (.npy, .tif, ... )')
    p.add_argument('--model-name', default='model', help='Name used in output filename')
    p.add_argument('--outdir', default='.', help='Directory to save JSON output')
    p.add_argument('--cutoff1', type=float, default=0.4)
    p.add_argument('--cutoff2', type=float, default=0.1)
    p.add_argument('--pixel-threshold', type=float, default=0.5)
    p.add_argument('--is-3d', action='store_true', help='Treat inputs as 3D (batch,z,x,y)')
    args = p.parse_args()

    truth = load_array(args.truth)
    pred = load_array(args.pred)

    truth = ensure_batch(truth)
    pred = ensure_batch(pred)

    if truth.shape != pred.shape:
        raise SystemExit('Shape mismatch: truth {} vs pred {}'.format(truth.shape, pred.shape))

    m = Metrics(
        model_name=args.model_name,
        outdir=args.outdir,
        cutoff1=args.cutoff1,
        cutoff2=args.cutoff2,
        pixel_threshold=args.pixel_threshold,
        is_3d=args.is_3d,
    )

    # This will compute object and pixel stats and save a JSON in outdir
    m.run_all(truth, pred)
    print('Saved metrics to', args.outdir)


if __name__ == '__main__':
    main()
