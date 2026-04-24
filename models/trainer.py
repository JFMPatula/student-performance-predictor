"""
Machine learning models: KNN, SVM, and ANN
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
import pandas as pd
from typing import Literal, Tuple

class ModelTrainer:
    """Train and evaluate ML models"""
    
    def __init__(self):
        self.models = {}
        self.predictions = {}
        self.metrics = {}
        self.confusion_matrices = {}
        
    def train_knn(self, X_train, y_train, n_neighbors=5):
        """Train K-Nearest Neighbor model"""
        self.models['KNN'] = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.models['KNN'].fit(X_train, y_train)
        return self.models['KNN']
    
    def train_svm(self, X_train, y_train, kernel: Literal['linear', 'poly', 'rbf', 'sigmoid'] = 'rbf', C=1.0):
        """Train Support Vector Machine model"""
        self.models['SVM'] = SVC(kernel=kernel, C=C, probability=True, random_state=42)
        self.models['SVM'].fit(X_train, y_train)
        return self.models['SVM']
    
    def train_ann(self, X_train, y_train, hidden_layers: Tuple[int, ...] = (100, 50), max_iter=1000):
        """Train Artificial Neural Network model"""
        self.models['ANN'] = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            max_iter=max_iter,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.models['ANN'].fit(X_train, y_train)
        return self.models['ANN']
    
    def predict(self, model_name, X):
        """Make predictions with a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        return self.models[model_name].predict(X)
    
    def evaluate(self, model_name, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.predict(model_name, X_test)
        self.predictions[model_name] = y_pred
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'classification_report': classification_report(y_test, y_pred, zero_division=0)
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        self.metrics[model_name] = metrics
        self.confusion_matrices[model_name] = cm
        
        return metrics, cm
    
    def train_all_models(self, X_train, y_train):
        """Train all three models with adaptive configuration"""
        n_samples = len(X_train)

        # --- Adaptive KNN ---
        if n_samples < 50:
            n_neighbors = 3
        elif n_samples < 200:
            n_neighbors = 5
        else:
            n_neighbors = 7
        print(f"Training KNN with {n_neighbors} neighbors...")
        self.train_knn(X_train, y_train, n_neighbors=n_neighbors)

        # --- Adaptive SVM ---
        if n_samples < 50:
            kernel_type = "linear"
            c_value = 0.5
        elif n_samples < 200:
            kernel_type = "rbf"
            c_value = 1.0
        else:
            kernel_type = "poly"
            c_value = 2.0
        print(f"Training SVM with kernel={kernel_type}, C={c_value}...")
        self.train_svm(X_train, y_train, kernel=kernel_type, C=c_value)

        # --- Adaptive ANN ---
        if n_samples < 50:
            hidden_layers = (20,)
            max_iter = 200
        elif n_samples < 200:
            hidden_layers = (50,)
            max_iter = 300
        else:
            hidden_layers = (100, 50)
            max_iter = 500
        print(f"Training ANN with layers={hidden_layers}, max_iter={max_iter}...")
        self.train_ann(X_train, y_train, hidden_layers=hidden_layers, max_iter=max_iter)

        return self.models
    
    def evaluate_all_models(self, X_test, y_test):
        """Evaluate all trained models"""
        results = {}
        for model_name in ['KNN', 'SVM', 'ANN']:
            if model_name in self.models:  # Only evaluate trained models
                metrics, cm = self.evaluate(model_name, X_test, y_test)
                results[model_name] = {'metrics': metrics, 'confusion_matrix': cm}
        
        return results
    
    def get_model(self, model_name):
        """Get a specific trained model"""
        return self.models.get(model_name)
    
    def get_all_metrics(self):
        """Get metrics for all models"""
        return self.metrics
    
    def compare_models(self):
        """Compare all models and return comparison dataframe"""
        if not self.metrics:
            return pd.DataFrame()
        
        comparison = []
        for model_name, metrics in self.metrics.items():
            comparison.append({
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1-Score': metrics['f1_score']
            })
        
        return pd.DataFrame(comparison)
