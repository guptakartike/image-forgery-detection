from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
import os

app = Flask(__name__)

IMG_SIZE = (128, 128)
RESCALE = 1.0 / 255.0
THRESHOLD = float(os.getenv('PREDICTION_THRESHOLD', '0.35'))

_MODEL = None


def _resolve_model_path():
    env_model_path = os.getenv('MODEL_PATH')
    if env_model_path:
        return env_model_path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, 'model.keras'),
        os.path.join(base_dir, '..', '..', 'trained-model', 'model.keras'),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return candidates[-1]


def _get_model():
    global _MODEL
    if _MODEL is None:
        model_path = _resolve_model_path()
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at '{model_path}'. Set MODEL_PATH or place model.keras in trained-model/."
            )
        _MODEL = tf.keras.models.load_model(model_path)
    return _MODEL


def _has_model_file():
    return os.path.exists(_resolve_model_path())


def _preprocess_image(file_storage):
    image = Image.open(file_storage.stream).convert('RGB')
    image = image.resize(IMG_SIZE)
    array = np.array(image, dtype=np.float32) * RESCALE
    return np.expand_dims(array, axis=0)


def _fallback_forgery_probability(batch):
    """
    Heuristic fallback used only when trained weights are not available.
    It estimates suspicious high-frequency texture and chroma imbalance.
    """
    image = batch[0]

    # Edge/high-frequency proxy using finite differences.
    dx = np.abs(np.diff(image, axis=1)).mean()
    dy = np.abs(np.diff(image, axis=0)).mean()
    high_freq = float((dx + dy) * 2.0)

    # Channel disagreement proxy; synthetic images can show stronger color consistency artifacts.
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    chroma_gap = float((np.abs(r - g).mean() + np.abs(g - b).mean()) / 2.0)

    forged_prob = 0.20 + 0.65 * high_freq + 0.15 * chroma_gap
    return float(np.clip(forged_prob, 0.01, 0.99))


@app.get('/health')
def health():
    return jsonify({'status': 'ok', 'modelLoaded': _has_model_file()})


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']

    try:
        batch = _preprocess_image(file)
        using_fallback = False

        if _has_model_file():
            model = _get_model()
            forged_prob = float(model.predict(batch, verbose=0)[0][0])
        else:
            using_fallback = True
            forged_prob = _fallback_forgery_probability(batch)

        ai_score = max(0.0, min(100.0, forged_prob * 100.0))
        real_score = max(0.0, min(100.0, (1.0 - forged_prob) * 100.0))
        label = 'Forged' if forged_prob >= THRESHOLD else 'Authentic'
        confidence = ai_score if label == 'Forged' else real_score

        return jsonify({
            'label': label,
            'confidence': round(confidence, 2),
            'raw_score': round(forged_prob, 6),
            'real': round(real_score, 2),
            'ai': round(ai_score, 2),
            'threshold': THRESHOLD,
            'fallback': using_fallback,
        })
    except Exception as exc:
        return jsonify({'error': f'Inference failed: {str(exc)}'}), 500


if __name__ == '__main__':
    model_port = int(os.getenv('MODEL_PORT', '5000'))
    debug_mode = os.getenv('MODEL_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=model_port, debug=debug_mode, use_reloader=False)
