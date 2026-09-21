from fastapi import APIRouter

from app.core.config import settings
from app.schemas.prediction import (
    CoralBleachingPredictionRequest,
    CoralBleachingPredictionResponse,
    ModelInfoResponse,
    ModelMetrics,
)
from app.services.prediction_service import (
    PredictionService,
)
from app.services.model_metadata_service import (
    ModelMetadataService,
)

router = APIRouter()


prediction_service = PredictionService(
    model_path=settings.model_path
)

metadata_service = ModelMetadataService(
    metadata_path=(
        settings.model_metadata_path
    )
)


@router.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Coral Bleaching Prediction API",
        "status": "running",
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@router.get("/model/status")
def model_status() -> dict[str, str]:
    return {
        "status": "loaded",
        "model": (
            metadata_service
            .get_model_name()
        ),
    }

@router.get(
    "/model/info",
    response_model=ModelInfoResponse,
)
def model_info() -> ModelInfoResponse:
    metadata = (
        metadata_service
        .get_metadata()
    )

    return ModelInfoResponse(
        model=metadata["model"],
        model_version=metadata[
            "model_version"
        ],
        target=metadata["target"],
        feature_count=metadata[
            "feature_count"
        ],
        metrics=ModelMetrics(
            mae=metadata[
                "metrics"
            ]["mae"],
            rmse=metadata[
                "metrics"
            ]["rmse"],
            r2=metadata[
                "metrics"
            ]["r2"],
        ),
        description=metadata[
            "description"
        ],
        limitation=metadata[
            "limitation"
        ],
    )

@router.post(
    "/api/v1/predictions",
    response_model=CoralBleachingPredictionResponse,
)
def predict_bleaching(
    request: CoralBleachingPredictionRequest,
) -> CoralBleachingPredictionResponse:

    prediction = (
        prediction_service.predict(
            request.model_dump()
        )
    )

    bleaching_level = (
        prediction_service
        .get_bleaching_level(
            prediction
        )
    )

    return CoralBleachingPredictionResponse(
        predicted_bleaching_percentage=(
            prediction
        ),
        bleaching_level=(
            bleaching_level
        ),
        model=(
            metadata_service
            .get_model_name()
        ),
        model_version=(
            metadata_service
            .get_model_version()
        ),
    )