# 🚀 Quick Start Guide - Student Performance Prediction System

## Setup Instructions (5 minutes)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Generate Sample Dataset (Optional)

```bash
python generate_dataset.py
```

This creates `data/student_performance.csv` with 300 sample student records.

### 3️⃣ Run the Application

```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501**

---

## 📋 Step-by-Step Usage

### Step 1: Load Data

- Go to **📁 Data Upload** page
- Click **"Generate Sample Student Dataset"** button
- OR upload your own CSV/Excel file

### Step 2: Preprocess Data

- Go to **🔧 Data Preprocessing** page
- Select target column (should be "performance")
- Choose missing value strategy
- Set train/test split ratio
- Click **"Apply Preprocessing"** button

### Step 3: Train Models

- Go to **🤖 Model Training** page
- Review default hyperparameters
- Click **"Train All Models"** button
- Wait for training to complete

### Step 4: View Results

- Go to **📈 Results & Comparison** page
- See model metrics and comparison charts
- View confusion matrices for each model
- Read detailed classification reports

### Step 5: Make Predictions

- Go to **🔮 Make Predictions** page
- Enter student characteristics
- Click **"Predict Performance"** button
- Get predictions from all three models

### Step 6: Read Documentation

- Go to **📄 Documentation** page
- Learn about algorithms and methodology
- Review technical details

---

## 🎯 Dataset Features

The sample dataset includes:

- **10 Input Features** about students
- **1 Target Variable** (Performance: Low/Medium/High)
- **300 Student Records**

**Features:**

1. Study hours (1-10 hours/week)
2. Attendance percentage (50-100%)
3. Previous GPA (1.5-4.0)
4. Sleep hours (4-10 hours/night)
5. Family income level (1-5)
6. Internet speed (1-100 Mbps)
7. Number of subjects (4-8)
8. Extracurricular activities (0-4)
9. Parental support (1-5)
10. Motivation level (1-5)

---

## 🤖 Three ML Algorithms

### 1. K-Nearest Neighbor (KNN)

- Simple and interpretable
- Good for student clustering patterns
- Default: k=5 neighbors

### 2. Support Vector Machine (SVM)

- Powerful for classification
- Finds optimal decision boundaries
- Default: RBF kernel, C=1.0

### 3. Artificial Neural Network (ANN)

- Deep learning model
- Captures complex patterns
- Default: 2 hidden layers (100, 50 neurons)

---

## 📊 Performance Metrics

Each model is evaluated on:

- **Accuracy** - Overall correctness
- **Precision** - Correctness of positive predictions
- **Recall** - Ability to find all positives
- **F1-Score** - Balanced metric
- **Confusion Matrix** - Detailed classification breakdown

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**

```bash
pip install streamlit pandas numpy scikit-learn plotly openpyxl
```

### Issue: Dataset not found

**Solution:**

```bash
python generate_dataset.py
```

### Issue: App won't start

**Solution:**

```bash
streamlit run app.py --logger.level=debug
```

### Issue: Slow performance

- Close other applications
- Reduce dataset size
- Restart the terminal

---

## 📁 Project Files

```
MIDTERM PROJECT (IS 108)/
├── app.py                          ← Main application (RUN THIS)
├── generate_dataset.py             ← Generate sample data
├── requirements.txt                ← Dependencies
├── README.md                       ← Overview
├── PROJECT_REPORT.md              ← Complete documentation
├── QUICK_START.md                 ← This file
├── data/
│   └── student_performance.csv    ← Sample dataset
├── models/
│   └── trainer.py                 ← ML model implementations
└── utils/
    └── preprocessing.py           ← Data preprocessing
```

---

## 💡 Tips & Tricks

1. **First Time?** Start with "Generate Sample Dataset"
2. **Custom Data?** Upload CSV with same column names
3. **Slow Training?** Reduce "Hidden Layer Sizes" in ANN
4. **Better Results?** Use more training data

---

## 🎓 Project Requirements Met

✅ Dataset handling (CSV/Excel import)  
✅ Data preprocessing (missing values, encoding, scaling)  
✅ Predictive modeling workflow  
✅ Three algorithms (KNN, SVM, ANN)  
✅ Model evaluation (accuracy, precision, recall, F1, confusion matrix)  
✅ User-friendly web interface  
✅ Complete documentation  
✅ Deployment ready

---

## 🌐 Deploy to Vercel

1. Push code to GitHub
2. Go to vercel.com
3. Import your repository
4. Click Deploy!

---

**Ready to start?** Run: `streamlit run app.py`

Need help? Check PROJECT_REPORT.md for detailed information!
