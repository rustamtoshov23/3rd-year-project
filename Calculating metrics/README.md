Setup (Calculating metrics)

This folder contains the `metrics` utilities used for pixel/object segmentation metrics.
A virtual environment was created at `.venv` and the packages listed in `requirements.txt` were installed.

Quick start (zsh / macOS)

1) Activate the project's venv:

```zsh
cd "$(dirname "$0")" # run from within this folder or `cd` to the folder first
source .venv/bin/activate
```

2) If you need to recreate the environment (fresh machine):

```zsh
# create the venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3) Verify imports quickly:

```zsh
# from within this folder and with the venv activated
python -c "import numpy; import cv2; import sys; sys.path.insert(0, '.'); import metrics; print('numpy', numpy.__version__); print('cv2', cv2.__version__); print('metrics OK')"
```

Notes and troubleshooting
- OpenCV: `utils.py` imports `cv2`, so `opencv-python` is required (already in `requirements.txt`).
- Cython: `metrics.py` uses `pyximport` to import `compute_overlap` — a C compiler may be needed to build Cython `.pyx` files at import-time. On macOS install Xcode Command Line Tools if you see build errors:

```zsh
xcode-select --install
```

- Reproducibility: To capture exact packages from the working venv, activate the venv and run:

```zsh
pip freeze > requirements-frozen.txt
```

- Location of the created venv: `.venv` (inside this folder). If you'd prefer the venv at the repo root or elsewhere, move or recreate accordingly.

If you'd like, I can:
- add a `requirements-frozen.txt` generated from the `.venv`,
- add a tiny test script that runs a minimal `ObjectMetrics`/`PixelMetrics` check on synthetic data, or
- move the venv to the repo root and update instructions. Which would you prefer?