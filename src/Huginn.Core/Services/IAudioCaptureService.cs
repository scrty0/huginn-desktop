using System;
using System.Collections.Generic;
namespace Huginn.Core.Services {
    public interface IAudioCaptureService {
        event Action<float[]> DataAvailable;
        void Start(string? deviceName = null);
        void Stop();
        IEnumerable<string> GetDevices();
    }
}
