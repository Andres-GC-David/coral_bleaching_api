from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_model_status() -> None:
    response = client.get("/model/status")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "loaded"
    assert body["model"] == "RandomForestRegressor"


def test_model_info() -> None:
    response = client.get("/model/info")

    assert response.status_code == 200

    body = response.json()

    assert body["model"] == "RandomForestRegressor"
    assert body["model_version"] == "1.0.0"
    assert body["target"] == "Percent_Bleaching"
    assert body["feature_count"] == 33

    assert body["metrics"]["mae"] == 7.4676
    assert body["metrics"]["rmse"] == 13.6202
    assert body["metrics"]["r2"] == 0.5549

def test_prediction() -> None:
    payload = {
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
        "Exposure": "Exposed",
    }

    response = client.post(
        "/api/v1/predictions",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert "predicted_bleaching_percentage" in body
    assert "bleaching_level" in body
    assert body["model"] == "RandomForestRegressor"
    assert body["model_version"] == "1.0.0"

    prediction = body[
        "predicted_bleaching_percentage"
    ]

    assert isinstance(
        prediction,
        float,
    )

    assert 0 <= prediction <= 100


def test_invalid_latitude() -> None:
    payload = {
        "Latitude_Degrees": 150,
    }

    response = client.post(
        "/api/v1/predictions",
        json=payload,
    )

    assert response.status_code == 422

def test_invalid_month() -> None:
    payload = {
        "Date_Month": 15,
    }

    response = client.post(
        "/api/v1/predictions",
        json=payload,
    )

    assert response.status_code == 422