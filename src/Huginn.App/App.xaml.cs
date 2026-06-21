using System;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Huginn.Core.Services;
using Huginn.MlBridge.Services;
namespace Huginn.App {
    public partial class App : System.Windows.Application {
        public static IServiceProvider? ServiceProvider { get; private set; }
        protected override void OnStartup(StartupEventArgs e) {
            var services = new ServiceCollection();
            services.AddSingleton<IStorageService, StorageService>();
            services.AddSingleton<IAudioCaptureService, AudioCaptureService>();
            services.AddSingleton<IMlInferenceService, MlInferenceService>();
            services.AddSingleton<AlertService>();
            services.AddSingleton<AudioProcessor>();
            services.AddSingleton<MainWindow>();
            ServiceProvider = services.BuildServiceProvider();
            ServiceProvider.GetRequiredService<MainWindow>().Show();
        }
    }
}
