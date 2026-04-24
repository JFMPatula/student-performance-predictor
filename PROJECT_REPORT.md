# Student Performance Prediction System

## IS 108 – Intelligence System Final Project

### SY 2025-2026

---

## 1. PROJECT OVERVIEW

### 1.1 Title

**Student Performance Prediction System using Machine Learning**

### 1.2 Team Members

- [Member 1 Name]
- [Member 2 Name]
- [Member 3 Name]

### 1.3 Project Description

This project develops a Business Intelligence application that predicts student academic performance using three machine learning algorithms: K-Nearest Neighbor (KNN), Support Vector Machine (SVM), and Artificial Neural Network (ANN). The application allows users to upload datasets, preprocess data, train models, compare results, and make predictions through an intuitive web interface.

---

## 2. BUSINESS PROBLEM

### 2.1 Problem Statement

Academic institutions need an effective way to predict student performance to:

- Identify at-risk students early for intervention
- Allocate resources and support programs effectively
- Guide course enrollment and curriculum decisions
- Improve overall student success rates

### 2.2 Problem Justification

Student performance prediction is a critical issue because:

- **Early Intervention:** Identifying students likely to struggle allows for timely support
- **Resource Optimization:** Schools can better allocate tutoring, counseling, and academic support
- **Decision Making:** Students can make informed decisions about course selection and study strategies
- **Institutional Goals:** Schools can work towards improving graduation rates and student outcomes

### 2.3 Expected Outcome

Build a predictive model that accurately classifies students into performance categories (Low, Medium, High) based on their characteristics and past academic behavior.

---

## 3. DATASET INFORMATION

### 3.1 Dataset Description

The dataset contains 300 student records with 10 features related to academic and personal characteristics.

### 3.2 Dataset Features

| Feature                    | Type        | Range/Values | Description                                |
| -------------------------- | ----------- | ------------ | ------------------------------------------ |
| study_hours                | Numerical   | 1-10         | Hours per week spent studying              |
| attendance_percentage      | Numerical   | 50-100       | Percentage of classes attended             |
| previous_gpa               | Numerical   | 1.5-4.0      | GPA from previous semester                 |
| sleep_hours                | Numerical   | 4-10         | Average hours of sleep per night           |
| family_income              | Categorical | 1-5          | Family income level (1=low, 5=high)        |
| internet_speed_mbps        | Numerical   | 1-100        | Internet speed in Mbps                     |
| number_of_subjects         | Numerical   | 4-8          | Number of courses enrolled                 |
| extracurricular_activities | Numerical   | 0-4          | Number of extracurricular activities       |
| parental_support           | Categorical | 1-5          | Level of parental support (1=low, 5=high)  |
| motivation_level           | Categorical | 1-5          | Student's motivation level (1=low, 5=high) |

### 3.3 Target Variable

- **performance**: Student performance level (1=Low, 2=Medium, 3=High)

### 3.4 Data Distribution

- **Total Records:** 300
- **Training Set:** 240 (80%)
- **Testing Set:** 60 (20%)

---

## 4. DATA PREPROCESSING

### 4.1 Missing Value Handling

**Strategy:** Mean/Median Imputation

- Numerical features with missing values are filled with mean values
- Categorical features with missing values are filled with mode values
- The application validates data completeness before model training

### 4.2 Feature Encoding

**Categorical Variable Encoding:**

- Applied Label Encoding to categorical features (family_income, parental_support, motivation_level)
- Converts categorical values to numerical (0, 1, 2, 3, 4)
- Uses consistent encoding across training and testing data

### 4.3 Feature Scaling

**Scaling Method:** StandardScaler (Z-score Normalization)

- Formula: $X_{scaled} = \frac{X - \mu}{\sigma}$
- Ensures all features have mean = 0 and standard deviation = 1
- Essential for KNN and SVM algorithms
- Fitted on training data and applied to test data to prevent data leakage

### 4.4 Train-Test Split

**Approach:** Stratified Split

- Training set: 80% (240 samples)
- Testing set: 20% (60 samples)
- Uses stratification to maintain class distribution
- Random state set to 42 for reproducibility

---

## 5. MACHINE LEARNING ALGORITHMS

### 5.1 K-Nearest Neighbor (KNN)

**Algorithm Overview:**
KNN is an instance-based learning algorithm that classifies a new data point based on the majority class of its k nearest neighbors in the training data.

**How It Works:**

1. Store all training data points
2. For a new point, calculate distances to all training points
3. Select the k closest neighbors
4. Assign the class based on majority vote among neighbors

**Mathematical Basis:**

- Distance Metric: Euclidean Distance
- Formula: $d(p_1, p_2) = \sqrt{\sum_{i=1}^{n}(p_{1i} - p_{2i})^2}$

**Implementation Details:**

- **n_neighbors:** 5
- **Distance Metric:** Euclidean
- **Weights:** Uniform

**Advantages:**

- Simple and easy to understand
- No training phase (lazy learner)
- Good for non-linear data
- Adapts well to local patterns

**Disadvantages:**

- Slow prediction time (must compute distances to all points)
- Sensitive to feature scaling (requires normalization)
- Sensitive to irrelevant features
- High memory requirement for large datasets

**Code Implementation:**

```python
from sklearn.neighbors import KNeighborsClassifier

model_knn = KNeighborsClassifier(n_neighbors=5)
model_knn.fit(X_train, y_train)
predictions = model_knn.predict(X_test)
```

---

### 5.2 Support Vector Machine (SVM)

**Algorithm Overview:**
SVM finds an optimal hyperplane that maximizes the margin between different classes. It can handle both linear and non-linear classification problems.

**How It Works:**

1. Transform data into higher-dimensional space (if needed)
2. Find the hyperplane that maximizes the margin between classes
3. Use kernel trick to handle non-linear boundaries
4. Make predictions based on which side of the hyperplane new points fall

**Mathematical Basis:**

- Objective: Maximize margin = $\frac{2}{\|w\|}$
- Classification: $f(x) = sign(w^T\phi(x) + b)$

**Implementation Details:**

- **Kernel:** RBF (Radial Basis Function)
- **C Parameter:** 1.0 (regularization strength)
- **Probability:** True (enables probability estimates)

**Advantages:**

- Effective in high-dimensional spaces
- Memory efficient (uses subset of training points - support vectors)
- Versatile with different kernel functions
- Works well for both linear and non-linear problems

**Disadvantages:**

- Slower training on large datasets
- Difficult to interpret results
- Requires feature scaling
- Choice of kernel affects performance significantly

**Code Implementation:**

```python
from sklearn.svm import SVC

model_svm = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
model_svm.fit(X_train, y_train)
predictions = model_svm.predict(X_test)
```

---

### 5.3 Artificial Neural Network (ANN)

**Algorithm Overview:**
ANN is a deep learning model inspired by biological neural networks. It consists of interconnected layers of neurons that learn complex patterns through backpropagation.

**Architecture:**

```
Input Layer (10 features)
    ↓
Hidden Layer 1 (100 neurons, ReLU activation)
    ↓
Hidden Layer 2 (50 neurons, ReLU activation)
    ↓
Output Layer (3 neurons, softmax activation)
```

**How It Works:**

1. Forward Pass: Input propagates through layers with weight multiplication and activation
2. Compute Loss: Measure difference between predicted and actual values
3. Backward Pass: Calculate gradients and update weights
4. Repeat: Continue until convergence or max iterations

**Mathematical Basis:**

- Forward Pass: $z^{(l)} = w^{(l)}a^{(l-1)} + b^{(l)}$, $a^{(l)} = \sigma(z^{(l)})$
- Activation: ReLU: $\sigma(x) = max(0, x)$

**Implementation Details:**

- **Hidden Layers:** (100, 50)
- **Activation Function:** ReLU (Rectified Linear Unit)
- **Max Iterations:** 1000
- **Early Stopping:** Enabled with 10% validation split
- **Optimizer:** Adam (adaptive learning rate)

**Advantages:**

- Can learn complex non-linear patterns
- Flexible architecture (easy to modify layers)
- Good for large datasets
- Automatic feature learning

**Disadvantages:**

- Requires more training data
- Longer training time
- Black box nature (hard to interpret)
- Sensitive to hyperparameter choices
- Risk of overfitting

**Code Implementation:**

```python
from sklearn.neural_network import MLPClassifier

model_ann = MLPClassifier(
    hidden_layer_sizes=(100, 50),
    max_iter=1000,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1
)
model_ann.fit(X_train, y_train)
predictions = model_ann.predict(X_test)
```

---

## 6. EVALUATION METRICS

### 6.1 Accuracy

**Definition:** Proportion of correct predictions among total predictions

**Formula:** $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

**Interpretation:**

- Ranges from 0 to 1 (or 0-100%)
- Good for balanced datasets
- Can be misleading with imbalanced data

---

### 6.2 Precision

**Definition:** Proportion of correct positive predictions among all positive predictions

**Formula:** $$\text{Precision} = \frac{TP}{TP + FP}$$

**Interpretation:**

- Answers: "Of all predicted positives, how many are actually positive?"
- Important when false positives are costly

---

### 6.3 Recall (Sensitivity)

**Definition:** Proportion of actual positives correctly identified

**Formula:** $$\text{Recall} = \frac{TP}{TP + FN}$$

**Interpretation:**

- Answers: "Of all actual positives, how many did we find?"
- Important when false negatives are costly

---

### 6.4 F1-Score

**Definition:** Harmonic mean of precision and recall

**Formula:** $$F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**Interpretation:**

- Balanced metric that considers both precision and recall
- Range: 0 to 1 (higher is better)
- Useful for imbalanced datasets

---

### 6.5 Confusion Matrix

**Definition:** Table showing true/false positives and negatives

**Structure:**

```
                 Predicted Low    Predicted Medium    Predicted High
Actual Low              TN               FP                  FP
Actual Medium           FN               TP                  FP
Actual High             FN               FN                  TP
```

**Interpretation:**

- Diagonal elements = correct predictions
- Off-diagonal elements = misclassifications
- Helps identify which classes are confused

---

## 7. MODEL COMPARISON & RESULTS

### 7.1 Performance Metrics Summary

[This section will be populated with actual results after model training]

| Model | Accuracy | Precision | Recall  | F1-Score |
| ----- | -------- | --------- | ------- | -------- |
| KNN   | [Value]  | [Value]   | [Value] | [Value]  |
| SVM   | [Value]  | [Value]   | [Value] | [Value]  |
| ANN   | [Value]  | [Value]   | [Value] | [Value]  |

### 7.2 Model Comparison Analysis

**Strengths and Weaknesses:**

**KNN:**

- Best for: [To be determined based on results]
- Weaknesses: [To be determined based on results]

**SVM:**

- Best for: [To be determined based on results]
- Weaknesses: [To be determined based on results]

**ANN:**

- Best for: [To be determined based on results]
- Weaknesses: [To be determined based on results]

### 7.3 Best Performing Model

[To be determined based on evaluation results]

---

## 8. APPLICATION FEATURES

### 8.1 User Interface Components

**Home Page:**

- Project overview
- Quick statistics
- Navigation guide

**Data Upload:**

- CSV/Excel file support
- Dataset preview
- Basic statistics display
- Sample dataset generation option

**Data Preprocessing:**

- Missing value handling
- Feature encoding
- Train-test split configuration
- Data transformation visualization

**Model Training:**

- Hyperparameter configuration
- Real-time training progress
- Model comparison dashboard

**Results & Comparison:**

- Detailed metrics display
- Confusion matrices visualization
- Model performance charts
- Classification reports

**Make Predictions:**

- Interactive input form
- Real-time predictions from all three models
- Prediction explanation

**Documentation:**

- Complete project documentation
- Algorithm explanations
- Usage instructions

### 8.2 Technology Stack

| Component        | Technology    |
| ---------------- | ------------- |
| Web Framework    | Streamlit     |
| Data Processing  | Pandas, NumPy |
| Machine Learning | scikit-learn  |
| Visualization    | Plotly        |
| Language         | Python 3.x    |
| Deployment       | Vercel        |

---

## 9. INSTALLATION & USAGE GUIDE

### 9.1 System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection

### 9.2 Local Installation

**Step 1: Clone/Extract Project**

```bash
cd "MIDTERM PROJECT (IS 108)"
```

**Step 2: Create Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

**Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Generate Sample Dataset**

```bash
python generate_dataset.py
```

**Step 5: Run Application**

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 9.3 Vercel Deployment

**Step 1: Push to GitHub**

- Create repository
- Push code to GitHub

**Step 2: Connect to Vercel**

- Visit vercel.com and sign in
- Click "New Project"
- Select your GitHub repository

**Step 3: Configure Settings**

- Build Command: Leave blank
- Output Directory: Leave blank
- Environment Variables: None needed

**Step 4: Deploy**

- Click "Deploy"
- Vercel will automatically build and deploy

---

## 10. CONCLUSIONS & RECOMMENDATIONS

### 10.1 Key Findings

[To be populated after results are available]

### 10.2 Recommendations

1. **Model Selection:**
   - Use [Best Model] for production deployment
   - Reasoning: [Explain why based on metrics]

2. **Data Collection:**
   - Collect more diverse student data from multiple institutions
   - Include additional features like study environment, technology access
   - Maintain balanced distribution across performance levels

3. **Feature Engineering:**
   - Explore interaction terms between features
   - Consider temporal features (semester, term)
   - Create derived features from existing ones

4. **Hyperparameter Tuning:**
   - Use GridSearchCV for systematic optimization
   - Implement cross-validation (k-fold)
   - Monitor for overfitting

5. **Model Improvement:**
   - Experiment with ensemble methods (Random Forest, Gradient Boosting)
   - Use class weights for imbalanced data
   - Implement regularization techniques

6. **Real-World Application:**
   - Test with actual student data
   - Get feedback from educational institutions
   - Consider privacy and ethical implications
   - Develop explainability features for model decisions

### 10.3 Future Enhancements

- Multi-class classification with more granular performance levels
- Time-series analysis for performance trends
- Integration with student information systems
- Automated intervention recommendations
- Mobile application development

---

## 11. REFERENCES

1. Scikit-learn Documentation: https://scikit-learn.org/
2. Streamlit Documentation: https://docs.streamlit.io/
3. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning
4. Bishop, C. M. (2006). Pattern Recognition and Machine Learning
5. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning

---

## 12. APPENDICES

### Appendix A: Code Files

- `app.py` - Main Streamlit application
- `generate_dataset.py` - Dataset generation script
- `utils/preprocessing.py` - Data preprocessing module
- `models/trainer.py` - Machine learning models module

### Appendix B: Project Structure

```
MIDTERM PROJECT (IS 108)/
├── app.py                     # Main application
├── generate_dataset.py        # Dataset generation
├── requirements.txt           # Dependencies
├── PROJECT_REPORT.md         # This document
├── data/
│   └── student_performance.csv
├── models/
│   ├── __init__.py
│   └── trainer.py
├── utils/
│   ├── __init__.py
│   └── preprocessing.py
└── README.md                 # Quick start guide
```

---

**Project Completed:** April 25, 2026  
**Team Members:** [To be filled]  
**Submitted to:** IS 108 - Intelligence System Course  
**Academic Year:** SY 2025-2026
