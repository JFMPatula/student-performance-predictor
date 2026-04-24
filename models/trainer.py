"""
Machine learning models: KNN, SVM, and ANN with class imbalance handling
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
from typing import Literal, Tuple

class ModelTrainer:
    """Train and evaluate ML models with automatic dataset adaptation"""
    
    def __init__(self):
        self.models = {}
        self.predictions = {}
        self.metrics = {}
        self.confusion_matrices = {}
        self.dataset_info = {}  # Store dataset characteristics for adaptation
        
    def train_knn(self, X_train, y_train, n_neighbors=5):
        """Train K-Nearest Neighbor model with weighted neighbors for class imbalance"""
        # KNN doesn't support class_weight, so use distance-weighted voting
        # This gives more influence to nearer neighbors, reducing bias from class imbalance
        self.models['KNN'] = KNeighborsClassifier(
            n_neighbors=n_neighbors,
            weights='distance',  # Weight by inverse distance to handle imbalance
            metric='minkowski'
        )
        self.models['KNN'].fit(X_train, y_train)
        return self.models['KNN']
    
    def train_svm(self, X_train, y_train, kernel: Literal['linear', 'poly', 'rbf', 'sigmoid'] = 'rbf', C=1.0):
        """Train Support Vector Machine model with class weight balancing"""
        # Compute class weights to handle imbalance
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = {cls: weight for cls, weight in zip(classes, class_weights)}
        
        self.models['SVM'] = SVC(kernel=kernel, C=C, class_weight=class_weight_dict, probability=True, random_state=42)
        self.models['SVM'].fit(X_train, y_train)
        return self.models['SVM']
    
    def train_ann(self, X_train, y_train, hidden_layers: Tuple[int, ...] = (100, 50), max_iter=1000):
        """Train Artificial Neural Network model with class weight balancing"""
        # Compute class weights and sample weights to handle imbalance
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = {cls: weight for cls, weight in zip(classes, class_weights)}
        sample_weights = np.array([class_weight_dict[label] for label in y_train])
        
        self.models['ANN'] = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            max_iter=max_iter,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.models['ANN'].fit(X_train, y_train, sample_weight=sample_weights)  # type: ignore[call-arg]
        return self.models['ANN']
    
    def predict(self, model_name, X):
        """Make predictions with a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        return self.models[model_name].predict(X)
    
    def evaluate(self, model_name, X_test, y_test):
        """Evaluate model performance with per-class metrics for edge case analysis"""
        y_pred = self.predict(model_name, X_test)
        self.predictions[model_name] = y_pred
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'classification_report': classification_report(y_test, y_pred, zero_division=0),
            # Per-class metrics for edge case analysis
            'precision_per_class': precision_score(y_test, y_pred, average=None, zero_division=0),
            'recall_per_class': recall_score(y_test, y_pred, average=None, zero_division=0),
            'f1_per_class': f1_score(y_test, y_pred, average=None, zero_division=0)
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        self.metrics[model_name] = metrics
        self.confusion_matrices[model_name] = cm
        
        return metrics, cm
    
    def train_all_models(self, X_train, y_train, use_smote=True):
        """Train all three models with automatic adaptation to dataset characteristics"""
        # Analyze dataset to guide hyperparameter selection
        self._analyze_dataset(X_train, y_train)
        
        n_samples = len(X_train)
        n_features = X_train.shape[1] if len(X_train.shape) > 1 else 1
        n_classes = len(np.unique(y_train))
        
        print(f"\nDataset Analysis:")
        print(f"  Samples: {n_samples}, Features: {n_features}, Classes: {n_classes}")
        
        # Apply SMOTE to balance minority classes (optional, controlled by use_smote parameter)
        if use_smote:
            try:
                # Determine safe k_neighbors value based on minority class size
                unique_classes, class_counts = np.unique(y_train, return_counts=True)
                min_class_count = class_counts.min()
                # k_neighbors must be < minority class size
                safe_k_neighbors = min(3, max(1, min_class_count - 1))
                
                smote = SMOTE(random_state=42, k_neighbors=safe_k_neighbors)
                X_train, y_train = smote.fit_resample(X_train, y_train)  # type: ignore[assignment]
                print("SMOTE applied: Minority classes oversampled")
                print(f"Original shape: {X_train.shape}, Balanced shape: {X_train.shape}")
            except Exception as e:
                print(f"SMOTE failed (likely too few samples): {e}. Using class weights instead.")
        
        n_samples = len(X_train)

        # --- Adaptive KNN ---
        # Adapt n_neighbors based on dataset size and number of classes
        if n_samples < 50:
            n_neighbors = max(3, n_classes)
        elif n_samples < 200:
            n_neighbors = max(5, n_classes)
        else:
            n_neighbors = max(7, n_classes + 2)
        print(f"\nTraining KNN with {n_neighbors} neighbors (adapted to {n_classes} classes)...")
        self.train_knn(X_train, y_train, n_neighbors=n_neighbors)

        # --- Adaptive SVM ---
        # Adapt kernel and C based on feature count and dataset size
        if n_features > 20:
            kernel_type = "linear"  # Linear kernel for high-dimensional data
        elif n_samples < 100:
            kernel_type = "linear"
        else:
            kernel_type = "rbf"
        
        if n_samples < 50:
            c_value = 0.5
        elif n_samples < 200:
            c_value = 1.0
        else:
            c_value = 2.0
        print(f"Training SVM with kernel={kernel_type}, C={c_value}...")
        self.train_svm(X_train, y_train, kernel=kernel_type, C=c_value)

        # --- Adaptive ANN ---
        # Adapt hidden layers based on feature and class count
        if n_samples < 50:
            hidden_layers = (max(10, n_features),)
            max_iter = 200
        elif n_samples < 200:
            hidden_layers = (max(50, n_features * 2), max(25, n_features))
            max_iter = 300
        else:
            hidden_layers = (max(100, n_features * 3), max(50, n_features))
            max_iter = 500
        print(f"Training ANN with layers={hidden_layers}, max_iter={max_iter}...")
        self.train_ann(X_train, y_train, hidden_layers=hidden_layers, max_iter=max_iter)

        return self.models
    
    def _analyze_dataset(self, X_train, y_train):
        """Analyze dataset characteristics for auto-adaptation"""
        n_samples = len(X_train)
        n_features = X_train.shape[1] if len(X_train.shape) > 1 else 1
        unique_classes, class_counts = np.unique(y_train, return_counts=True)
        n_classes = len(unique_classes)
        
        # Calculate class imbalance ratio
        imbalance_ratio = class_counts.max() / class_counts.min()
        
        self.dataset_info = {
            'n_samples': n_samples,
            'n_features': n_features,
            'n_classes': n_classes,
            'class_counts': dict(zip(unique_classes, class_counts)),
            'imbalance_ratio': imbalance_ratio,
            'is_imbalanced': imbalance_ratio > 2.0  # Consider >2:1 as imbalanced
        }
        
        return self.dataset_info
    
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
