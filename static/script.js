document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Disable submit button
        submitBtn.disabled = true;
        const buttonText = submitBtn.querySelector('.button-text');
        if (buttonText) {
            buttonText.textContent = 'Analyzing...';
        } else {
            submitBtn.textContent = 'Analyzing...';
        }
        resultDiv.classList.add('hidden');

        // Collect form data
        const formData = new FormData(form);
        const data = {};
        
        // Convert FormData to object
        for (let [key, value] of formData.entries()) {
            // Convert numeric fields
            if (['lead_time', 'arrival_date_week_number', 'arrival_date_day_of_month',
                 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 
                 'babies', 'is_repeated_guest', 'required_car_parking_spaces', 
                 'total_of_special_requests'].includes(key)) {
                data[key] = parseInt(value) || 0;
            } else if (['adr', 'agent'].includes(key)) {
                data[key] = parseFloat(value) || 0;
            } else {
                data[key] = value;
            }
        }

        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Display result
            if (response.ok) {
                resultDiv.classList.remove('hidden');
                
                if (result.prediction === 1) {
                    resultDiv.className = 'result canceled';
                    resultDiv.textContent = '❌ ' + result.result;
                } else {
                    resultDiv.className = 'result success';
                    resultDiv.textContent = '✅ ' + result.result;
                }
            } else {
                // Display error
                resultDiv.classList.remove('hidden');
                resultDiv.className = 'result error';
                resultDiv.textContent = 'Error: ' + (result.error || 'Unknown error occurred');
            }
        } catch (error) {
            // Display error
            resultDiv.classList.remove('hidden');
            resultDiv.className = 'result error';
            resultDiv.textContent = 'Error: ' + error.message;
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            const buttonText = submitBtn.querySelector('.button-text');
            if (buttonText) {
                buttonText.textContent = 'Analyze Cancellation Risk';
            } else {
                submitBtn.textContent = 'Analyze Cancellation Risk';
            }
            
            // Scroll to result
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
});

