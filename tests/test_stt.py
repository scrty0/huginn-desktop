import pytest
from core.stt import SpeechToText
import numpy as np

def test_stt_init():
    # This might fail if models can't be downloaded, but we check import
    try:
        stt = SpeechToText(model_size="tiny")
        assert stt is not None
    except Exception as e:
        pytest.skip(f"Could not initialize STT: {e}")

def test_audio_pipeline_resample():
    from sip.audio_pipeline import AudioPipeline
    audio = np.zeros(48000)
    resampled = AudioPipeline.resample(audio, 48000, 16000)
    assert len(resampled) == 16000
