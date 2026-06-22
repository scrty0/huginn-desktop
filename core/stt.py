import numpy as np
from faster_whisper import WhisperModel
from typing import AsyncIterator

class SpeechToText:
    def __init__(self, model_size="base", device="cpu"):
        self.model = WhisperModel(model_size, device=device, compute_type="int8")

    def transcribe(self, audio_data: np.ndarray) -> str:
        # audio_data should be float32, 16000Hz
        segments, _ = self.model.transcribe(audio_data, language="ru")
        return " ".join(s.text for s in segments)

    async def transcribe_stream(self, chunk_iter: AsyncIterator[np.ndarray]) -> str:
        full_text = ""
        async for chunk in chunk_iter:
            text = self.transcribe(chunk)
            full_text += text + " "
        return full_text.strip()
