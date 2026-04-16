## **📅 30-Day AIML Execution Plan**

---

## **PHASE 1 — Foundations & Learning (Days 1–7)**


### **🎯 Goal**

Reach _minimum working confidence_ in CNNs and inference pipelines.

---

### **Days 1–2: Orientation & Setup**

  

**Tasks**

- Clone GitHub repository
    
- Create AIML branch
    
- Install Python, PyTorch, FastAPI
    
- Understand full system flow:

- Environment fully working
    
- Clear understanding of project scope
    
- Notes on model choice
    

---

### **Days 3–5: Core Learning (Focused Only)**

  

**Learn ONLY the following:**

- Python basics (functions, loops, file I/O)
    
- PyTorch basics:
    
    - Dataset
        
    - DataLoader
        
    - Model loading
        
    - Training loop
        
    
- Transfer Learning:
    
    - Load pretrained ResNet/EfficientNet
        
    - Replace final classification layer
        
    
- Image preprocessing:
    
    - Resize
        
    - Normalize
        
    
- Dataset handling using ImageFolder
    

  

**Target Outcome**

- Able to fine-tune a pretrained CNN
    
- Able to run inference on a single image
    

---

### **Days 6–7: Mini Practice Build**

  

**Tasks**

- Train a **small CNN** on a sample dataset
    
- Save trained model (.pt file)
    
- Write a script to:
    
    - Load model
        
    - Input one image
        
    - Output prediction + confidence
        
    

  

**Deliverables**

- Working offline inference script
    
- Saved model file
    
- Training notebook/script
    

---

## **PHASE 2 — Core Build (Days 8–15)**

  

### **🎯 Goal**

  

Achieve a **fully working ML-backed MVP**.

---

### **Days 8–9: Backend + Model Integration**

  

**Tasks**

- Build FastAPI backend
    
- Load trained model at startup
    
- Create /infer endpoint:
    
    - Accept image
        
    - Run preprocessing
        
    - Return label + confidence
        
    

  

**Deliverables**

- API returns valid predictions
    
- Backend stable and responsive
    

---

### **Days 10–11: Dataset Expansion & Improved Training**

  

**Tasks**

- Expand dataset (real vs forged images)
    
- Apply augmentations:
    
    - Flip
        
    - Rotation
        
    - Color jitter
        
    
- Retrain model
    
- Track accuracy and loss
    

  

**Deliverables**

- Improved model (.pt)
    
- Accuracy better than initial baseline
    
- Training logs saved
    

---

### **Days 12–13: Model Validation Support**

  

**Tasks**

- Verify prediction consistency
    
- Check false positives/negatives
    
- Adjust threshold if required
    

  

**Deliverables**

- Reliable inference behavior
    
- Notes on model behavior
    

---

### **Days 14–15: MVP Freeze**

  

**Tasks**

- Finalize model version
    
- Lock architecture
    
- Test end-to-end with frontend
    

  

**Deliverable**

- Stable ML inference pipeline
    
- No breaking changes after this point
    

---

## **PHASE 3 — Advanced Features & Quality (Days 16–23)**

  

### **🎯 Goal**

  

Turn the project into a **judge-worthy system**.

---

### **Days 16–17: Grad-CAM (Explainable AI)**

  

**Tasks**

- Implement Grad-CAM
    
- Generate heatmap highlighting manipulated regions
    
- Save heatmap image
    

  

**Deliverables**

- Heatmap image per inference
    
- Explainable AI output (major evaluation advantage)
    

---

### **Days 18–19: Metadata (EXIF) Analysis**

  

**Tasks**

- Extract EXIF metadata:
    
    - Camera model
        
    - Software used
        
    - Timestamp
        
    
- Flag suspicious patterns (missing or altered metadata)
    

  

**Deliverables**

- Metadata extraction logic
    
- Suspicion indicators
    

---

### **Days 20–21: Evaluation & Metrics**

  

**Tasks**

- Generate:
    
    - Confusion matrix
        
    - Precision
        
    - Recall
        
    - F1-score
        
    - ROC curve
        
    
- Store results for presentation
    

  

**Deliverables**

- Evaluation plots
    
- Metrics summary table
    

---

### **Days 22–23: Bonus Feature (Choose ONE)**

  

Choose **one only**:

- Patch-based forgery localization
    
- Batch image inference
    
- PDF report generation
    
- Demo mode (preloaded examples)
    

  

**Deliverable**

- One clearly documented differentiator
    

---

## **PHASE 4 — Testing, Polish & Presentation (Days 24–30)**

  

### **🎯 Goal**

  

Maximum marks. Zero surprises.

---

### **Days 24–25: Robustness Testing**

  

**Tasks**

- Handle:
    
    - Corrupted images
        
    - Unsupported formats
        
    - Empty uploads
        
    
- Improve error responses
    

---

### **Days 26–27: Documentation**

  

**Tasks**

- Write:
    
    - Model explanation
        
    - Dataset description
        
    - Training pipeline
        
    - Limitations
        
    

  

**Deliverable**

- Clear README ML section
    

---

### **Days 28–29: Presentation Prep**

  

**Tasks**

- Prepare explanation for:
    
    - Model choice
        
    - Training strategy
        
    - Explainability
        
    - Metrics
        
    - Limitations
        
    

---

### **Day 30: Final Review**

  

**Tasks**

- Live demo rehearsal
    
- Backup demo video
    
- Final model tag in GitHub


## **🚫 What NOT To Do**

- Do not train custom CNNs from scratch
    
- Do not chase SOTA accuracy
    
- Do not change models late
    
- Do not skip evaluation metrics
    

---

## **✅ What Judges Care About**

- Working system
    
- Explainable decisions
    
- Clear metrics
    
- Honest limitations
    
- Confident explanation