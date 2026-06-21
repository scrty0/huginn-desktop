using System;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Media;
using System.Windows.Forms;
using Microsoft.Win32;
using Huginn.Core.Models;
using Huginn.Core.Services;
namespace Huginn.App {
    public partial class MainWindow : Window, INotifyPropertyChanged {
        private readonly IAudioCaptureService _cap; private readonly IMlInferenceService _ml; private readonly AudioProcessor _proc; private readonly AlertService _al; private readonly IStorageService _st;
        private AppSettings _set = new AppSettings();
        private NotifyIcon _trayIcon;
        public event PropertyChangedEventHandler? PropertyChanged;
        private string _statusText = "Активен"; public string StatusText { get => _statusText; set { _statusText = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(StatusText))); } }
        private System.Windows.Media.Brush _statusColor = System.Windows.Media.Brushes.Green; public System.Windows.Media.Brush StatusColor { get => _statusColor; set { _statusColor = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(StatusColor))); } }
        public MainWindow(IAudioCaptureService cap, IMlInferenceService ml, AudioProcessor proc, AlertService al, IStorageService st) {
            InitializeComponent(); DataContext = this; _cap = cap; _ml = ml; _proc = proc; _al = al; _st = st;
            _cap.DataAvailable += s => _proc.AddSamples(s, 48000);
            _proc.ProcessedChunkAvailable += async c => { if (_set.IsPaused) return; float sc = await _ml.GetSpoofScoreAsync(c); if (sc > _set.DetectionThreshold) await _al.TriggerAlertAsync(sc); };
            _al.OnDeepfakeDetected += a => Dispatcher.Invoke(() => new AlertWindow(a.Confidence).Show());
            _trayIcon = new NotifyIcon { Visible = true, Text = "Huginn Deepfake Guard" };
            try { _trayIcon.Icon = System.Drawing.Icon.ExtractAssociatedIcon(System.Windows.Forms.Application.ExecutablePath); } catch {}
            _trayIcon.Click += (s, e) => { Show(); WindowState = WindowState.Normal; Activate(); };
            var menu = new ContextMenuStrip(); menu.Items.Add("Открыть", null, (s, e) => { Show(); WindowState = WindowState.Normal; Activate(); }); menu.Items.Add("Выход", null, (s, e) => System.Windows.Application.Current.Shutdown());
            _trayIcon.ContextMenuStrip = menu;
            Loaded += async (s, e) => {
                _set = await _st.LoadSettingsAsync(); ThresholdSlider.Value = _set.DetectionThreshold; AutostartCheckBox.IsChecked = _set.Autostart;
                DeviceComboBox.ItemsSource = _cap.GetDevices().ToList(); DeviceComboBox.SelectedItem = _set.SelectedDeviceName;
                UpdateUI(); if (!_set.IsPaused) _cap.Start(_set.SelectedDeviceName);
            };
        }
        private void UpdateUI() { StatusText = _set.IsPaused ? "На паузе" : "Активен"; StatusColor = _set.IsPaused ? System.Windows.Media.Brushes.Orange : System.Windows.Media.Brushes.Green; PauseBtn.Content = _set.IsPaused ? "Возобновить" : "Пауза"; }
        private async void TogglePause_Click(object s, System.Windows.RoutedEventArgs e) { _set.IsPaused = !_set.IsPaused; if (_set.IsPaused) _cap.Stop(); else _cap.Start(_set.SelectedDeviceName); UpdateUI(); await _st.SaveSettingsAsync(_set); }
        private async void SaveSettings_Click(object s, System.Windows.RoutedEventArgs e) {
            _set.DetectionThreshold = ThresholdSlider.Value; _set.Autostart = AutostartCheckBox.IsChecked ?? false; _set.SelectedDeviceName = DeviceComboBox.SelectedItem?.ToString() ?? "";
            await _st.SaveSettingsAsync(_set);
            try { using var key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true); if (_set.Autostart) key?.SetValue("Huginn", $"\"{Environment.ProcessPath}\""); else key?.DeleteValue("Huginn", false); } catch {}
            System.Windows.MessageBox.Show("Настройки сохранены");
        }
        private async void MenuListBox_SelectionChanged(object s, System.Windows.Controls.SelectionChangedEventArgs e) {
            if (DashboardView == null) return; DashboardView.Visibility = HistoryView.Visibility = SettingsView.Visibility = Visibility.Collapsed;
            if (MenuListBox.SelectedIndex == 0) DashboardView.Visibility = Visibility.Visible;
            else if (MenuListBox.SelectedIndex == 1) { HistoryView.Visibility = Visibility.Visible; HistoryView.ItemsSource = await _st.GetAlertsAsync(); }
            else SettingsView.Visibility = Visibility.Visible;
        }
        protected override void OnClosing(CancelEventArgs e) { e.Cancel = true; Hide(); }
    }
}
