from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Huginn AI-Охранник</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; margin: 20px; }
        .card { background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #444; }
        .card.fraud { border-left-color: #ff5252; }
        .card.safe { border-left-color: #4caf50; }
        h1 { color: #bb86fc; }
        #status { color: #03dac6; }
    </style>
</head>
<body>
    <h1>🛡 Huginn AI-Охранник</h1>
    <p>Статус АТС: <span id="status">Онлайн</span></p>
    <div id="alerts"></div>

    <script>
        const ws = new WebSocket("ws://" + window.location.host + "/ws");
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const container = document.getElementById("alerts");
            const card = document.createElement("div");
            card.className = "card " + (data.type === 'fraud_detected' ? 'fraud' : 'safe');

            if (data.type === 'fraud_detected') {
                const report = data.report;
                card.innerHTML = `
                    <h3>🚨 ОБНАРУЖЕНА УГРОЗА!</h3>
                    <p><b>Звонок от:</b> ${report.caller_info}</p>
                    <p><b>Уверенность:</b> ${(report.confidence * 100).toFixed(1)}%</p>
                    <p><b>Причина:</b> ${report.reason}</p>
                    <p><b>Транскрипт:</b> ${report.transcript}</p>
                `;
            } else {
                card.innerHTML = `<p>${data.message}</p>`;
            }
            container.prepend(card);
        };
    </script>
</body>
</html>
"""
