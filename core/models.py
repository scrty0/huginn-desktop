from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal, Optional

class FraudReport(BaseModel):
    id: str
    is_fraud: bool
    confidence: float
    reason: str
    triggers: List[str]
    trigger_category: str
    transcript: str
    caller_info: str
    timestamp: datetime = Field(default_factory=datetime.now)
    call_duration: int = 0
    audio_path: Optional[str] = None
    feedback: Optional[bool] = None

class AlertEvent(BaseModel):
    type: Literal["fraud_detected", "safe", "processing", "error"]
    report: Optional[FraudReport] = None
    message: str

class CallRecord(BaseModel):
    id: str
    caller: str
    timestamp: datetime
    duration: int
    status: str
    report_id: Optional[str] = None

class TextAnalysisRequest(BaseModel):
    text: str
    caller_info: str = "Unknown"

class FeedbackRequest(BaseModel):
    alert_id: str
    correct: bool
