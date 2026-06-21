using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;
using Huginn.Core.Models;
namespace Huginn.Core.Services {
    public class StorageService : IStorageService {
        private readonly string _connectionString;
        public StorageService() {
            var appData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            var huginnDir = Path.Combine(appData, "Huginn");
            if (!Directory.Exists(huginnDir)) Directory.CreateDirectory(huginnDir);
            _connectionString = $"Data Source={Path.Combine(huginnDir, "huginn.db")}";
            InitializeDatabase();
        }
        private void InitializeDatabase() {
            using var connection = new SqliteConnection(_connectionString);
            connection.Open();
            var command = connection.CreateCommand();
            command.CommandText = "CREATE TABLE IF NOT EXISTS Alerts (Id INTEGER PRIMARY KEY AUTOINCREMENT, Timestamp TEXT, Confidence REAL, AudioPath TEXT); CREATE TABLE IF NOT EXISTS Settings (Key TEXT PRIMARY KEY, Value TEXT);";
            command.ExecuteNonQuery();
        }
        public async Task SaveAlertAsync(AlertEntry alert) {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            var command = connection.CreateCommand();
            command.CommandText = "INSERT INTO Alerts (Timestamp, Confidence, AudioPath) VALUES (@t, @c, @a)";
            command.Parameters.AddWithValue("@t", alert.Timestamp.ToString("o"));
            command.Parameters.AddWithValue("@c", alert.Confidence);
            command.Parameters.AddWithValue("@a", alert.AudioPath);
            await command.ExecuteNonQueryAsync();
        }
        public async Task<List<AlertEntry>> GetAlertsAsync() {
            var alerts = new List<AlertEntry>();
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            var command = connection.CreateCommand();
            command.CommandText = "SELECT Id, Timestamp, Confidence, AudioPath FROM Alerts ORDER BY Timestamp DESC";
            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync()) {
                alerts.Add(new AlertEntry { Id = reader.GetInt32(0), Timestamp = DateTime.Parse(reader.GetString(1)), Confidence = reader.GetDouble(2), AudioPath = reader.GetString(3) });
            }
            return alerts;
        }
        public async Task SaveSettingsAsync(AppSettings settings) {
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            using var transaction = connection.BeginTransaction();
            var upsert = "INSERT INTO Settings (Key, Value) VALUES (@k, @v) ON CONFLICT(Key) DO UPDATE SET Value=@v";
            async Task SaveKey(string key, string value) {
                var cmd = connection.CreateCommand(); cmd.Transaction = transaction; cmd.CommandText = upsert;
                cmd.Parameters.AddWithValue("@k", key); cmd.Parameters.AddWithValue("@v", value);
                await cmd.ExecuteNonQueryAsync();
            }
            await SaveKey("SelectedDeviceName", settings.SelectedDeviceName);
            await SaveKey("DetectionThreshold", settings.DetectionThreshold.ToString());
            await SaveKey("Autostart", settings.Autostart.ToString());
            await SaveKey("IsPaused", settings.IsPaused.ToString());
            await transaction.CommitAsync();
        }
        public async Task<AppSettings> LoadSettingsAsync() {
            var settings = new AppSettings();
            using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            var command = connection.CreateCommand();
            command.CommandText = "SELECT Key, Value FROM Settings";
            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync()) {
                var key = reader.GetString(0); var val = reader.GetString(1);
                switch (key) {
                    case "SelectedDeviceName": settings.SelectedDeviceName = val; break;
                    case "DetectionThreshold": double.TryParse(val, out var threshold); settings.DetectionThreshold = threshold; break;
                    case "Autostart": bool.TryParse(val, out var autostart); settings.Autostart = autostart; break;
                    case "IsPaused": bool.TryParse(val, out var isPaused); settings.IsPaused = isPaused; break;
                }
            }
            return settings;
        }
    }
}
