• Technology Used: Python, Deep Learning (ResUNet)
• Description: Developed a ResUNet-based segmentation 
model with Dice loss to detect liver tumors from CT 
scans, automating image analysis to improve accuracy 
and reduce radiologist workload by reducing 1 hour per 
case to under 2 minutes

## Liver Tumor Segmentation using U-Net

This project presents a **robust deep learning model** for medical image segmentation, specifically focused on the **delineation of liver tumors in CT scans**. The model is based on the **U-Net architecture**, a well-established framework for biomedical image segmentation.

### Dataset

The study utilizes the **3DIRCADb dataset**, curated from Kaggle, and introduces a **custom data generator** to enable efficient data loading and preprocessing.

### Objective

The primary goal is to enhance the **accuracy and precision** of liver tumor segmentation, which is crucial for **diagnosis** and **treatment planning** in the field of medical imaging.

### Evaluation Metrics

The model performance was evaluated using multiple metrics:

* **Pixel Accuracy:** 26.58%
* **True Positive Accuracy:** 99.68%
* **Dice Coefficient:** 0.89

Additionally, a **confusion matrix analysis** provides detailed insights into the classification outcomes.

### Key Findings

* The model effectively handles the **binary classification task** of distinguishing between *Malignant* and *Benign* tumors.
* Achieves a **high true positive rate**, ensuring that most tumors are correctly identified.
* Maintains a **low false negative rate**, minimizing the risk of missed tumor detections.

### Contribution

This research contributes to the advancement of **medical image segmentation techniques**, offering clinicians a valuable tool for the **accurate detection and delineation of liver tumors**.

