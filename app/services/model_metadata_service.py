import json
from pathlib import Path


class ModelMetadataService:
    def __init__(
        self,
        metadata_path: str,
    ) -> None:
        self._metadata_path = Path(
            metadata_path
        )

        self._metadata = (
            self._load_metadata()
        )

    def _load_metadata(self) -> dict:
        if not self._metadata_path.exists():
            raise FileNotFoundError(
                f"No se encontró la metadata en: "
                f"{self._metadata_path}"
            )

        with open(
            self._metadata_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def get_metadata(self) -> dict:
        return self._metadata

    def get_model_name(self) -> str:
        return self._metadata["model"]

    def get_model_version(self) -> str:
        return self._metadata[
            "model_version"
        ]