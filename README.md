# 🏨 Hotel Booking Cancellation Prediction System

<div align="center">
  <img src="static/images/hotel-cancellation.png" alt="Hotel Booking Cancellation Prediction" width="300"/>
  
  <br/>
  
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6+-orange.svg)](https://scikit-learn.org/)
  [![MLP](https://img.shields.io/badge/model-MLP-green.svg)](https://scikit-learn.org/stable/modules/neural_networks.html)
  
  📊 **Dataset**: Hotel Bookings Dataset (119,390 bookings)
</div>

---

## Project Overview

A full machine learning pipeline project that predicts hotel booking cancellations (target variable: `is_canceled`). The project implements:

- **Data Preprocessing & Cleaning** - Missing values, outliers, data type conversion, encoding
- **Exploratory Data Analysis (EDA)** - Visual analysis of booking patterns and cancellation trends
- **Feature Engineering** - Creating derived features from dates and booking characteristics
- **Feature Selection** - Genetic Algorithm (GA) to select optimal feature subset
- **Model Building & Comparison** - KNN, Decision Tree, and MLP (Multi-Layer Perceptron) neural network models
- **Performance Evaluation** - Accuracy, Precision, Recall, F1 Score, Confusion Matrix
- **Web Deployment** - Flask-based web interface for real-time predictions

Trained on 119,390 booking records with 33 original features, reduced to 308 selected features via Genetic Algorithm Feature Selection (44.6% reduction).

**Resources:**
- 📓 [Notebook Implementation](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/Hotel_Booking.ipynb) - Full ML pipeline implementation
- 📄 [Research Paper](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/Documents/IEEE_Conference_Hotel_Booking.pdf) - IEEE Conference paper
- 📊 [Dataset](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/hotel_bookings.csv) - Hotel bookings dataset (119,390 records)

## Demo

### Prediction Examples

The following predictions are based on actual data rows from the `hotel_bookings.csv` dataset:

**Not Cancelled Prediction (Row 4):**

<img src="https://github.com/user-attachments/assets/9bec58d9-aba0-4eb5-803b-2ad6c7ecc924" alt="Not Cancelled Prediction" width="450"/>

*Prediction using data from Row 4 of the dataset (target: not cancelled)*

**Cancelled Prediction (Row 10):**

<img src="https://github.com/user-attachments/assets/e9731016-b215-4998-a7eb-26fbd8d7fb9e" alt="Cancelled Prediction" width="450"/>

*Prediction using data from Row 10 of the dataset (target: cancelled)*

## How It Works

### Training Pipeline (Notebook Implementation)

**A. Data Preprocessing & Cleaning**
- Handle missing values (imputation with median/mode)
- Fix data types and remove duplicates
- Handle outliers using IQR method for selected numerical columns
- Remove data leakage features (`reservation_status`, `reservation_status_date`)
- Drop high missing value columns (`company` - 94.3% missing)

**B. Exploratory Data Analysis (EDA)**
- Distribution analysis of cancellations
- Booking trends by month, week, city
- ADR vs cancellation relationships
- Correlation heatmaps
- Lead time analysis
- Categorical feature analysis

**C. Data Balance Handling**
- Check target variable distribution
- Apply SMOTE (Synthetic Minority Oversampling Technique) to handle class imbalance

**D. Feature Engineering**
- Extract date features (`is_month_start`, `is_month_end`, `is_peak_season`)
- Create derived features (`total_stay`, `total_guests`)
- Convert categorical to numerical (Label Encoding, One-Hot Encoding)
- Result: 556 features after encoding

**E. Feature Selection (Genetic Algorithm)**
- Apply GA to select optimal feature subset
- Reduce from 556 to 308 features (44.6% reduction)
- Test impact on model performance

**F. Model Building & Comparison**
- Train/validation/test split (70/15/15)
- Build and compare: KNN, Decision Tree, MLP (Multi-Layer Perceptron) neural network
- Hyperparameter tuning using validation set
- Best model: MLP neural network (selected for deployment)

**G. Performance Evaluation**
- Compute metrics: Accuracy, Precision, Recall, F1 Score
- Generate confusion matrices
- Compare all models and select best performer

### Deployment Pipeline (Web Application)

1. **User Input** - Hotel staff input booking details through web interface
2. **Preprocessing** - Apply same preprocessing pipeline as training (see [notebook](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/Hotel_Booking.ipynb)): feature engineering, encoding, feature selection, standardization
3. **Prediction** - Load pre-trained MLP (Multi-Layer Perceptron) neural network model and return cancellation prediction

**Model Persistence:**
- Models and preprocessing tools are saved using `joblib` during training (see [notebook](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/Hotel_Booking.ipynb)):
  - `mlp_model.joblib` - Trained MLP neural network
  - `scaler.joblib` - StandardScaler fitted on training data
  - `selected_features.joblib` - List of 308 GA-selected features
  - `label_encoders.joblib` - Label encoders for categorical features
- At runtime, Flask application loads these saved artifacts from the `models/` directory using `joblib.load()`


## Setup Instructions

### To set up your environment after cloning (from the project root):

**1. Create a virtual environment:**
```bash
python -m venv .venv
```

**2. Activate the virtual environment:**

```bash
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Ensure you have the trained models (.joblib):**
Make sure the models are present in the `models/` directory.

**5. Run the Flask application:**
```bash
python app.py
```

**6. Access the application:**
Open your browser and navigate to:
```
http://localhost:3000
```

## Testing the Model

To test the deployed Flask model, you can use specific rows from the [dataset](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/hotel_bookings.csv):

- **Row 4** (target: not cancelled): Use this row to test a booking that should predict as "not cancelled"
- **Row 10** (target: cancelled): Use this row to test a booking that should predict as "cancelled"

Simply copy the values from these rows in the CSV file and input them into the web form to verify the model's predictions.

### Column Name Mapping

Note that some CSV column names differ from the frontend form labels for better user understanding. The mapping below follows the exact sequential order as fields appear in the frontend form:

| CSV Column Name | Frontend Form Label |
|----------------|---------------------|
| `hotel` | **Hotel Type** |
| `lead_time` | **Days Until Arrival** |
| `arrival_date_month` | **Month** |
| `arrival_date_week_number` | **Week** |
| `arrival_date_day_of_month` | **Day** |
| `stays_in_weekend_nights` | **Weekend Nights** |
| `stays_in_week_nights` | **Week Nights** |
| `adults` | **Adults** |
| `children` | **Children** |
| `babies` | **Babies** |
| `meal` | **Meal Type** |
| `country` | **Country Code** |
| `market_segment` | **Market Segment** |
| `distribution_channel` | **Distribution Channel** |
| `is_repeated_guest` | **Returning Guest** |
| `reserved_room_type` | **Reserved Room Type** |
| `assigned_room_type` | **Assigned Room Type** |
| `deposit_type` | **Deposit Type** |
| `customer_type` | **Customer Type** |
| `adr` | **Average Daily Rate (€)** |
| `required_car_parking_spaces` | **Parking Spaces** |
| `total_of_special_requests` | **Special Requests** |
| `agent` | **Agent ID** (optional) |
| `city` | **City** (optional) |

**Note:** The following CSV columns are not used in the frontend form and can be ignored when testing. These columns were excluded for different reasons (as documented in the [notebook](https://github.com/mohamedelziat50/Hotel-Bookings-AI-MIU/blob/main/Hotel_Booking.ipynb)):

**Dropped before feature selection (data preprocessing):**
- `company` - Dropped due to high missing values (94.3% missing); removed during data cleaning phase (see notebook section on missing values)
- `arrival_date_year` - Dropped during preprocessing; year information was not needed for prediction
- `reservation_status` - Dropped as a data leakage feature (contains the outcome information we're trying to predict - "Check-Out" or "Canceled")
- `reservation_status_date` - Dropped as a data leakage feature (date when status was finalized, which is post-booking information)

**Excluded by Genetic Algorithm (GA) feature selection:**
- `previous_cancellations` - Not selected by GA (may be system-related or not available at prediction time)
- `previous_bookings_not_canceled` - Not selected by GA (may be system-related or not available at prediction time)
- `booking_changes` - Not selected by GA (may be system-related or not available at prediction time)
- `days_in_waiting_list` - Not selected by GA (automatically set to 0 in preprocessing if not provided)

**Target variable (not a feature):**
- `is_canceled` - This is the target variable (what we're predicting), not an input feature
