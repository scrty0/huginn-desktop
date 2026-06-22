# Интеграция Huginn AI с Asterisk PBX

Для захвата аудиопотока в реальном времени рекомендуется использовать метод **External Media** или **EAGI**.

## Метод 1: Parallel Capture (AudioSocket)
Asterisk 16+ поддерживает `AudioSocket`, который позволяет передавать аудио по TCP.

### Настройка extensions.conf
```asterisk
[incoming]
exten => _X., 1, NoOp(Incoming call to Huginn)
 same => n, Dial(PJSIP/100, 30, U(huginn_handler))

[huginn_handler]
exten => s, 1, AudioSocket(uuid, 127.0.0.1:8080)
 same => n, Return()
```

## Метод 2: AMI (Asterisk Manager Interface)
Huginn может прослушивать события AMI и инициировать запись через `Monitor` или `MixMonitor`, затем считывать файл по мере записи.

## Настройка FreePBX
1. Перейдите в **Connectivity** -> **Custom Extensions**.
2. Создайте экстеншн, который вызывает `Dial` с опцией `b(huginn-hook^s^1)`.
3. В `extensions_custom.conf` пропишите логику пересылки RTP.
