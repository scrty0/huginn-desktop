from fastapi import APIRouter, UploadFile, File, Request
from core.models import FraudReport, TextAnalysisRequest, AlertEvent
import uuid
import aiosqlite
import json
import numpy as np
import librosa
from config import settings

router = APIRouter(prefix="/api/v1")

@router.post("/analyze", response_model=FraudReport)
async def analyze_audio(request: Request, file: UploadFile = File(...), caller_info: str = "Unknown"):
    content = await file.read()
    temp_path = f"data/audio/{uuid.uuid4()}.wav"
    with open(temp_path, "wb") as f:
        f.write(content)

    # Load and resample
    audio_data, _ = librosa.load(temp_path, sr=16000)

    text = request.app.state.stt.transcribe(audio_data)
    report = await request.app.state.analyzer.analyze(text, caller_info)
    report.audio_path = temp_path

    await save_to_db(report)

    if report.is_fraud:
        await request.app.state.notifier.broadcast(AlertEvent(type="fraud_detected", report=report, message="Threat detected"))

    return report

@router.post("/analyze-text", response_model=FraudReport)
async def analyze_text(request: Request, data: TextAnalysisRequest):
    report = await request.app.state.analyzer.analyze(data.text, data.caller_info)
    await save_to_db(report)
    if report.is_fraud:
        await request.app.state.notifier.broadcast(AlertEvent(type="fraud_detected", report=report, message="Threat detected"))
    return report

async def save_to_db(report: FraudReport):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute(
            "INSERT INTO calls (id, timestamp, caller_info, transcript, is_fraud, confidence, triggers, trigger_category, audio_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (report.id, report.timestamp.isoformat(), report.caller_info, report.transcript, report.is_fraud, report.confidence, json.dumps(report.triggers), report.trigger_category, report.audio_path)
        )
        await db.commit()

@router.get("/history")
async def get_history():
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM calls ORDER BY timestamp DESC LIMIT 20") as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

@router.get("/health")
async def health():
    return {"status": "healthy"}
