# dataset_loader.py
# ------------------
# Loads the CASIA v2 dataset using Keras's image_dataset_from_directory.
# This streams images directly from disk in batches — no RAM overload.
#
# Dataset structure:
#   dataset/dataset/
#       authentic/   → label 0
#       forged/      → label 1

import tensorflow as tf

# ── Settings ──────────────────────────────────────────
DATASET_DIR = "dataset/dataset"   # Root folder with authentic/ and forged/
IMG_SIZE    = (128, 128)          # Resize every image to 128x128
BATCH_SIZE  = 32                  # Number of images loaded per step
SEED        = 42                  # For reproducibility
# ──────────────────────────────────────────────────────


def load_datasets():
    """
    Load train and test datasets directly from folder.

    Uses Keras's image_dataset_from_directory which:
        - Reads images in batches (no full RAM load)
        - Automatically assigns labels from folder names
        - Splits into train (80%) and test (20%)
        
    Class labels assigned alphabetically:
        authentic → 0
        forged    → 1

    Returns:
        train_ds : tf.data.Dataset for training
        test_ds  : tf.data.Dataset for testing
    """

    # ── Training set (80% of data) ────────────────────
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        labels="inferred",        # Automatically use folder names as labels
        label_mode="binary",      # Output labels as 0 or 1 (not one-hot)
        image_size=IMG_SIZE,      # Resize all images to 128x128
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=SEED,
        validation_split=0.2,     # Reserve 20% for testing
        subset="training"         # This call gets the 80% training portion
    )

    # ── Test set (20% of data) ────────────────────────
    # IMPORTANT: shuffle=True with the SAME seed as train_ds
    # This ensures Keras shuffles the full file list before splitting,
    # so both train and test get a proper mix of authentic + forged images.
    # If shuffle=False here, Keras takes the LAST 20% alphabetically
    # which would be ALL forged images — causing a bad evaluation.
    test_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        labels="inferred",
        label_mode="binary",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,             # Must be True so split is class-balanced
        seed=SEED,                # Same seed as train — ensures consistent split
        validation_split=0.2,
        subset="validation"       # This call gets the 20% test portion
    )

    print(f"\nClass names (label order): {train_ds.class_names}")
    print(f"  Index 0 = {train_ds.class_names[0]}")
    print(f"  Index 1 = {train_ds.class_names[1]}")

    # ── Normalize pixel values from [0, 255] → [0, 1] ─
    # Rescaling(1/255) maps 0–255 → 0.0–1.0, matching what predict.py does.
    normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)

    train_ds = train_ds.map(
        lambda x, y: (normalization_layer(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )
    test_ds = test_ds.map(
        lambda x, y: (normalization_layer(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )

    # ── Cache normalized images (BEFORE augmentation) ────────────────────────
    # cache() stores normalized pixel values. Augmentation runs AFTER the cache,
    # so each epoch still gets FRESH random augmentation — cache does NOT freeze
    # augmented images. This also lets split_train_val() count batches correctly.
    train_ds = train_ds.cache()
    test_ds  = test_ds.cache()

    # ── Data Augmentation (training set ONLY) ─────────────────────────────────
    # Applied AFTER cache → runs freshly every epoch (random each time).
    # Do NOT augment the test set — it must look like real-world input.
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1),
    ])

    train_ds = train_ds.map(
        lambda x, y: (data_augmentation(x, training=True), y),
        num_parallel_calls=tf.data.AUTOTUNE
    )

    # ── Prefetch (load next batch while GPU trains current batch) ─────────────
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    test_ds  = test_ds.prefetch(tf.data.AUTOTUNE)

    return train_ds, test_ds


def split_train_val(train_ds, val_split=0.2):
    """
    Split the training dataset into train and validation.

    Args:
        train_ds : tf.data.Dataset from load_datasets()
        val_split : fraction to use for validation (default 0.2)

    Returns:
        train_ds : 80% for training
        val_ds   : 20% for validation
    """
    # Count total batches
    total_batches = tf.data.experimental.cardinality(train_ds).numpy()
    val_batches   = max(1, int(total_batches * val_split))

    val_ds   = train_ds.take(val_batches)
    train_ds = train_ds.skip(val_batches)

    return train_ds, val_ds
