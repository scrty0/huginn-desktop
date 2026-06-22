import numpy as np
import scipy.io.wavfile as wav

def create_sample_call(filename="demo/sample_call.wav"):
    # Generate 1 second of "silence" (noise)
    fs = 16000
    duration = 5  # seconds
    samples = np.random.uniform(-0.01, 0.01, fs * duration).astype(np.float32)
    wav.write(filename, fs, samples)
    print(f"Sample call generated: {filename}")

if __name__ == "__main__":
    create_sample_call()
