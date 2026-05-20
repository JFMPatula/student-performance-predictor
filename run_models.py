"""
Run all models and generate results for documentation
"""
import sys
sys.path.insert(0, '.')

# Import necessary modules
from utils.preprocessing import DataPreprocessor
from models.trainer import ModelTrainer
import pandas as pd

# Generate and load dataset
print("=" * 60)
print("RUNNING MODELS AND GENERATING RESULTS")
print("=" * 60)

# Load data
preprocessor = DataPreprocessor(test_size=0.2, random_state=42)
df = preprocessor.load_data('data/student_performance.csv')
print(f"\n✓ Dataset loaded: {df.shape[0]} records, {df.shape[1]} features")

# Preprocess
X_train, X_test, y_train, y_test = preprocessor.preprocess(df, target_column='performance')
print(f"✓ Data preprocessed")
print(f"  - Training set: {X_train.shape[0]} samples")
print(f"  - Testing set: {X_test.shape[0]} samples")

# Train models
print(f"\n✓ Training models...")
trainer = ModelTrainer()
trainer.train_all_models(X_train, y_train, use_smote=False)

# Evaluate
print(f"\n✓ Evaluating models...")
results = trainer.evaluate_all_models(X_test, y_test)

# Display results
print("\n" + "=" * 60)
print("MODEL PERFORMANCE RESULTS")
print("=" * 60)

comparison_df = trainer.compare_models()
print("\n" + comparison_df.to_string(index=False))

# Print detailed metrics
print("\n" + "=" * 60)
print("DETAILED METRICS")
print("=" * 60)

for model_name in ['KNN', 'SVM', 'ANN']:
    if model_name in trainer.metrics:
        metrics = trainer.metrics[model_name]
        cm = trainer.confusion_matrices[model_name]
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")
        print(f"\n  Confusion Matrix:")
        print(f"  {cm}")

# Save results to file for documentation
with open('model_results.txt', 'w') as f:
    f.write("MODEL RESULTS\n")
    f.write("=" * 60 + "\n\n")
    f.write(comparison_df.to_string(index=False))
    f.write("\n\n" + "=" * 60 + "\n")
    f.write("DETAILED METRICS\n")
    f.write("=" * 60 + "\n\n")
    
    for model_name in ['KNN', 'SVM', 'ANN']:
        if model_name in trainer.metrics:
            metrics = trainer.metrics[model_name]
            cm = trainer.confusion_matrices[model_name]
            f.write(f"{model_name}:\n")
            f.write(f"  Accuracy:  {metrics['accuracy']:.4f}\n")
            f.write(f"  Precision: {metrics['precision']:.4f}\n")
            f.write(f"  Recall:    {metrics['recall']:.4f}\n")
            f.write(f"  F1-Score:  {metrics['f1_score']:.4f}\n")
            f.write(f"\n  Confusion Matrix:\n")
            f.write(f"  {cm}\n\n")

print("\n✓ Results saved to model_results.txt")
print("=" * 60)
