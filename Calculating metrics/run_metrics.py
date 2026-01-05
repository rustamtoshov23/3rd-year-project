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
import glob
import json

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
    p.add_argument('--summary-only', action='store_true', help='Delete detailed JSON and keep only compact summary')
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
    # Try to find the generated detailed JSON (created by Metrics) and
    # produce a compact summary containing the image-level ("average")
    # metrics for pixel and object stat types.
    pattern = os.path.join(args.outdir, f"{args.model_name}*.json")
    # Exclude any existing summary files when selecting the detailed JSON
    candidates = [p for p in glob.glob(pattern) if not p.endswith(f"_{'summary'}.json") and not p.endswith(f"_summary.json")]
    detailed_json = None
    if candidates:
        # pick the most recently modified file
        detailed_json = max(candidates, key=os.path.getmtime)

    summary = {"metadata": {"model_name": args.model_name}}
    if detailed_json:
        try:
            with open(detailed_json, 'r') as f:
                data = json.load(f)
            metrics = data.get('metrics', [])
            pixel_avg = {m['name']: m['value'] for m in metrics if m.get('feature') == 'average' and m.get('stat_type') == 'pixel'}
            object_avg = {m['name']: m['value'] for m in metrics if m.get('feature') == 'average' and m.get('stat_type') == 'object'}
            summary['pixel_summary'] = pixel_avg
            summary['object_summary'] = object_avg
            # include original metadata if present
            if 'metadata' in data:
                summary['metadata'].update(data['metadata'])
        except Exception:
            # Fallback: no detailed file readable
            summary['error'] = 'failed to read detailed JSON'
    else:
        summary['error'] = 'detailed JSON not found in outdir'

    # Write compact summary
    summary_path = os.path.join(args.outdir, f"{args.model_name}_summary.json")
    try:
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print('Saved compact summary to', summary_path)
    except Exception as e:
        print('Failed to write summary:', e)

    # If requested, remove the detailed JSON files and keep only the summary
    if getattr(args, 'summary_only', False):
        removed = []
        for pth in candidates:
            try:
                # don't remove the summary file itself if it matched (it shouldn't)
                if os.path.abspath(pth) == os.path.abspath(summary_path):
                    continue
                os.remove(pth)
                removed.append(pth)
            except Exception as e:
                print('Failed to remove', pth, ':', e)
        if removed:
            print('Removed detailed JSON files:')
            for r in removed:
                print('  ', r)
        else:
            print('No detailed JSON files found to remove')

    print('Saved metrics to', args.outdir)


if __name__ == '__main__':
    main()
