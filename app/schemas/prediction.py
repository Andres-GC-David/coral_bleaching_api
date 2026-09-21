from pydantic import BaseModel, ConfigDict, Field


class CoralBleachingPredictionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )

    Longitude_Degrees: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    Latitude_Degrees: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    Distance_to_Shore: float | None = None
    Cyclone_Frequency: float | None = None
    SSTA_DHWMax: float | None = None
    Temperature_Mean: float | None = None
    TSA_DHWMax: float | None = None
    Turbidity: float | None = None
    TSA_Minimum: float | None = None
    SSTA_Frequency_Standard_Deviation: float | None = None
    SSTA_Standard_Deviation: float | None = None
    Temperature_Maximum: float | None = None
    TSA_Frequency_Standard_Deviation: float | None = None
    Temperature_Kelvin: float | None = None
    SSTA_Maximum: float | None = None
    ClimSST: float | None = None

    Date_Year: int | None = None

    TSA_Maximum: float | None = None
    SSTA_Minimum: float | None = None

    Date_Day: int | None = Field(
        default=None,
        ge=1,
        le=31,
    )

    SSTA: float | None = None
    TSA_DHWMean: float | None = None
    SSTA_DHW: float | None = None
    SSTA_Frequency: float | None = None
    TSA_DHW: float | None = None
    Depth_m: float | None = None
    SSTA_FrequencyMean: float | None = None
    TSA_Frequency: float | None = None
    Windspeed: float | None = None

    Date_Month: int | None = Field(
        default=None,
        ge=1,
        le=12,
    )

    Ocean_Name: str | None = None
    Realm_Name: str | None = None
    Exposure: str | None = None


class CoralBleachingPredictionResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "predicted_bleaching_percentage": 34.72,
                "bleaching_level": "Moderate",
                "model": "RandomForestRegressor",
                "model_version": "1.0.0"
            }
        }
    )

    predicted_bleaching_percentage: float
    bleaching_level: str
    model: str
    model_version: str

class ModelMetrics(BaseModel):
    mae: float
    rmse: float
    r2: float


class ModelInfoResponse(BaseModel):
    model: str
    model_version: str
    target: str
    feature_count: int
    metrics: ModelMetrics
    description: str
    limitation: str