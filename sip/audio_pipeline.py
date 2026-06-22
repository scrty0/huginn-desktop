import numpy as np
import scipy.signal

class AudioPipeline:
    @staticmethod
    def resample(audio: np.ndarray, from_sr: int, to_sr: int = 16000) -> np.ndarray:
        if from_sr == to_sr:
            return audio
        num_samples = int(len(audio) * to_sr / from_sr)
        return scipy.signal.resample(audio, num_samples)

    @staticmethod
    def normalize(audio: np.ndarray) -> np.ndarray:
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio
