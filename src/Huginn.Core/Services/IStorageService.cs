using System.Collections.Generic;
using System.Threading.Tasks;
using Huginn.Core.Models;
namespace Huginn.Core.Services {
    public interface IStorageService {
        Task SaveAlertAsync(AlertEntry alert);
        Task<List<AlertEntry>> GetAlertsAsync();
        Task SaveSettingsAsync(AppSettings settings);
        Task<AppSettings> LoadSettingsAsync();
    }
}
