# evaluate.py
# -----------
# Standalone script to evaluate a saved model on the test set.
# Produces: Classification Report, Confusion Matrix, ROC-AUC curve.
# Run: python evaluate.py

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import tensorflow as tf
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score
)

from dataset_loader import load_datasets

# ── Settings ──────────────────────────────────────────
MODEL_PATH = "model.keras"
os.makedirs("graphs", exist_ok=True)
# ──────────────────────────────────────────────────────


def evaluate():
    # ── Step 1: Check model exists ────────────────────
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at '{MODEL_PATH}'")
        print("Please run: python train.py")
        return

    # ── Step 2: Load model ────────────────────────────
    print(f"\nLoading model from '{MODEL_PATH}'...")
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.\n")

    # ── Step 3: Load test dataset ─────────────────────
    print("Loading test dataset...")
    _, test_ds = load_datasets()
    print("Dataset loaded.\n")

    # ── Step 4: Collect predictions ───────────────────
    print("Running predictions on test set...")
    y_true_all  = []
    y_pred_probs = []

    for images, labels in test_ds:
        preds = model.predict(images, verbose=0).flatten()
        y_true_all.extend(labels.numpy())
        y_pred_probs.extend(preds)

    y_true_all   = np.array(y_true_all)
    y_pred_probs = np.array(y_pred_probs)
    y_pred_labels = (y_pred_probs >= 0.5).astype(int)

    # ── Step 5: Classification Report ─────────────────
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(
        y_true_all, y_pred_labels,
        target_names=["Authentic", "Forged"]
    ))

    # ── Step 6: Confusion Matrix ──────────────────────
    cm = confusion_matrix(y_true_all, y_pred_labels)
    tn, fp, fn, tp = cm.ravel()
    print(f"True Negatives  (Auth predicted Auth)  : {tn}")
    print(f"False Positives (Auth predicted Forged): {fp}")
    print(f"False Negatives (Forged predicted Auth): {fn}")
    print(f"True Positives  (Forged predicted Forged): {tp}")

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
    print("\nSaved: graphs/confusion_matrix.png")

    # ── Step 7: ROC Curve ─────────────────────────────
    fpr, tpr, _ = roc_curve(y_true_all, y_pred_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="steelblue", lw=2,
             label=f"ROC Curve (AUC = {roc_auc:.4f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Random Baseline")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graphs/roc_curve.png")
    plt.close()
    print("Saved: graphs/roc_curve.png")
    print(f"ROC AUC Score: {roc_auc:.4f}")

    # ── Step 8: Precision-Recall Curve ────────────────
    precision, recall, _ = precision_recall_curve(y_true_all, y_pred_probs)
    ap_score = average_precision_score(y_true_all, y_pred_probs)

    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, color="darkorange", lw=2,
             label=f"PR Curve (AP = {ap_score:.4f})")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graphs/pr_curve.png")
    plt.close()
    print("Saved: graphs/pr_curve.png")
    print(f"Average Precision Score: {ap_score:.4f}")

    # ── Summary ───────────────────────────────────────
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print(f"  graphs/confusion_matrix.png")
    print(f"  graphs/roc_curve.png")
    print(f"  graphs/pr_curve.png")
    print("="*60 + "\n")


if __name__ == "__main__":
    evaluate()
