namespace Huginn.Core.Models {
    public class AppSettings {
        public string SelectedDeviceName { get; set; } = string.Empty;
        public double DetectionThreshold { get; set; } = 0.7;
        public bool Autostart { get; set; } = false;
        public bool IsPaused { get; set; } = false;
    }
}
