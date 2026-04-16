# **Skeleton**


## **Project Title**
**Image Forgery Detection System using Deep Learning**



 ## **Problem Statement**
 
With the rapid rise of image manipulation tools and deepfake technology, forged images are increasingly used to spread misinformation and fraud. There is a strong need for an automated system that can accurately identify whether an image is authentic or manipulated.

This project aims to build a web-based application that detects forged images using deep learning techniques and presents the results in a clear, user-friendly manner.

---

## **Objectives**

- Detect whether an uploaded image is **real or forged**
    
- Provide a **confidence score** for predictions
    
- Optionally highlight **tampered regions**
    
- Deliver results through a **simple web interface**
    
- Keep the system lightweight and beginner-friendly
    

---

## **Scope of the Project**

- Image-level forgery detection (initial phase)
    
- Supports common image formats (JPEG, PNG)
    
- Uses a pre-trained deep learning model
    
- Web-based deployment for easy access
    

---

## **Tech Stack**

  

### **Frontend**

- HTML, CSS, JavaScript
    
- React (optional)
    


### **Backend**

- Python
    
- Flask / FastAPI
    

  

### **Machine Learning**

- Python
    
- TensorFlow / PyTorch
    
- OpenCV, NumPy
    
- Pre-trained CNN (EfficientNet / ResNet)
    

  

### **Tools**

- Git & GitHub
    
- Google Colab (training)
    
- VS Code
    

---

## **System Architecture**

  

_(Refer to Architecture Diagram below)_

---

## **Workflow**

1. User uploads an image via web interface
    
2. Backend validates and preprocesses the image
    
3. Image is passed to the trained ML model
    
4. Model predicts authenticity
    
5. Results are returned to frontend
    
6. User views prediction and confidence score
    

---

## **Dataset**

- CASIA Image Tampering Dataset
    
- FaceForensics++ (optional)
    

---

## **Model Details**

- CNN-based binary classifier
    
- Input: Preprocessed image
    
- Output: Real / Forged + probability