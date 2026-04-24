# Student Performance Prediction System

**IS 108 – Intelligence System Final Project | SY 2025-2026**

A Business Intelligence application that predicts student academic performance using machine learning algorithms (KNN, SVM, and ANN).

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Navigate to project directory:**

```bash
cd "MIDTERM PROJECT (IS 108)"
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Generate sample dataset:**

```bash
python generate_dataset.py
```

5. **Run the application:**

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📊 Features

✅ **Data Management**

- Import CSV/Excel datasets
- View and explore data statistics
- Automatic missing value handling

✅ **Data Preprocessing**

- Feature scaling and encoding
- Configurable train-test split
- Real-time preprocessing pipeline

✅ **Model Training**

- Train KNN, SVM, and ANN models
- Configure hyperparameters
- Monitor training progress

✅ **Model Evaluation**

- Compare model performance
- View confusion matrices
- Detailed classification reports
- Multiple evaluation metrics

✅ **Predictions**

- Make predictions on new data
- Get results from all three models
- Interactive input interface

## 📂 Project Structure

```
MIDTERM PROJECT (IS 108)/
├── app.py                      # Main Streamlit application
├── generate_dataset.py         # Sample data generator
├── requirements.txt            # Python dependencies
├── PROJECT_REPORT.md          # Complete project documentation
├── README.md                  # This file
├── data/
│   └── student_performance.csv
├── models/
│   ├── __init__.py
│   └── trainer.py             # ML model implementations
└── utils/
    ├── __init__.py
    └── preprocessing.py       # Data preprocessing
```

## 🤖 Models Implemented

### 1. K-Nearest Neighbor (KNN)

- Simple instance-based classifier
- Uses distance metrics to find similar students
- Parameters: n_neighbors=5

### 2. Support Vector Machine (SVM)

- Finds optimal decision boundary
- Uses RBF kernel for non-linear classification
- Parameters: kernel='rbf', C=1.0

### 3. Artificial Neural Network (ANN)

- Deep learning model with 2 hidden layers
- Architecture: 10 → 100 → 50 → 3 neurons
- Uses ReLU activation and early stopping

## 📈 Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: True positive rate among positives
- **Recall**: Ability to find all positives
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Detailed classification breakdown

## 🎯 Business Problem

**Student Performance Prediction** helps educational institutions:

- Identify at-risk students early
- Allocate support resources effectively
- Make data-driven decisions about student intervention
- Improve overall academic outcomes

## 💻 Technology Stack

| Technology       | Purpose              |
| ---------------- | -------------------- |
| **Streamlit**    | Web interface        |
| **Python**       | Programming language |
| **scikit-learn** | Machine learning     |
| **Pandas**       | Data processing      |
| **Plotly**       | Visualizations       |

## 🌐 Deployment

### Deploy to Vercel

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure build settings (defaults work)
4. Deploy!

## 📖 Usage Guide

1. **Home**: Understand the application
2. **Data Upload**: Load your dataset or generate sample data
3. **Data Preprocessing**: Configure and apply preprocessing
4. **Model Training**: Train all three models
5. **Results**: View and compare model performance
6. **Predictions**: Make predictions for new students
7. **Documentation**: Read complete project details

## 📝 Dataset Information

**Features (10 total):**

- Study hours per week
- Attendance percentage
- Previous GPA
- Sleep hours
- Family income level
- Internet speed (Mbps)
- Number of subjects
- Extracurricular activities
- Parental support level
- Motivation level

**Target Variable:**

- Performance: Low, Medium, or High

**Dataset Size:**

- 300 student records
- 80% training / 20% testing

## ✅ Project Requirements Met

- [x] Dataset handling (CSV/Excel import)
- [x] Data preprocessing (missing values, encoding, scaling)
- [x] Predictive modeling workflow
- [x] Three algorithm implementation (KNN, SVM, ANN)
- [x] Model evaluation (accuracy, precision, recall, F1, confusion matrix)
- [x] User-friendly web interface
- [x] Complete documentation
- [x] Deployment ready

## 👥 Team

- Team Member 1: Jean Faith Marie Patula
- Team Member 2: Sean Endriga
- Team Member 3: [Name]

## 📚 References

- Scikit-learn: https://scikit-learn.org/
- Streamlit: https://streamlit.io/
- Plotly: https://plotly.com/

## 📄 License

Educational Project - IS 108 Course

---

**Created:** April 2026  
**Last Updated:** April 25, 2026
