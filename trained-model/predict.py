# predict.py
# -----------
# Predicts whether an image is Authentic (0) or Forged (1).
# Usage: python predict.py path/to/image.jpg

import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF verbose logging

import numpy as np
import tensorflow as tf
from PIL import Image

# ── Settings ──────────────────────────────────────────────────────────────────
MODEL_PATH = "model.keras"
IMG_SIZE   = (128, 128)
RESCALE    = 1.0 / 255
THRESHOLD  = 0.35  # Lowered from 0.5 → forged recall was only 19% at 0.5
                   # 0.35 catches forged images with sigmoid scores in 0.35–0.49 range
# ──────────────────────────────────────────────────────────────────────────────

# Cache model in memory so Django doesn't reload on every request
_model_cache = None


def _load_model():
    """Load model once and cache it."""
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at '{MODEL_PATH}'. Please run: python train.py"
            )
        _model_cache = tf.keras.models.load_model(MODEL_PATH)
    return _model_cache


def _preprocess_image(image_path):
    """
    Load and preprocess a single image for prediction.

    Steps:
        1. Open with PIL and convert to RGB (handles grayscale/RGBA)
        2. Resize to 128×128
        3. Normalize pixels [0, 255] → [0.0, 1.0]
        4. Add batch dimension → shape (1, 128, 128, 3)

    Returns:
        np.ndarray of shape (1, 128, 128, 3)
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) * RESCALE
    return np.expand_dims(arr, axis=0)


def predict_image(image_path):
    """
    Predict whether a single image is Authentic or Forged.

    Django integration:
        from predict import predict_image
        result = predict_image(request.FILES['image'].temporary_file_path())
        # result = {"label": "Forged", "confidence": 68.3, "raw_score": 0.683}

    Args:
        image_path : str — path to the image file

    Returns:
        dict with keys: label, confidence (%), raw_score
        or None if model is missing
    """
    try:
        model = _load_model()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return None

    print(f"\nAnalyzing: {os.path.basename(image_path)}")
    img_array = _preprocess_image(image_path)

    raw_score = float(model.predict(img_array, verbose=0)[0][0])

    # ── Decision logic ────────────────────────────────────────────────────────
    if raw_score >= THRESHOLD:
        label      = "Forged"
        confidence = raw_score * 100
    else:
        label      = "Authentic"
        confidence = (1.0 - raw_score) * 100

    # ── Debug bar visualization ───────────────────────────────────────────────
    bar_len   = 20
    bar_pos   = int(raw_score * bar_len)
    filled    = "-" * bar_pos
    empty     = "-" * (bar_len - bar_pos)
    thresh_pos = int(THRESHOLD * bar_len)

    bar = list("-" * bar_len)
    bar[bar_pos]   = "|"         # Current score marker
    bar[thresh_pos] = "|"        # Threshold marker
    bar_str = "".join(bar)

    print(f"[Debug] Raw sigmoid score : {raw_score:.6f}")
    print(f"[Debug] Threshold         : {THRESHOLD}")
    print(f"[Debug] 0.0=Authentic  |  1.0=Forged")
    print(f"[Debug] Score bar [{bar_str}]  threshold at pos {thresh_pos}")
    if raw_score >= THRESHOLD:
        print(f"[Debug] Decision: score {raw_score:.4f} >= {THRESHOLD}  ->  {label}  ({confidence:.1f}% confident)")
    else:
        print(f"[Debug] Decision: score {raw_score:.4f} < {THRESHOLD}  ->  {label}  ({confidence:.1f}% confident)")

    return {
        "label"      : label,
        "confidence" : round(confidence, 2),
        "raw_score"  : round(raw_score, 6),
        "image_path" : image_path,
    }


# ── CLI entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage  : python predict.py <image_path>")
        print("Example: python predict.py test_image.jpg")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"ERROR: Image not found: {path}")
        sys.exit(1)

    result = predict_image(path)

    if result:
        print("\n" + "=" * 40)
        print(f"  Result     : {result['label']}")
        print(f"  Confidence : {result['confidence']}%")
        print("=" * 40 + "\n")
