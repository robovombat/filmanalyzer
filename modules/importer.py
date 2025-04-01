# [MODIFIED STEP: Step 3.1 - Frame Extraction | 2025-03-31 19:50]
# CHANGES:
# - Added extract_frames(fps)
# - Uses OpenCV to read + save frames at regular intervals
# - Creates tmp_frames/<video_name>/ for output

from pathlib import Path
import cv2
import os

class MediaImporter:
    """📁 Handle media file imports and frame extraction"""

    SUPPORTED_FORMATS = ['.mp4', '.mkv', '.mov', '.avi']

    def __init__(self):
        self.video_path: Path = None
        self.loaded_name = ""

    def load_media(self, file_path: str) -> str:
        """📥 Load and validate media file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Path {file_path} not found")
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {path.suffix}")
        self.video_path = path
        self.loaded_name = path.stem
        return f"Loaded {path.name} successfully"

    def extract_frames(self, fps: float = 1.0) -> str:
        """🎞️ Extract frames at given FPS"""
        if not self.video_path:
            raise ValueError("No video loaded. Use load_media(path) first.")

        cap = cv2.VideoCapture(str(self.video_path))
        if not cap.isOpened():
            raise IOError("Failed to open video.")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / video_fps
        interval_ms = int(1000 / fps)

        output_dir = Path("tmp_frames") / self.loaded_name
        output_dir.mkdir(parents=True, exist_ok=True)

        frame_count = 0
        current_ms = 0
        while current_ms < duration * 1000:
            cap.set(cv2.CAP_PROP_POS_MSEC, current_ms)
            success, frame = cap.read()
            if not success:
                break
            frame_file = output_dir / f"frame_{frame_count:04d}.jpg"
            cv2.imwrite(str(frame_file), frame)
            frame_count += 1
            current_ms += interval_ms

        cap.release()
        return f"Extracted {frame_count} frames at {fps} fps → {output_dir}"
