# Image Forgery Detection — ML Module

A CNN-based image forgery detection system trained on the **CASIA v2 dataset**.
Built from scratch using TensorFlow/Keras. Beginner-friendly and designed for Django integration.

---

## ⬇️ Downloads

> **Large files are hosted on Google Drive** (too big for GitHub).

| File | Size | Link |
|------|------|------|
| `model.keras` (trained weights) | ~101 MB | [📥 Download](https://drive.google.com/file/d/1CkuTFXcrLjXrVraoWDXFuioTQEIk-DE6/view?usp=sharing) |

After downloading, place the files in the project root:
```
Image_forgery_detection/
├── model.keras        ← place here
├── dataset/           ← place here
│   └── dataset/
│       ├── authentic/
│       └── forged/
└── ...
```

---

## 📁 Project Structure

```
Image_forgery_detection/
│
├── dataset/
│   └── dataset/
│       ├── authentic/    ← real images (label 0)
│       └── forged/       ← forged images (label 1)
│
├── graphs/               ← training graphs saved here
│
├── dataset_loader.py     ← load, normalize, split, augment data
├── model.py              ← CNN architecture (4 conv blocks)
├── train.py              ← training pipeline with callbacks + graphs
├── predict.py            ← Django-ready prediction API
├── evaluate.py           ← standalone evaluation with full metrics
└── README.md
```

---

## 🏗️ CNN Architecture

```
Input (128×128×3)
    ↓
[Conv2D(32)  → BatchNorm → ReLU → MaxPool → Dropout(0.25)]  Block 1
    ↓
[Conv2D(64)  → BatchNorm → ReLU → MaxPool → Dropout(0.25)]  Block 2
    ↓
[Conv2D(128) → BatchNorm → ReLU → MaxPool → Dropout(0.30)]  Block 3
    ↓
[Conv2D(256) → BatchNorm → ReLU → MaxPool → Dropout(0.30)]  Block 4
    ↓
Flatten → Dense(512) → BatchNorm → ReLU → Dropout(0.50)
    ↓
Dense(128) → BatchNorm → ReLU → Dropout(0.40)
    ↓
Dense(1, Sigmoid)  →  0 = Authentic | 1 = Forged
```

---

## ⚙️ Training Configuration

| Setting       | Value                     |
|---------------|---------------------------|
| Loss          | Binary Crossentropy        |
| Optimizer     | Adam (lr=0.001)           |
| Epochs        | 35 max (EarlyStopping)    |
| Batch Size    | 32                        |
| Image Size    | 128×128                   |
| Split         | 80% train / 20% test      |
| Class Weight  | 1.0 (Authentic) / 3.0 (Forged) |

**Callbacks:**
- `EarlyStopping` (patience=5, monitor=val_loss)
- `ModelCheckpoint` (saves best model as `model.keras`)
- `ReduceLROnPlateau` (factor=0.5, patience=2, min_lr=1e-6)

---

## 🚀 How to Run

```bash
# Step 1: Clone the repository
git clone https://github.com/guptakartike/image-forgery-detection.git
cd image-forgery-detection

# Step 2: Activate virtual environment
python -m venv venv
venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Download model.keras and dataset/ from the links above
# Place them in the project root directory

# Step 5: Predict on an image (uses pre-trained model.keras)
python predict.py path/to/image.jpg

# Step 6: (Optional) Re-train from scratch
python train.py

# Step 7: (Optional) Evaluate the saved model
python evaluate.py
```

---

## 🔍 Django Integration

```python
from predict import predict_image

# In your Django view:
result = predict_image(request.FILES['image'].temporary_file_path())
# Returns: {"label": "Forged", "confidence": 93.42, "raw_prediction": 0.9342}
```

---

## 📊 Output Graphs (saved to `graphs/`)

| File                    | Description                        |
|-------------------------|------------------------------------|
| `training_graphs.png`   | Train vs Val Accuracy & Loss       |
| `confusion_matrix.png`  | TP/TN/FP/FN heatmap                |

---

## 🛡️ Anti-Overfitting Techniques

| Technique              | Applied In                         |
|------------------------|------------------------------------|
| Dropout (0.25–0.50)    | Every Conv block + Dense layers   |
| BatchNormalization     | Every Conv block + Dense layers   |
| Data Augmentation      | Training set only                 |
| EarlyStopping          | Training callbacks                |
| Class Weights (1:3)    | `model.fit(class_weight=...)`     |

---

## 📋 Dataset

- **CASIA v2**: 7,492 authentic + 5,125 forged images
- Labels assigned alphabetically: `authentic=0`, `forged=1`
- Pixel values normalized: `[0, 255] → [0.0, 1.0]`

---

## 📝 Notes

- `model.keras` is **not included in this repo** due to GitHub's 100 MB file size limit — download it from the [Downloads](#️-downloads) section above.
- The trained model uses class weights `1.0 (Authentic) / 3.0 (Forged)` to handle dataset imbalance.