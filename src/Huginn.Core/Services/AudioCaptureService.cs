using System;
using System.Collections.Generic;
using System.Linq;
using NAudio.CoreAudioApi;
using NAudio.Wave;
namespace Huginn.Core.Services {
    public class AudioCaptureService : IAudioCaptureService, IDisposable {
        private WasapiLoopbackCapture? _capture;
        public event Action<float[]>? DataAvailable;
        public void Start(string? deviceName = null) {
            Stop();
            MMDevice? device = null;
            if (!string.IsNullOrEmpty(deviceName)) {
                var enumerator = new MMDeviceEnumerator();
                device = enumerator.EnumerateAudioEndPoints(DataFlow.Render, DeviceState.Active)
                    .FirstOrDefault(d => d.FriendlyName == deviceName);
            }
            _capture = device == null ? new WasapiLoopbackCapture() : new WasapiLoopbackCapture(device);
            int sr = _capture.WaveFormat.SampleRate;
            _capture.DataAvailable += (s, e) => {
                if (e.BytesRecorded == 0) return;
                var buffer = new WaveBuffer(e.Buffer);
                int samplesRecorded = e.BytesRecorded / 4;
                float[] samples = new float[samplesRecorded];
                Array.Copy(buffer.FloatBuffer, samples, samplesRecorded);
                DataAvailable?.Invoke(samples); // Processor handles resampling
            };
            _capture.StartRecording();
        }
        public void Stop() { if (_capture != null) { _capture.StopRecording(); _capture.Dispose(); _capture = null; } }
        public IEnumerable<string> GetDevices() {
            var enumerator = new MMDeviceEnumerator();
            return enumerator.EnumerateAudioEndPoints(DataFlow.Render, DeviceState.Active).Select(d => d.FriendlyName);
        }
        public void Dispose() => Stop();
    }
}
