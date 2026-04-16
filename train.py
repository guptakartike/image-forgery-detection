# train.py
# ---------
# Trains the CNN on the CASIA v2 dataset.
# Run: python train.py

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from dataset_loader import load_datasets, split_train_val
from model import build_model, compile_model

# ── Settings ──────────────────────────────────────────────────────────────────
EPOCHS     = 35        # EarlyStopping(patience=5) will auto-stop if val_loss plateaus
MODEL_PATH = "model.keras"
os.makedirs("graphs", exist_ok=True)
# ──────────────────────────────────────────────────────────────────────────────


# ── Step 1: Load dataset ──────────────────────────────────────────────────────
print("\n--- Step 1: Loading Dataset ---")
train_ds, test_ds = load_datasets()
train_ds, val_ds  = split_train_val(train_ds)


# ── Step 2: Class weights ─────────────────────────────────────────────────────
# CASIA v2: 7492 authentic vs 5125 forged — imbalanced!
# 2.0 → recall stuck at 0.31 (too low, model predicts mostly Authentic)
# 3.0 → val_accuracy only 32% (too high, model predicts mostly Forged)
# 2.5 → sweet spot: enough to learn forgeries without over-correcting.
print("\n--- Step 2: Computing Class Weights ---")
weight_authentic = 1.0
weight_forged    = 2.5   # Balanced: 2.0 too weak, 3.0 too aggressive
class_weight = {0: weight_authentic, 1: weight_forged}
print(f"  Class weight authentic (0) : {weight_authentic}")
print(f"  Class weight forged    (1) : {weight_forged}")


# ── Step 3: Build model ───────────────────────────────────────────────────────
print("\n--- Step 3: Building Model ---")
model = build_model()
model = compile_model(model)
model.summary()


# ── Step 4: Callbacks ─────────────────────────────────────────────────────────
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
    verbose=1
)

checkpoint = ModelCheckpoint(
    filepath=MODEL_PATH,
    monitor="val_loss",
    save_best_only=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-6,
    verbose=1
)


# ── Step 5: Train ─────────────────────────────────────────────────────────────
print("\n--- Step 4: Training ---")
history = model.fit(
    train_ds,
    epochs=EPOCHS,
    validation_data=val_ds,
    class_weight=class_weight,   # <-- KEY FIX: penalise missed forgeries
    callbacks=[early_stop, checkpoint, reduce_lr],
    verbose=1
)


# ── Step 6: Evaluate on test set ──────────────────────────────────────────────
print("\n--- Step 5: Evaluating on Test Set ---")
results = model.evaluate(test_ds, verbose=0)
test_loss      = results[0]
test_accuracy  = results[1]   # 'accuracy' (BinaryAccuracy)
test_precision = results[2]   # 'precision'
test_recall    = results[3]   # 'recall'
print(f"Test Loss      : {test_loss:.4f}")
print(f"Test Accuracy  : {test_accuracy * 100:.2f}%")
print(f"Test Precision : {test_precision:.4f}")
print(f"Test Recall    : {test_recall:.4f}")


# ── Collect predictions for confusion matrix ──────────────────────────────────
y_true_all = []
y_pred_all = []

for images, labels in test_ds:
    preds = model.predict(images, verbose=0).flatten()
    y_true_all.extend(labels.numpy())
    y_pred_all.extend((preds >= 0.5).astype(int))

print("\nClassification Report:")
print(classification_report(y_true_all, y_pred_all, target_names=["Authentic", "Forged"]))


# ── Step 7: Accuracy & Loss graphs ────────────────────────────────────────────
print("\n--- Step 6: Saving Graphs ---")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"],     label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Val Accuracy")
plt.title("Accuracy over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"],     label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.title("Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("graphs/training_graphs.png")
plt.close()
print("Saved: graphs/training_graphs.png")


# ── Step 8: Confusion Matrix ──────────────────────────────────────────────────
cm = confusion_matrix(y_true_all, y_pred_all)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Authentic", "Forged"],
            yticklabels=["Authentic", "Forged"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig("graphs/confusion_matrix.png")
plt.close()
print("Saved: graphs/confusion_matrix.png")


print("\n=== Training Complete! ===")
print(f"Model saved to: {MODEL_PATH}")
