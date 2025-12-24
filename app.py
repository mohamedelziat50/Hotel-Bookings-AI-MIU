from flask import Flask, render_template, request, jsonify
from joblib import load
import pandas as pd
import numpy as np
import warnings

app = Flask(__name__)

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Load the pre-trained model and preprocessing tools
mlp_model = load('models/mlp_model.joblib')
scaler = load('models/scaler.joblib')
selected_features = load('models/selected_features.joblib')

# Load label encoders (required for prediction)
try:
    label_encoders = load('models/label_encoders.joblib')
except FileNotFoundError:
    print("Warning: label_encoders.joblib not found. You need to create and save label encoders from your notebook.")
    label_encoders = None

# Columns for label encoding (as per notebook)
LABEL_ENCODE_COLS = [
    'hotel', 'meal', 'deposit_type', 'customer_type',
    'reserved_room_type', 'assigned_room_type'
]

# Columns for one-hot encoding (as per notebook)
ONE_HOT_COLS = ['country', 'market_segment', 'distribution_channel', 'agent', 'city']


def preprocess_input(data):
    """Preprocess input data to match the training pipeline"""
    df = pd.DataFrame([data])
    
    # Handle missing values - fill with defaults
    df['children'] = df['children'].fillna(0).astype(int)
    df['agent'] = df['agent'].fillna(0).astype(float) if 'agent' in df.columns else 0.0
    if 'agent' not in df.columns:
        df['agent'] = 0.0
    
    # Add any missing base features that might be in training data
    if 'days_in_waiting_list' not in df.columns:
        df['days_in_waiting_list'] = 0
    
    defaults = {
        'country': 'PRT',
        'market_segment': 'Online TA',
        'distribution_channel': 'TA/TO',
        'meal': 'BB'
    }
    for col, default in defaults.items():
        df[col] = df[col].fillna(default)
    
    # Create engineered features (as per notebook)
    df['is_month_start'] = (df['arrival_date_day_of_month'] <= 10).astype(int)
    df['is_month_end'] = (df['arrival_date_day_of_month'] >= 25).astype(int)
    df = df.drop('arrival_date_day_of_month', axis=1)
    
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['total_guests'] = df['adults'] + df['children'] + df['babies']
    df['adr'] = df['adr'].clip(lower=0)
    
    # Apply label encoding
    if label_encoders is None:
        raise ValueError("Label encoders not loaded. Please create and save label_encoders.joblib from your notebook.")
    
    for col in LABEL_ENCODE_COLS:
        le = label_encoders[col]
        # Handle unseen labels by using the first known class
        df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        df[col] = le.transform(df[col])
    
    # Convert agent to string for consistent one-hot encoding format
    df['agent'] = df['agent'].astype(str)
    
    # Store all columns before one-hot encoding
    cols_before_ohe = list(df.columns)
    
    # Apply one-hot encoding (preserves all non-encoded columns)
    df = pd.get_dummies(df, columns=ONE_HOT_COLS, drop_first=True)
    
    # Debug: Check what columns we have after one-hot encoding
    cols_after_ohe = list(df.columns)
    
    # Critical: Ensure we have EXACTLY the columns from selected_features
    # Step 1: Add all missing features from selected_features with 0
    for feature in selected_features:
        if feature not in df.columns:
            df[feature] = 0
    
    # Step 2: Create a new dataframe with ONLY selected_features columns
    # This removes any extra one-hot encoded columns (like agent_10.0 if it wasn't in training)
    result_df = pd.DataFrame(index=df.index)
    for feature in selected_features:
        if feature in df.columns:
            result_df[feature] = df[feature]
        else:
            result_df[feature] = 0
    
    # Step 3: Ensure columns are in the exact same order as selected_features
    result_df = result_df[selected_features]
    
    return result_df
    
    # Scale numerical features
    numerical_features = result_df.select_dtypes(include=[np.number]).columns.tolist()
    result_df[numerical_features] = scaler.transform(result_df[numerical_features])
    
    return result_df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Add optional fields with defaults
    data.setdefault('agent', 0)
    data.setdefault('city', 'Unknown')
    data.setdefault('arrival_date_day_of_month', 15)
    
    # Preprocess and predict
    processed_data = preprocess_input(data)
    prediction = mlp_model.predict(processed_data)[0]
    
    result = "Booking Likely to be Canceled" if prediction == 1 else "Booking Likely to be Not Canceled"
    
    return jsonify({
        "prediction": int(prediction),
        "result": result
    })


if __name__ == '__main__':
    app.run(port=3000, debug=True)

