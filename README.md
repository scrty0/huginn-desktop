# Huginn Desktop

Антивирус от AI-мошенников. Детекция синтезированного голоса в реальном времени на устройстве.

## Стек

- C# .NET 9 + WPF + MaterialDesignXaml
- NAudio (WASAPI loopback)
- ONNX Runtime
- SQLite

## Структура

- `src/Huginn.App/` — WPF приложение (UI, трей, уведомления)
- `src/Huginn.Core/` — ядро (сервисы: захват аудио, обработка, алерты, БД)
- `src/Huginn.MlBridge/` — ONNX Runtime обёртка + модель
- `ml/` — ML-пайплайн (Python, конвертация в ONNX)

## Сборка

dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
