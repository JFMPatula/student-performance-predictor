"""
Generate realistic student performance dataset for training models
Loads real-world scenario data from sample_dataset_large.csv
Format: study_hours, attendance_percentage, sleep_hours, family_income, 
         internet_speed_mbps, number_of_subjects, extracurricular_activities,
         parental_support, motivation_level, performance
"""
import pandas as pd
import os

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

# Path to real-world sample dataset
sample_path = os.path.join(os.path.dirname(__file__), 'sample_dataset_large.csv')
csv_path = os.path.join(data_dir, 'student_performance.csv')

# Check if sample dataset exists
if os.path.exists(sample_path):
    # Load the real-world scenario dataset
    df = pd.read_csv(sample_path)
    
    # Save to the data directory
    df.to_csv(csv_path, index=False)
    
    print(f"✓ Real-world scenario dataset loaded successfully!")
    print(f"  Source: {sample_path}")
    print(f"  Location: {csv_path}")
    print(f"  Records: {df.shape[0]}")
    print(f"\nPerformance Distribution:")
    print(df['performance'].value_counts())
    print(f"\nFirst few records:\n{df.head(10)}")
else:
    print(f"❌ Error: sample_dataset_large.csv not found!")
    print(f"  Expected location: {sample_path}")
    print(f"\nPlease ensure sample_dataset_large.csv exists in the project root.")

