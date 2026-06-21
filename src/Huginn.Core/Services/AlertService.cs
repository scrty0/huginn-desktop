using System;
using System.Threading.Tasks;
using Huginn.Core.Models;
namespace Huginn.Core.Services {
    public class AlertService {
        private readonly IStorageService _storageService;
        public event Action<AlertEntry>? OnDeepfakeDetected;
        public AlertService(IStorageService storageService) => _storageService = storageService;
        public async Task TriggerAlertAsync(double confidence) {
            var alert = new AlertEntry { Timestamp = DateTime.Now, Confidence = confidence };
            await _storageService.SaveAlertAsync(alert);
            OnDeepfakeDetected?.Invoke(alert);
        }
    }
}
