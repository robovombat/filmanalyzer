# [ADDED STEP: Step 2e - MediaImporter Module | 2025-03-31 18:03]
# CHANGES:
# - File path validation for media import
# - Checks for supported file extensions
# - Returns load status string for shell or log output

from pathlib import Path

class MediaImporter:
    """📁 Handle media file imports and validation"""

    SUPPORTED_FORMATS = ['.mp4', '.mkv', '.mov', '.avi']

    def load_media(self, file_path: str) -> str:
        """📥 Load a media file from disk"""
        path = Path(file_path)

        # Check file exists
        if not path.exists():
            raise FileNotFoundError(f"[error] Path not found: {file_path}")

        # Check extension
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"[error] Unsupported format: {path.suffix}")

        # All good
        return f"[OK] Loaded {path.name} successfully"
