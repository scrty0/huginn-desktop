using System.Media;
using System.Windows;
namespace Huginn.App {
    public partial class AlertWindow : Window {
        public AlertWindow(double conf) {
            InitializeComponent();
            ConfidenceText.Text = $"Вероятность: {conf:P1}";
            Left = SystemParameters.WorkArea.Right - Width;
            Top = SystemParameters.WorkArea.Bottom - Height;
            try { SystemSounds.Exclamation.Play(); } catch {}
        }
        private void Close_Click(object s, RoutedEventArgs e) => Close();
    }
}
