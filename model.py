# model.py
# --------
# Builds the CNN architecture for image forgery detection.
# Uses L2 regularization on all Conv + Dense layers to prevent overfitting.

import tensorflow as tf
from tensorflow.keras import regularizers

L2 = 1e-4   # L2 regularization factor — applied to all Conv and Dense weights


def build_model():
    """
    Build a custom CNN for binary image classification.

    Architecture:
        Input (128×128×3)
            ↓
        [Conv2D(32,  L2) → BatchNorm → ReLU → MaxPool → Dropout(0.25)]  Block 1
            ↓
        [Conv2D(64,  L2) → BatchNorm → ReLU → MaxPool → Dropout(0.25)]  Block 2
            ↓
        [Conv2D(128, L2) → BatchNorm → ReLU → MaxPool → Dropout(0.30)]  Block 3
            ↓
        [Conv2D(256, L2) → BatchNorm → ReLU → MaxPool → Dropout(0.30)]  Block 4
            ↓
        Flatten
            ↓
        Dense(512, L2) → BatchNorm → ReLU → Dropout(0.50)
            ↓
        Dense(128, L2) → BatchNorm → ReLU → Dropout(0.40)
            ↓
        Dense(1) → Sigmoid
            ↓
        Output: 0 = Authentic | 1 = Forged

    Returns:
        model : Uncompiled Keras model
    """

    model = tf.keras.Sequential([
        # ── Input ─────────────────────────────────────────────────────────────
        tf.keras.layers.Input(shape=(128, 128, 3)),

        # ── Block 1: Conv 32 ──────────────────────────────────────────────────
        tf.keras.layers.Conv2D(32, (3, 3), padding='same',
                               kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),

        # ── Block 2: Conv 64 ──────────────────────────────────────────────────
        tf.keras.layers.Conv2D(64, (3, 3), padding='same',
                               kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),

        # ── Block 3: Conv 128 ─────────────────────────────────────────────────
        tf.keras.layers.Conv2D(128, (3, 3), padding='same',
                               kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.30),

        # ── Block 4: Conv 256 ─────────────────────────────────────────────────
        tf.keras.layers.Conv2D(256, (3, 3), padding='same',
                               kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.30),

        # ── Flatten ───────────────────────────────────────────────────────────
        tf.keras.layers.Flatten(),

        # ── Dense Block 1 (512) ───────────────────────────────────────────────
        tf.keras.layers.Dense(512, kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dropout(0.50),

        # ── Dense Block 2 (128) ───────────────────────────────────────────────
        tf.keras.layers.Dense(128, kernel_regularizer=regularizers.l2(L2)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dropout(0.40),

        # ── Output ────────────────────────────────────────────────────────────
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    return model


def compile_model(model):
    """
    Compile the model with optimizer, loss, and metrics.

    Args:
        model : Uncompiled Keras model from build_model()

    Returns:
        model : Compiled model ready for training
    """

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")
        ]
    )

    return model
