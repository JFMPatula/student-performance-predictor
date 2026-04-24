"""
Data preprocessing module for student performance prediction
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from io import BytesIO

class DataPreprocessor:
    """Handle all data preprocessing operations"""
    
    def __init__(self, test_size=0.2, random_state=42):
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self, filepath):
        """Load data from CSV, Excel, or uploaded file object"""
        # Check if it's a file object (from Streamlit uploader)
        if hasattr(filepath, 'name'):
            if filepath.name.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
            else:
                raise ValueError("Unsupported file format")
        # Check if it's a string path
        elif isinstance(filepath, str):
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
            else:
                raise ValueError("Unsupported file format")
        else:
            raise ValueError("Invalid file input")
        return df
    
    def get_dataset_info(self, df):
        """Get basic information about the dataset"""
        if df is None:
            return {
                'shape': (0, 0),
                'columns': [],
                'data_types': {},
                'missing_values': {},
                'numeric_columns': [],
                'categorical_columns': []
            }
        
        info = {
            'shape': df.shape,
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
        }
        return info
    
    def handle_missing_values(self, df, strategy='mean'):
        """Handle missing values"""
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype in ['int64', 'float64']:
                    if strategy == 'mean':
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                    elif strategy == 'median':
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                else:
                    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        
        return df_clean
    
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical features"""
        df_encoded = df.copy()
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col])
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    df_encoded[col] = self.label_encoders[col].transform(df_encoded[col])
        
        return df_encoded
    
    def preprocess(self, df, target_column='performance'):
        """Complete preprocessing pipeline"""
        # Make a copy
        df_processed = df.copy()
        
        # Handle missing values
        df_processed = self.handle_missing_values(df_processed)
        
        # Encode categorical variables
        df_processed = self.encode_categorical_features(df_processed, fit=True)
        
        # Separate features and target
        X = df_processed.drop(columns=[target_column])
        y = df_processed[target_column]
        
        # Split dataset
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        
        # Scale features
        self.X_train = pd.DataFrame(
            self.scaler.fit_transform(self.X_train),
            columns=X.columns
        )
        self.X_test = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=X.columns
        )
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_split_info(self):
        """Get training/testing split information"""
        if self.X_train is None or self.X_test is None:
            return {
                'train_size': 0,
                'test_size': 0,
                'total_size': 0,
                'train_percentage': 0.0,
                'test_percentage': 0.0,
            }
        
        return {
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'total_size': len(self.X_train) + len(self.X_test),
            'train_percentage': (len(self.X_train) / (len(self.X_train) + len(self.X_test))) * 100,
            'test_percentage': (len(self.X_test) / (len(self.X_train) + len(self.X_test))) * 100,
        }