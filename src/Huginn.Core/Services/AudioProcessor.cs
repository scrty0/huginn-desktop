using System;
using System.Collections.Generic;
using System.Linq;
using NAudio.Wave;
using NAudio.Wave.SampleProviders;

namespace Huginn.Core.Services {
    public class AudioProcessor {
        private readonly List<float> _buffer = new List<float>();
        private const int RequiredSamples = 64600;
        private const int TargetSampleRate = 16000;
        public event Action<float[]>? ProcessedChunkAvailable;

        public void AddSamples(float[] samples, int sourceSampleRate) {
            float[] resampled = samples;
            if (sourceSampleRate != TargetSampleRate) {
                resampled = Resample(samples, sourceSampleRate, TargetSampleRate);
            }

            lock (_buffer) {
                _buffer.AddRange(resampled);
                while (_buffer.Count >= RequiredSamples) {
                    float[] chunk = _buffer.GetRange(0, RequiredSamples).ToArray();
                    _buffer.RemoveRange(0, 16000); // 1 sec shift
                    if (IsSpeech(chunk)) ProcessedChunkAvailable?.Invoke(chunk);
                }
            }
        }

        private float[] Resample(float[] samples, int fromSr, int toSr) {
            var format = WaveFormat.CreateIeeeFloatWaveFormat(fromSr, 2); // Assuming stereo loopback
            using var ms = new System.IO.MemoryStream();
            using (var writer = new WaveFileWriter(new NAudio.Utils.IgnoreDisposeStream(ms), format)) {
                writer.WriteSamples(samples, 0, samples.Length);
                writer.Flush();
            }
            ms.Position = 0;
            using var reader = new WaveFileReader(ms);
            var resampler = new WdlResamplingSampleProvider(reader.ToSampleProvider(), toSr);

            // Note: In real-time this is tricky. Simplified for the task:
            List<float> output = new List<float>();
            float[] buffer = new float[toSr];
            int read;
            while ((read = resampler.Read(buffer, 0, buffer.Length)) > 0) {
                output.AddRange(buffer.Take(read));
            }
            return output.ToArray();
        }

        private bool IsSpeech(float[] chunk) => chunk.Select(x => (double)x * x).Average() > 0.0001;
    }
}
