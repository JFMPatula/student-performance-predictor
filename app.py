"""
🎓 Streamlit App — Student Performance Prediction
Business Intelligence - Predictive Modeling Application
"""

import os
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ===============================================================
# 🧩 Imports and Path Setup
# ===============================================================

sys.path.insert(0, str(Path(__file__).parent))

from utils.preprocessing import DataPreprocessor
from models.trainer import ModelTrainer

# ===============================================================
# ⚙️ Page Configuration
# ===============================================================

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================================
# 🎨 Custom CSS
# ===============================================================

st.markdown(
    """
    <style>
        .main { padding-top: 2rem; }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================================================
# 💾 Initialize Session State
# ===============================================================

for key, default in {
    'data': None,
    'preprocessor': None,
    'trainer': None,
    'models_trained': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ===============================================================
# 🧭 Sidebar Navigation
# ===============================================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    [
        "🏠 Home",
        "📁 Data Upload",
        "🔧 Data Preprocessing",
        "🤖 Model Training",
        "📈 Results & Comparison",
        "🔮 Make Predictions",
        "📄 Documentation"
    ]
)

# ===============================================================
# 🏠 HOME PAGE
# ===============================================================

if page == "🏠 Home":
    st.title("🎓 Student Performance Prediction System")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            ### Welcome to the Business Intelligence Predictive Modeling Application

            This tool predicts **student academic performance** using machine learning models.

            **Project Overview:**
            - **Goal:** Predict student performance levels (Low, Medium, High)
            - **Algorithms:** KNN, SVM, ANN
            - **Data:** Academic and personal features

            **Key Features:**
            ✅ Upload datasets  
            ✅ Preprocess and clean data  
            ✅ Train and compare multiple models  
            ✅ Generate predictions for new students  

            **How to Use:**
            1. Upload data
            2. Preprocess and split dataset
            3. Train models
            4. View results & metrics
            5. Predict new records
            """
        )

    with col2:
        st.info(
            """
            ### Quick Stats
            - **Models:** 3 (KNN, SVM, ANN)
            - **Metrics:** 4 (Accuracy, Precision, Recall, F1)
            - **Status:** Ready to start
            """
        )

    st.markdown("---")
    st.markdown("### 📚 Dataset Sample")
    st.markdown("Example features: study hours, attendance, GPA, sleep hours, etc.")

# ===============================================================
# 📁 DATA UPLOAD
# ===============================================================

elif page == "📁 Data Upload":
    st.title("📁 Data Upload & Exploration")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    # ---- Upload File ----
    with col1:
        st.subheader("Upload Your Dataset")
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file", type=["csv", "xlsx", "xls"]
        )

        if uploaded_file:
            try:
                preprocessor = DataPreprocessor()
                st.session_state.data = preprocessor.load_data(uploaded_file)
                st.session_state.preprocessor = preprocessor

                st.success("✅ Dataset loaded successfully!")

                st.subheader("Dataset Preview")
                st.dataframe(st.session_state.data.head(10), use_container_width=True)

                st.subheader("Dataset Statistics")
                st.write(st.session_state.data.describe())

            except Exception as e:
                st.error(f"❌ Error loading file: {e}")

    # ---- Dataset Info ----
    with col2:
        if st.session_state.data is not None:
            info = st.session_state.preprocessor.get_dataset_info(st.session_state.data)
            st.subheader("Dataset Info")

            st.metric("Records", info['shape'][0])
            st.metric("Features", info['shape'][1])
            st.metric("Missing Values", sum(info['missing_values'].values()))

            st.markdown("**Columns:**")
            for col in info['columns']:
                st.write(f"• {col}")

    # ---- Sample Dataset ----
    st.markdown("---")
    st.subheader("🔽 Or Use Sample Dataset")

    if st.button("Generate Sample Student Dataset"):
        try:
            import subprocess

            subprocess.run(
                [sys.executable, "generate_dataset.py"],
                cwd=str(Path(__file__).parent),
                check=True,
            )

            data_path = Path(__file__).parent / "data" / "student_performance.csv"
            if data_path.exists():
                preprocessor = DataPreprocessor()
                st.session_state.data = preprocessor.load_data(data_path)
                st.session_state.preprocessor = preprocessor
                st.success("✅ Sample dataset generated and loaded!")
                st.rerun()
            else:
                st.error("❌ Generated dataset not found.")
        except Exception as e:
            st.error(f"❌ Error generating sample dataset: {e}")

# ===============================================================
# 🔧 DATA PREPROCESSING
# ===============================================================

elif page == "🔧 Data Preprocessing":
    st.title("🔧 Data Preprocessing")
    st.markdown("---")

    if st.session_state.data is None or st.session_state.preprocessor is None:
        st.warning("⚠️ Please upload or generate a dataset first.")
    else:
        preprocessor = st.session_state.preprocessor
        df = st.session_state.data

        col1, col2 = st.columns(2)

        # ---- Missing Values ----
        with col1:
            st.subheader("Missing Values")
            missing = preprocessor.get_dataset_info(df)['missing_values']
            n_missing = sum(missing.values())
            if n_missing:
                st.warning(f"Found {n_missing} missing values")
                st.write(missing)
            else:
                st.success("✅ No missing values found")

        # ---- Data Types ----
        with col2:
            info = preprocessor.get_dataset_info(df)
            st.subheader("Data Types")
            st.write(f"**Numeric:** {len(info['numeric_columns'])}")
            st.write(f"**Categorical:** {len(info['categorical_columns'])}")

        st.markdown("---")

        # ---- Target Variable ----
        st.subheader("Target Variable Selection")
        target_column = st.selectbox(
            "Select target column (to predict):",
            df.columns,
            index=df.columns.get_loc("performance")
            if "performance" in df.columns
            else 0,
        )

        # ---- Options ----
        st.subheader("Preprocessing Options")
        missing_strategy = st.radio("Missing values strategy:", ["mean", "median"])
        test_size = st.slider("Test set size (%):", 10, 40, 20) / 100

        # ---- Apply ----
        if st.button("🔄 Apply Preprocessing", type="primary"):
            try:
                preprocessor.test_size = test_size
                X_train, X_test, y_train, y_test = preprocessor.preprocess(
                    df, target_column=target_column
                )

                st.session_state.preprocessor = preprocessor
                st.session_state.models_trained = False

                st.success("✅ Data preprocessing completed!")

                # Split info
                split_info = preprocessor.get_split_info()
                col1, col2, col3 = st.columns(3)
                col1.metric("Training Samples", split_info['train_size'])
                col2.metric("Testing Samples", split_info['test_size'])
                col3.metric("Total Samples", split_info['total_size'])

                st.subheader("Training Set Preview")
                st.dataframe(X_train.head(10), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error during preprocessing: {e}")

# ===============================================================
# 🤖 MODEL TRAINING
# ===============================================================

elif page == "🤖 Model Training":
    st.title("🤖 Model Training")
    st.markdown("---")

    preprocessor = st.session_state.preprocessor

    if preprocessor is None or preprocessor.X_train is None:
        st.warning("⚠️ Please preprocess your dataset first.")
    else:
        st.subheader("Hyperparameter Configuration")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**KNN Configuration**")
            knn_neighbors = st.slider("Number of Neighbors (K):", 3, 15, 5)
        with col2:
            st.markdown("**SVM Configuration**")
            svm_kernel = st.selectbox("Kernel Type:", ["rbf", "linear", "poly"])
            svm_c = st.slider("C Parameter:", 0.1, 10.0, 1.0)
        with col3:
            st.markdown("**ANN Configuration**")
            ann_layers = st.multiselect(
                "Hidden Layer Sizes:",
                [50, 100, 150, 200],
                default=[100, 50]
            )

        st.markdown("---")

        if st.button("🚀 Train All Models", type="primary", use_container_width=True):
            with st.spinner("Training models... This may take a moment."):
                try:
                    trainer = ModelTrainer()

                    # Train KNN
                    st.write("🔄 Training KNN...")
                    trainer.train_knn(
                        preprocessor.X_train, 
                        preprocessor.y_train, 
                        n_neighbors=knn_neighbors
                    )

                    # Train SVM
                    st.write("🔄 Training SVM...")
                    trainer.train_svm(
                        preprocessor.X_train, 
                        preprocessor.y_train, 
                        kernel=svm_kernel,  # type: ignore[arg-type]
                        C=svm_c
                    )

                    # Train ANN
                    st.write("🔄 Training ANN...")
                    ann_tuple = tuple(ann_layers) if ann_layers else (100, 50)
                    trainer.train_ann(
                        preprocessor.X_train, 
                        preprocessor.y_train, 
                        hidden_layers=ann_tuple
                    )

                    # Evaluate all models
                    st.write("📊 Evaluating models...")
                    trainer.evaluate_all_models(preprocessor.X_test, preprocessor.y_test)

                    st.session_state.trainer = trainer
                    st.session_state.models_trained = True

                    st.success("✅ All models trained and evaluated successfully!")

                    # Quick summary
                    st.subheader("Quick Performance Overview")
                    st.dataframe(trainer.compare_models(), use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error during training: {e}")
                    st.exception(e)

# ===============================================================
# 📈 RESULTS & COMPARISON
# ===============================================================

elif page == "📈 Results & Comparison":
    st.title("📈 Results & Model Comparison")
    st.markdown("---")

    trainer = st.session_state.trainer

    if not st.session_state.models_trained or trainer is None:
        st.warning("⚠️ Please train models first.")
    else:
        st.subheader("📊 Model Comparison")

        comparison_df = trainer.compare_models()
        st.dataframe(comparison_df, use_container_width=True)

        fig = go.Figure()
        for _, row in comparison_df.iterrows():
            fig.add_trace(
                go.Bar(
                    x=["Accuracy", "Precision", "Recall", "F1-Score"],
                    y=[row["Accuracy"], row["Precision"], row["Recall"], row["F1-Score"]],
                    name=row["Model"],
                )
            )

        fig.update_layout(
            title="Model Performance Comparison",
            barmode="group",
            xaxis_title="Metrics",
            yaxis_title="Score",
            height=400,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("📋 Detailed Model Metrics")

        selected_model = st.selectbox("Select a model:", ["KNN", "SVM", "ANN"])

        if selected_model in trainer.metrics:
            metrics = trainer.metrics[selected_model]
            cm = trainer.confusion_matrices[selected_model]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{metrics['accuracy']:.4f}")
            col2.metric("Precision", f"{metrics['precision']:.4f}")
            col3.metric("Recall", f"{metrics['recall']:.4f}")
            col4.metric("F1-Score", f"{metrics['f1_score']:.4f}")

            st.markdown("---")
            st.subheader(f"Classification Report - {selected_model}")
            st.text(metrics["classification_report"])

            st.subheader(f"Confusion Matrix - {selected_model}")

            # ✅ FIXED CONFUSION MATRIX BLOCK
            from sklearn.metrics import confusion_matrix
            import plotly.express as px

            # Ensure cm is a 2D array
            if cm.ndim == 1:
                cm = cm.reshape((int(np.sqrt(len(cm))), int(np.sqrt(len(cm)))))

            fig_cm = px.imshow(
                cm,
                labels=dict(x="Predicted", y="Actual"),
                x=["Poor", "Average", "Good", "Excellent"],
                y=["Poor", "Average", "Good", "Excellent"],
                color_continuous_scale="Blues",
                text_auto=True,
            )
            st.plotly_chart(fig_cm, use_container_width=True)
        else:
            st.warning(f"No metrics found for {selected_model}.")


# ===============================================================
# 🔮 PREDICTION
# ===============================================================

elif page == "🔮 Make Predictions":
    st.title("🔮 Make Predictions")
    st.markdown("---")

    trainer = st.session_state.trainer
    preprocessor = st.session_state.preprocessor

    if not st.session_state.models_trained or trainer is None or preprocessor is None:
        st.warning("⚠️ Please train models first.")
    else:
        st.subheader("Enter Student Information")

        feature_names = preprocessor.X_train.columns.tolist()
        cols = st.columns(2)
        input_data = {}

        for i, feature in enumerate(feature_names):
            col = cols[i % 2]
            input_data[feature] = col.number_input(f"{feature}:", value=0.0)

        st.markdown("---")

        if st.button("🔮 Predict Performance", type="primary", use_container_width=True):
            try:
                input_df = pd.DataFrame([input_data])
                input_scaled = preprocessor.scaler.transform(input_df)

                performance_labels = ["Low", "Medium", "High"]
                cols = st.columns(3)

                for i, model_name in enumerate(["KNN", "SVM", "ANN"]):
                    if model_name in trainer.models:
                        pred = trainer.predict(model_name, input_scaled)[0]
                        label = performance_labels[int(pred) - 1]
                        cols[i].metric(model_name, label)
                    else:
                        cols[i].metric(model_name, "Not trained")

            except Exception as e:
                st.error(f"❌ Prediction error: {e}")

# ===============================================================
# 📄 DOCUMENTATION
# ===============================================================

elif page == "📄 Documentation":
    st.title("📄 Project Documentation")
    st.markdown("---")

    st.markdown(
        """
        ## Business Intelligence Predictive Modeling Application
        ### Project Information
        - **Course:** IS 108 - Intelligence System  
        - **Academic Year:** 2025–2026  
        - **Project Type:** Business Intelligence and Predictive Modeling  
        - **Team Size:** 3 Members  
        """
    )

    st.markdown(
        """
        ### Business Problem: Student Performance Prediction

        Predict academic performance based on:
        - Study hours, attendance, GPA, sleep hours, income, 
          internet speed, subjects, activities, parental support, motivation
        """
    )

    st.markdown(
        """
        ### Machine Learning Models
        1. **KNN:** Simple, interpretable — uses k nearest neighbors  
        2. **SVM:** Finds optimal separating hyperplane  
        3. **ANN:** Neural network captures complex patterns
        """
    )

    st.markdown(
        """
        ### Metrics
        - Accuracy, Precision, Recall, F1-Score  
        - Confusion Matrix visualization
        """
    )

    st.markdown(
        """
        ### Technical Stack
        - **Language:** Python 3.x  
        - **Framework:** Streamlit  
        - **Libraries:** scikit-learn, pandas, numpy, plotly  
        """
    )

    st.markdown("### Installation and Deployment")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

    st.markdown(
        """
        ---
        **Project Submitted by:** Jean Faith Marie Patula & Sean Endriga  
        **Date:** April 25, 2026
        """
    )
