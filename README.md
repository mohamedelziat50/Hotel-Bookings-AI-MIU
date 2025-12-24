# 🏨 Hotel Booking Cancellation Prediction System

<div align="center">
  
  <br/>
  
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6+-orange.svg)](https://scikit-learn.org/)
  [![MLP](https://img.shields.io/badge/model-MLP-green.svg)](https://scikit-learn.org/stable/modules/neural_networks.html)
  
  📊 **Dataset**: Hotel Bookings Dataset (119,390 bookings)
</div>

---

## Project Overview

A web-based machine learning system that predicts hotel booking cancellations to help hotels optimize revenue management. The system analyzes booking details (lead time, guest info, hotel type, dates, preferences) to predict cancellation likelihood, enabling:

- **Overbooking optimization** - Understand cancellation risk
- **Revenue management** - Identify high-risk bookings early
- **Operational planning** - Forecast actual occupancy
- **Loss reduction** - Minimize revenue loss from cancellations

Uses Genetic Algorithm (GA) feature selection and neural network classification trained on 119,390 historical bookings.

## Demo

### Prediction Examples

The following predictions are based on actual data rows from the `hotel_bookings.csv` dataset:

- **Not Cancelled Prediction (Row 4):** ![Not Cancelled Prediction](demo/not_cancelled_prediction.png)
  *Prediction using data from Row 4 of the dataset (target: not cancelled)*

- **Cancelled Prediction (Row 10):** ![Cancelled Prediction](demo/cancelled_prediction.png)
  *Prediction using data from Row 10 of the dataset (target: cancelled)*

## How It Works

### 1. User Input
Hotel staff input booking details through the web interface (guest info, dates, preferences, etc.)

### 2. Data Preprocessing
Input is automatically processed:
- Feature engineering (e.g., `total_stay`, `total_guests`, `is_month_start`, `is_month_end`)
- Categorical encoding and one-hot encoding
- Feature selection (uses 308 GA-selected features from 556 original)

### 3. Prediction
Trained model analyzes booking characteristics and returns cancellation prediction (cancelled/not cancelled)

### 4. Model Training
- **Genetic Algorithm**: Selected 308 most predictive features (44.6% reduction)
- **SMOTE**: Handled class imbalance
- **Neural Network (MLP)**: Trained on 119,390 historical bookings

## Features

- 🎯 Real-time cancellation prediction
- 📊 Interactive web interface
- 🔬 GA-based feature selection (308 features from 556)
- ⚖️ SMOTE for class imbalance
- 🧠 MLP neural network classifier

## Dataset

Trained on **119,390 booking records** with 33 original features including hotel type, booking dates, guest info, preferences, and market segment data.

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

To test the deployed Flask model, you can use specific rows from the `hotel_bookings.csv` dataset:

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

**Note:** The following CSV columns are not used in the frontend form and can be ignored when testing. These columns were excluded for different reasons (as documented in `Hotel_Booking.ipynb`):

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
