from pathlib import Path

import joblib
import pandas as pd


class PredictionService:
    def __init__(
        self,
        model_path: str,
    ) -> None:
        self._model_path = Path(model_path)
        self._model = self._load_model()

    def _load_model(self):
        if not self._model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en: "
                f"{self._model_path}"
            )

        return joblib.load(
            self._model_path
        )

    def predict(
        self,
        input_data: dict,
    ) -> float:
        dataframe = pd.DataFrame(
            [input_data]
        )

        prediction = self._model.predict(
            dataframe
        )[0]

        return float(prediction)

    @staticmethod
    def get_bleaching_level(
        prediction: float,
    ) -> str:
        if prediction < 25:
            return "Low"

        if prediction < 50:
            return "Moderate"

        if prediction < 75:
            return "High"

        return "Severe"