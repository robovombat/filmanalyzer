# [STEP: Step 3.1 - Extract Frame Progress | INITIAL: 2025-04-01 16:10 | MODIFIED: 2025-04-01 16:49]
# CHANGES:
# - Added extract_frames() method
# - Supports optional on_progress() callback
# - Extracts frames using cv2.VideoCapture
# - Stores frames in tmp_frames/<video_stem>/

import os
from pathlib import Path
import cv2
from time import time
from log.logger import log

class MediaImporter:
    """📁 Handle media file imports and validation"""

    SUPPORTED_FORMATS = ['.mp4', '.mkv', '.mov', '.avi']

    def __init__(self):
        self.last_loaded_path = None

    def load_media(self, file_path: str) -> str:
        """📥 Load and validate a video file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Path {file_path} not found")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {path.suffix}")

        self.last_loaded_path = path
        log.info(f"[IMPORT] Media loaded: {path.name}")
        return f"Loaded {path.name} successfully"

    def extract_frames(self, fps: float = 1.0, on_progress=None) -> str:
        """🖼️ Extract frames from the loaded video at fixed fps"""
        if not self.last_loaded_path:
            raise RuntimeError("No media loaded")

        video_path = str(self.last_loaded_path)
        name = self.last_loaded_path.stem
        out_dir = Path("tmp_frames") / name
        out_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        interval = max(int(video_fps / fps), 1)

        extracted = 0
        start = time()
        frame_id = 0
        progress_step = max(total_frames // 10, 1)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id % interval == 0:
                out_path = out_dir / f"frame_{extracted:04d}.jpg"
                cv2.imwrite(str(out_path), frame)
                extracted += 1

                # 🔁 Update progress
                if on_progress and extracted % progress_step == 0:
                    percent = int((frame_id / total_frames) * 100)
                    elapsed = time() - start
                    fps_eff = extracted / elapsed if elapsed > 0 else 1
                    eta = int((total_frames - frame_id) / fps_eff)
                    on_progress(percent, eta)

            frame_id += 1

        cap.release()
        log.info(f"[IMPORT] Extracted {extracted} frames to {out_dir}")
        return f"Extracted {extracted} frames at {fps} fps → {out_dir}"
