# 🪸 Coral Bleaching Prediction API

[![API Tests](https://github.com/Andres-GC-David/coral_bleaching_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Andres-GC-David/coral_bleaching_api/actions/workflows/tests.yml)

Machine Learning REST API for estimating coral bleaching percentage from environmental, geographic, temporal, and categorical variables.

The project started as an academic supervised-learning study focused on predicting `Percent_Bleaching`. The selected model was later exported as a serialized scikit-learn pipeline and exposed through a production-style REST API built with FastAPI.

The repository demonstrates an end-to-end Machine Learning delivery workflow:

```text
Data analysis
    ↓
Preprocessing
    ↓
Feature selection
    ↓
Model training and evaluation
    ↓
Model serialization
    ↓
FastAPI REST API
    ↓
Automated tests
    ↓
Docker
    ↓
GitHub Actions CI
    ↓
Render deployment
```

---

## 🌐 Live API

The application is publicly deployed on **Render** using the Docker image defined in this repository.

### Interactive API Documentation

[Open Swagger UI](https://coral-bleaching-api.onrender.com/docs)

### Health Check

[API Health](https://coral-bleaching-api.onrender.com/health)

### Model Information

[Model Information](https://coral-bleaching-api.onrender.com/model/info)

> The application is hosted on a free-tier service. The first request after a period of inactivity may take additional time while the service starts.

---

## Project Overview

Coral bleaching is influenced by multiple environmental conditions, including temperature anomalies, thermal stress, turbidity, depth, wind conditions, geography, and other oceanographic variables.

This project uses a **supervised regression** approach to estimate the percentage of coral bleaching from environmental observations.

## Data Source

The Machine Learning model was developed using the following public dataset:

> van Woesik, R., & Burkepile, D. (2022).  
> *Bleaching and environmental data for global coral reef sites from 1980–2020.*  
> Biological and Chemical Oceanography Data Management Office (BCO-DMO).  
> Version 2, version date 2022-10-14.  
> DOI: https://doi.org/10.26008/1912/bco-dmo.773466.2  
> Accessed September 20, 2026.

Dataset page:

https://www.bco-dmo.org/dataset/773466

For this project, a processed subset of the original dataset was used after
data cleaning, feature preprocessing, feature selection, and preparation of
the supervised regression target.

### Target

```text
Percent_Bleaching
```

The final prediction pipeline receives **33 input features** and returns an estimated coral bleaching percentage.

---

## Machine Learning Model

Several regression algorithms were evaluated during the experimentation phase.

The selected final model is:

```text
RandomForestRegressor
```

### Final Test Metrics

| Metric | Result |
|---|---:|
| MAE | 7.4676 |
| RMSE | 13.6202 |
| R² | 0.5549 |

### Interpretation

The model explains approximately **55.5% of the observed variance** in coral bleaching percentage.

The MAE indicates that predictions differ from observed bleaching values by approximately **7.5 percentage points on average**.

The model performs better on low and moderate bleaching observations than on severe bleaching events.

For this reason, the system should be considered an **experimental academic Machine Learning model**, not an operational ecological forecasting system.

---

## Model Inputs

The final model uses **33 predictors**.

They include variables related to:

- Latitude and longitude
- Distance to shore
- Depth
- Turbidity
- Cyclone frequency
- Wind speed
- Sea-surface temperature
- Sea Surface Temperature Anomaly (`SSTA`)
- Thermal Stress Anomaly (`TSA`)
- Degree Heating Week variables
- Observation year, month, and day
- Ocean
- Biogeographic realm
- Exposure

The categorical variables used by the final model are:

```text
Ocean_Name
Realm_Name
Exposure
```

---

## Machine Learning Pipeline

The deployed `.joblib` artifact contains both preprocessing and prediction logic.

```text
Raw input
    │
    ▼
Missing-value handling
    │
    ├── Numerical variables → median imputation
    │
    └── Categorical variables → categorical imputation
    │
    ▼
Categorical encoding
    │
    └── One-Hot Encoding
    │
    ▼
RandomForestRegressor
    │
    ▼
Predicted bleaching percentage
```

Keeping preprocessing and the estimator inside the same serialized pipeline helps ensure that inference applies the same transformations used during training.

---

## API Architecture

```text
Client
   │
   │ HTTP / JSON
   ▼
FastAPI
   │
   ▼
Pydantic validation
   │
   ▼
PredictionService
   │
   ▼
Scikit-learn Pipeline
   │
   ├── Preprocessing
   │
   └── RandomForestRegressor
   │
   ▼
Prediction
   │
   ▼
JSON Response
```

Model metadata is managed separately:

```text
model_metadata.json
        │
        ▼
ModelMetadataService
        │
        ▼
API
```

---

## Technology Stack

### Machine Learning

- Python
- pandas
- NumPy
- scikit-learn
- joblib

### API

- FastAPI
- Pydantic
- Uvicorn

### Testing

- pytest
- FastAPI TestClient

### DevOps / Deployment

- Git
- GitHub
- GitHub Actions
- Docker
- Render

---

## Project Structure

```text
coral-bleaching-api/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prediction.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_metadata_service.py
│   │   └── prediction_service.py
│   ├── __init__.py
│   └── main.py
│
├── models/
│   ├── coral_bleaching_pipeline.joblib
│   └── model_metadata.json
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── run.py
└── README.md
```

---

# API Endpoints

## Root

```http
GET /
```

Returns the general API status.

Example:

```json
{
  "name": "Coral Bleaching Prediction API",
  "status": "running"
}
```

---

## Health Check

```http
GET /health
```

Example:

```json
{
  "status": "healthy"
}
```

This endpoint is also configured as the health-check path for the Render service.

---

## Model Status

```http
GET /model/status
```

Example:

```json
{
  "status": "loaded",
  "model": "RandomForestRegressor"
}
```

---

## Model Information

```http
GET /model/info
```

Returns metadata about the deployed Machine Learning model.

Example:

```json
{
  "model": "RandomForestRegressor",
  "model_version": "1.0.0",
  "target": "Percent_Bleaching",
  "feature_count": 33,
  "metrics": {
    "mae": 7.4676,
    "rmse": 13.6202,
    "r2": 0.5549
  },
  "description": "Regression model for estimating coral bleaching percentage using environmental variables.",
  "limitation": "Experimental academic model. Performance decreases for severe bleaching events."
}
```

---

# Prediction Endpoint

```http
POST /api/v1/predictions
```

The endpoint receives environmental information and returns a predicted coral bleaching percentage.

### Example Request

```json
{
  "Longitude_Degrees": -82.526,
  "Latitude_Degrees": 23.163,
  "Distance_to_Shore": 8519.23,
  "Cyclone_Frequency": 49.9,
  "SSTA_DHWMax": 7.88,
  "Temperature_Mean": 302.05,
  "TSA_DHWMax": 7.25,
  "Turbidity": 0.0287,
  "TSA_Minimum": -6.12,
  "SSTA_Frequency_Standard_Deviation": 3.13,
  "SSTA_Standard_Deviation": 1.0,
  "Temperature_Maximum": 304.69,
  "TSA_Frequency_Standard_Deviation": 1.09,
  "Temperature_Kelvin": 301.61,
  "SSTA_Maximum": 2.24,
  "ClimSST": 50.2,
  "Date_Year": 2005,
  "TSA_Maximum": 1.83,
  "SSTA_Minimum": -3.56,
  "Date_Day": 15,
  "SSTA": -0.46,
  "TSA_DHWMean": 0.18,
  "SSTA_DHW": 0.0,
  "SSTA_Frequency": 0.0,
  "TSA_DHW": 0.0,
  "Depth_m": 10.0,
  "SSTA_FrequencyMean": 3.0,
  "TSA_Frequency": 0.0,
  "Windspeed": 8.0,
  "Date_Month": 9,
  "Ocean_Name": "Atlantic",
  "Realm_Name": "Tropical Atlantic",
  "Exposure": "Exposed"
}
```

### Example Response

```json
{
  "predicted_bleaching_percentage": 34.72,
  "bleaching_level": "Moderate",
  "model": "RandomForestRegressor",
  "model_version": "1.0.0"
}
```

The exact prediction depends on the trained model.

---

## Bleaching Level

For presentation purposes, the API converts the numerical prediction into an interpretation band:

| Predicted bleaching | Level |
|---:|---|
| `< 25%` | Low |
| `25% – < 50%` | Moderate |
| `50% – < 75%` | High |
| `≥ 75%` | Severe |

These bands are an **application-level interpretation** of the regression output.

They are not additional classes learned by the Machine Learning model.

---

# Running Locally

## Requirements

- Python 3.13+
- pip

Clone the repository:

```bash
git clone https://github.com/Andres-GC-David/coral_bleaching_api.git
cd coral_bleaching_api
```

Create a virtual environment.

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

Run the application:

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Interactive API Documentation

FastAPI automatically generates OpenAPI documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger can be used to execute prediction requests directly from the browser.

---

# Automated Tests

The project contains automated API tests using `pytest`.

Run:

```bash
pytest -v
```

The current test suite validates:

- Health endpoint
- Model loading status
- Model metadata
- Prediction endpoint
- Latitude validation
- Month validation

Expected result:

```text
6 passed
```

---

# Continuous Integration and Deployment

## GitHub Actions CI

The repository includes the workflow:

```text
.github/workflows/tests.yml
```

The workflow is triggered on:

```text
push → main
pull_request → main
```

For every execution it:

1. Checks out the repository.
2. Configures Python 3.13.
3. Installs the dependencies from `requirements.txt`.
4. Runs the complete `pytest` test suite.

```text
Git push / Pull Request
          │
          ▼
     GitHub Actions
          │
          ▼
       pytest -v
          │
    ┌─────┴─────┐
    │           │
   FAIL        PASS
    │           │
    ▼           ▼
 CI fails   CI succeeds
```

The current workflow has been validated successfully with all **6 tests passing**.

## CI-Gated Deployment

Render is configured to deploy from the `main` branch **after CI checks pass**.

The resulting flow is:

```text
Local development
       │
       ▼
   git push
       │
       ▼
     GitHub
       │
       ▼
 GitHub Actions
       │
       ▼
      Tests
       │
 ┌─────┴────────────┐
 │                  │
FAIL               PASS
 │                  │
 ▼                  ▼
No production     Render
deployment          │
                    ▼
                Docker build
                    │
                    ▼
                 Deploy
                    │
                    ▼
              Public FastAPI
```

This prevents a new production deployment from proceeding when the automated CI checks fail.

---

# Docker

The API can run locally in the same containerized environment used for deployment.

Build the image:

```bash
docker build -t coral-bleaching-api .
```

Run the container:

```bash
docker run -p 8000:8000 coral-bleaching-api
```

The API will be available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Cloud Deployment

The production API is hosted as a **Render Web Service** using the repository's `Dockerfile`.

Deployment configuration:

```text
Repository: Andres-GC-David/coral_bleaching_api
Branch: main
Runtime: Docker
Health Check: /health
Deployment: after CI checks pass
Hosting: Render free tier
```

The deployment pipeline is therefore reproducible from source control and does not require manually copying application files to the server.

---

# Data Validation

Input validation is performed using Pydantic before data reaches the Machine Learning pipeline.

Examples include:

```text
Latitude  → -90 to 90
Longitude → -180 to 180
Month     → 1 to 12
Day       → 1 to 31
```

Invalid requests return an HTTP validation response before inference is executed.

---

# Model Limitations

The model has several important limitations.

### Moderate Predictive Capability

The final model achieved:

```text
R² ≈ 0.555
```

A significant part of the variability in coral bleaching therefore remains unexplained by the available predictors.

### Severe Bleaching Events

Prediction error increases for observations with very high bleaching percentages.

The model should not be interpreted as equally reliable across the entire target range.

### Dataset Dependency

Predictions depend on environmental and geographic patterns represented in the training dataset.

Observations substantially outside the training distribution may produce less reliable predictions.

### Scientific Use

This API was developed as an academic and portfolio Machine Learning project.

It is **not intended for operational environmental monitoring, ecological decision-making, or scientific forecasting without additional validation**.

---

# Design Principles

The API follows separation of responsibilities.

### Routes

Responsible for HTTP communication.

```text
app/api/
```

### Schemas

Responsible for request and response validation.

```text
app/schemas/
```

### Services

Responsible for application and inference logic.

```text
app/services/
```

### Configuration

Responsible for application settings and resource locations.

```text
app/core/
```

### Models

Contains the serialized Machine Learning pipeline and model metadata.

```text
models/
```

This structure avoids placing the entire application in a single FastAPI module and makes the project easier to maintain, test, and extend.

---

# Current Development Status

- [x] Exploratory Data Analysis
- [x] Data preprocessing
- [x] Feature selection
- [x] Model comparison
- [x] Hyperparameter optimization
- [x] Final model evaluation
- [x] Model serialization
- [x] FastAPI REST API
- [x] Pydantic input validation
- [x] Model metadata endpoint
- [x] Swagger / OpenAPI documentation
- [x] Automated API tests
- [x] Docker containerization
- [x] GitHub repository
- [x] GitHub Actions continuous integration
- [x] CI-gated deployment
- [x] Render public cloud deployment
- [x] Render health check
- [ ] Web user interface
- [ ] Model monitoring / observability
- [ ] Data drift detection

---

# Future Improvements

Potential improvements include:

- Batch prediction endpoint
- Prediction logging
- Model monitoring and observability
- Data drift detection
- Model versioning strategy
- Improved severe-event modeling
- Prediction uncertainty information
- Additional integration tests
- Code quality / linting checks in CI
- Automated container security scanning
- External environmental data integrations
- Web-based user interface

---

# Repository

GitHub:

[Andres-GC-David/coral_bleaching_api](https://github.com/Andres-GC-David/coral_bleaching_api)

---

# Disclaimer

This repository is an educational Machine Learning project.

Predictions generated by the API should not be interpreted as authoritative ecological forecasts or used as the sole basis for environmental decision-making.

---

## Authors

**Andrés Gutiérrez and Brandon Arroyo**

Machine Learning / Data Science project focused on environmental data and coral bleaching prediction.
