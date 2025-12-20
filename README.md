# Hotel-Bookings-AI-MIU

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

**Note:** The following CSV columns are not used in the frontend form and can be ignored when testing. These columns were excluded during the **Genetic Algorithm (GA) feature selection** process, which identified the optimal subset of features for model training:

- `is_canceled` - This is the target variable (what we're predicting), not an input feature
- `arrival_date_year` - Excluded by GA feature selection; the model doesn't use year information for prediction
- `previous_cancellations` - Excluded by GA feature selection; historical cancellation data was not selected as a relevant feature
- `previous_bookings_not_canceled` - Excluded by GA feature selection; historical booking data was not selected as a relevant feature
- `booking_changes` - Excluded by GA feature selection; booking modification history was not selected as a relevant feature
- `company` - Excluded by GA feature selection; company information was not selected as a relevant feature
- `days_in_waiting_list` - Excluded by GA feature selection; automatically set to 0 in the preprocessing pipeline if not provided, so no user input needed
- `reservation_status` - This is the outcome/result of the booking (e.g., "Check-Out", "Canceled"), not an input feature
- `reservation_status_date` - This is the date when the reservation status was determined, not an input feature
