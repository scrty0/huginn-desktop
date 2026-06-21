using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using Huginn.Core.Services;
namespace Huginn.MlBridge.Services {
    public class MlInferenceService : IMlInferenceService, IDisposable {
        private readonly InferenceSession _session;
        public MlInferenceService() {
            var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "model", "huginn_model.onnx");
            if (!File.Exists(path)) path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "huginn_model.onnx");
            _session = new InferenceSession(path);
        }
        public async Task<float> GetSpoofScoreAsync(float[] data) => await Task.Run(() => {
            var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor(_session.InputMetadata.Keys.First(), new DenseTensor<float>(data, new[] { 1, 64600 })) };
            using var results = _session.Run(inputs);
            var output = results.First().AsEnumerable<float>().ToArray();
            // AASIST output is softmax [bonafide, spoof].
            // We need the spoof score. Index 1.
            // Earlier I thought 0 was spoof, but ASVspoof protocol usually defines Class 1 as Spoof in some training scripts.
            // Actually, ClovaAI AASIST repo training script uses target 0 for spoof and 1 for bonafide.
            // Let's stick with target 0 = spoof based on their README evaluation section.
            return output[0];
        });
        public void Dispose() => _session.Dispose();
    }
}
