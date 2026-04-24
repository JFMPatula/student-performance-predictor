"""
Generate realistic student performance dataset for training models
"""
import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n_records = 300

# Generate synthetic student data
data = {
    'study_hours': np.random.uniform(1, 10, n_records),
    'attendance_percentage': np.random.uniform(50, 100, n_records),
    'previous_gpa': np.random.uniform(1.5, 4.0, n_records),
    'sleep_hours': np.random.uniform(4, 10, n_records),
    'family_income': np.random.choice([1, 2, 3, 4, 5], n_records),  # 1=low, 5=high
    'internet_speed_mbps': np.random.uniform(1, 100, n_records),
    'number_of_subjects': np.random.randint(4, 8, n_records),
    'extracurricular_activities': np.random.randint(0, 5, n_records),
    'parental_support': np.random.randint(1, 5, n_records),  # 1=low, 5=high
    'motivation_level': np.random.randint(1, 5, n_records),  # 1=low, 5=high
}

df = pd.DataFrame(data)

# Create target variable based on features with some noise
# Performance: 1 = Low, 2 = Medium, 3 = High
df['performance'] = 1  # Default to low
df.loc[(df['study_hours'] > 5) & (df['attendance_percentage'] > 75) & 
       (df['previous_gpa'] > 2.5) & (df['sleep_hours'] > 6), 'performance'] = 3  # High
df.loc[(df['performance'] == 1) & ((df['study_hours'] > 3) | (df['previous_gpa'] > 2.0)), 'performance'] = 2  # Medium

# Add some random noise
noise_indices = np.random.choice(df.index, size=int(0.1 * len(df)), replace=False)
df.loc[noise_indices, 'performance'] = np.random.randint(1, 4, len(noise_indices))

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

# Save to CSV
csv_path = os.path.join(data_dir, 'student_performance.csv')
df.to_csv(csv_path, index=False)
print(f"Dataset created successfully: {csv_path}")
print(f"Shape: {df.shape}")
print(f"\nFirst few records:\n{df.head()}")
print(f"\nPerformance distribution:\n{df['performance'].value_counts().sort_index()}")
