# 🪸 Coral Bleaching Prediction API

[![API Tests](https://github.com/Andres-GC-David/coral_bleaching_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Andres-GC-David/coral_bleaching_api/actions/workflows/tests.yml)

Backend API for an academic Machine Learning project that estimates coral bleaching percentage from environmental and geographic variables.

## Live Project

- **Web application:** https://coral-bleaching-prediction.netlify.app/
- **Swagger / API documentation:** https://coral-bleaching-api.onrender.com/docs
- **Health check:** https://coral-bleaching-api.onrender.com/health
- **Model information:** https://coral-bleaching-api.onrender.com/model/info

> The API is hosted on Render's free tier. The first request after a period of inactivity may take additional time while the service starts.

---

## About the Project

This project was developed as an **academic supervised Machine Learning project** focused on estimating coral bleaching percentage.

The target variable is:

```text
Percent_Bleaching
```

The final model uses **33 predictors** related to:

- Geographic location
- Distance to shore and depth
- Temperature
- Turbidity
- Wind and cyclone conditions
- Sea Surface Temperature Anomalies (`SSTA`)
- Thermal Stress Anomalies (`TSA`)
- Degree Heating Weeks (`DHW`)
- Observation date
- Ocean, marine realm, and exposure

The Machine Learning model is exposed through a FastAPI REST API and consumed by a separate Astro frontend.

---

## Machine Learning Model

The deployed model is:

```text
RandomForestRegressor
```

### Test Metrics

| Metric | Result |
|---|---:|
| MAE | 7.4676 |
| RMSE | 13.6202 |
| R² | 0.5549 |

The model has moderate predictive capability and performs less consistently for severe bleaching observations.

It should be treated as an **experimental academic model**, not as an operational ecological forecasting system.

---

## Data Source

The model was developed using a processed subset of:

> van Woesik, R., & Burkepile, D. (2022).  
> *Bleaching and environmental data for global coral reef sites from 1980–2020.*  
> Biological and Chemical Oceanography Data Management Office (BCO-DMO).  
> Version 2, version date 2022-10-14.  
> DOI: https://doi.org/10.26008/1912/bco-dmo.773466.2  
> Accessed September 20, 2026.

Dataset:

https://www.bco-dmo.org/dataset/773466

---

## Architecture

```text
Astro Frontend
Netlify
    │
    │ HTTPS / JSON
    ▼
FastAPI
Render
    │
    ▼
Pydantic Validation
    │
    ▼
Prediction Service
    │
    ▼
Scikit-learn Pipeline
    │
    ├── Preprocessing
    └── RandomForestRegressor
    │
    ▼
Bleaching Prediction
```

The frontend and backend are deployed independently.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning

- pandas
- NumPy
- scikit-learn
- joblib

### Testing & Deployment

- pytest
- Docker
- GitHub Actions
- Render

### Frontend

- Astro
- TypeScript
- Netlify

---

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status |
| `GET` | `/health` | Health check |
| `GET` | `/model/status` | Model loading status |
| `GET` | `/model/info` | Model metadata and metrics |
| `POST` | `/api/v1/predictions` | Generate a bleaching prediction |

For request and response schemas, use the interactive documentation:

https://coral-bleaching-api.onrender.com/docs

### Example Response

```json
{
  "predicted_bleaching_percentage": 34.72,
  "bleaching_level": "Moderate",
  "model": "RandomForestRegressor",
  "model_version": "1.0.0"
}
```

The exact result depends on the supplied observation.

---

## Bleaching Interpretation

The API also provides a simple presentation label:

| Prediction | Level |
|---:|---|
| `< 25%` | Low |
| `25% – < 50%` | Moderate |
| `50% – < 75%` | High |
| `≥ 75%` | Severe |

These labels are **application-level interpretation bands**. They are not classes learned by the model.

---

## Running Locally

### Requirements

- Python 3.13+
- pip

Clone the repository:

```bash
git clone https://github.com/Andres-GC-David/coral_bleaching_api.git
cd coral_bleaching_api
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Tests

Run:

```bash
pytest -v
```

The current suite validates:

- Health endpoint
- Model status
- Model metadata
- Prediction endpoint
- Latitude validation
- Month validation

Expected result:

```text
6 passed
```

---

## Docker

Build:

```bash
docker build -t coral-bleaching-api .
```

Run:

```bash
docker run -p 8000:8000 coral-bleaching-api
```

Then open:

```text
http://localhost:8000/docs
```

---

## CI/CD

GitHub Actions runs the automated test suite on pushes and pull requests to `main`.

```text
git push
   ↓
GitHub Actions
   ↓
pytest
   ↓
Tests pass
   ↓
Render deployment
```

Render is configured to deploy after CI checks pass.

---

## Project Structure

```text
app/
├── api/        # Routes
├── core/       # Configuration
├── schemas/    # Request and response models
├── services/   # Prediction and metadata logic
└── main.py

models/
├── coral_bleaching_pipeline.joblib
└── model_metadata.json

tests/
└── test_api.py
```

---

## Limitations

- The model does not explain all variability in coral bleaching.
- Performance decreases for severe bleaching observations.
- Predictions depend on patterns represented in the training data.
- Inputs far outside the training distribution may produce less reliable results.
- This project is intended for academic demonstration and portfolio use.

It is **not intended for operational environmental monitoring or conservation decisions without additional scientific validation**.

---

## Related Links

- **Web application:** https://coral-bleaching-prediction.netlify.app/
- **Backend repository:** https://github.com/Andres-GC-David/coral_bleaching_api
- **Swagger:** https://coral-bleaching-api.onrender.com/docs
- **BCO-DMO dataset:** https://www.bco-dmo.org/dataset/773466

---

## Authors

**Andrés Gutiérrez and Brandon Arroyo**

Academic Machine Learning project focused on coral bleaching prediction from environmental data.
