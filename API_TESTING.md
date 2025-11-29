# Price Prediction API - Testing Guide

## Available Endpoints

### 1. `/ml/predict-price` - Price Prediction Only
Predict price when you already know the breed.

**Method:** POST  
**Content-Type:** multipart/form-data

**Parameters:**
- `image`: File (pet image)
- `pet_type`: String ('Dog' or 'Cat')
- `breed`: String (e.g., 'Golden Retriever', 'Persian')
- `age_months`: Integer (2-60)
- `weight_kg`: Float
- `health_status`: Integer (0=normal, 1=good, 2=excellent)
- `vaccinated`: Boolean (true/false)

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/ml/predict-price" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/dog.jpg" \
  -F "pet_type=Dog" \
  -F "breed=Golden Retriever" \
  -F "age_months=4" \
  -F "weight_kg=10.5" \
  -F "health_status=2" \
  -F "vaccinated=true"
```

**Response:**
```json
{
  "predicted_price": 1875.50,
  "metadata": {
    "pet_type": "Dog",
    "breed": "Golden Retriever",
    "age_months": 4,
    "weight_kg": 10.5,
    "health_status": 2,
    "vaccinated": true
  }
}
```

---

### 2. `/ml/classify-and-price` - Combined Endpoint
Classify breed AND predict price in one call.

**Method:** POST  
**Content-Type:** multipart/form-data

**Parameters:**
- `image`: File (pet image)
- `age_months`: Integer (2-60)
- `weight_kg`: Float
- `health_status`: Integer (0, 1, or 2)
- `vaccinated`: Boolean

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/ml/classify-and-price" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/dog.jpg" \
  -F "age_months=4" \
  -F "weight_kg=10.5" \
  -F "health_status=2" \
  -F "vaccinated=true"
```

**Response:**
```json
{
  "classification": {
    "type": "Dog",
    "breed": "Golden Retriever",
    "confidence": 0.95
  },
  "price_prediction": {
    "predicted_price": 1875.50,
    "metadata": {
      "age_months": 4,
      "weight_kg": 10.5,
      "health_status": 2,
      "vaccinated": true
    }
  }
}
```

---

## Testing with Postman

1. **Open Postman**
2. **Create New Request**
3. **Set Method to POST**
4. **Enter URL**: `http://localhost:8000/ml/predict-price`
5. **Go to Body tab**
6. **Select "form-data"**
7. **Add fields:**
   - `image` (File) - Upload a dog/cat image
   - `pet_type` (Text) - `Dog`
   - `breed` (Text) - `Golden Retriever`
   - `age_months` (Text) - `4`
   - `weight_kg` (Text) - `10.5`
   - `health_status` (Text) - `2`
   - `vaccinated` (Text) - `true`
8. **Click Send**

---

## Testing with Python

```python
import requests

# Test predict-price endpoint
url = "http://localhost:8000/ml/predict-price"

files = {
    'image': open('path/to/dog.jpg', 'rb')
}

data = {
    'pet_type': 'Dog',
    'breed': 'Golden Retriever',
    'age_months': 4,
    'weight_kg': 10.5,
    'health_status': 2,
    'vaccinated': True
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

---

## Expected Results

Based on the training data:
- **Young pets (< 6 months)**: Higher prices (1.3x multiplier)
- **Excellent health**: +$200 bonus
- **Vaccinated**: +$150 bonus
- **Breed base prices**: Vary by breed (e.g., Golden Retriever ~$1500)

**Example calculations:**
- Golden Retriever, 4 months, Excellent health, Vaccinated
- Base: $1500 × 1.3 (young) = $1950
- +$200 (excellent health)
- +$150 (vaccinated)
- **Expected: ~$2300**

---

## Troubleshooting

### Error: Model not found
**Solution:** Ensure `ml/models/price_predictor.keras` exists. Run training if needed:
```bash
python ml/train_price_model.py
```

### Error: Unknown breed
**Solution:** The breed must exist in the training data. Check available breeds:
```python
import joblib
encoders = joblib.load('ml/models/price_encoders.joblib')
print(encoders['breed_encoder'].classes_)
```

### High price variance
**Solution:** This is expected! The model considers:
- Image visual features (appearance, coat quality)
- Age (younger = more expensive)
- Weight (healthier weight)
- Health status
- Vaccination
