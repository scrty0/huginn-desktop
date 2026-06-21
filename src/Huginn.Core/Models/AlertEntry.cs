using System;
namespace Huginn.Core.Models {
    public class AlertEntry {
        public int Id { get; set; }
        public DateTime Timestamp { get; set; }
        public double Confidence { get; set; }
        public string AudioPath { get; set; } = string.Empty;
    }
}
