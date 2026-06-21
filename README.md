# Huginn Deepfake Guard

Антивирус от голосовых дипфейков и мошенников.

## Функционал
- Захват системного аудио (WASAPI Loopback).
- Анализ в реальном времени через AASIST (ONNX).
- Уведомления при обнаружении синтезированного голоса.
- История срабатываний (SQLite).
- Полностью офлайн работа.

## Сборка
1. Установите .NET 9 SDK.
2. Установите Python и зависимости: `pip install torch onnx librosa soundfile numpy onnxscript`.
3. Сгенерируйте ONNX модель: `python ml/convert_to_onnx.py`.
4. Соберите проект: `dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true`.

## Установка
Используйте Inno Setup с файлом `huginn_setup.iss` для создания установщика.
