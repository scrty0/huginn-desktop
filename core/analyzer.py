import json
import uuid
from typing import List
from openai import AsyncOpenAI
from .models import FraudReport
from .trigger_patterns import TRIGGER_PHRASES, classify_trigger
from config import settings

class FraudAnalyzer:
    def __init__(self, provider=settings.LLM_PROVIDER):
        self.provider = provider
        self.client = None
        if provider == "openai" and settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-..."):
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def level1_regex(self, text: str) -> List[dict]:
        text_lower = text.lower()
        found = []
        for phrase in TRIGGER_PHRASES:
            if phrase in text_lower:
                found.append({
                    "phrase": phrase,
                    "category": classify_trigger(phrase),
                    "pos": text_lower.index(phrase)
                })
        return found

    async def level2_llm(self, text: str, caller_info: str) -> dict:
        prompt = f"""
        Ты — AI-детектор мошенничества для корпоративной АТС.
        Определи, является ли этот диалог мошенническим.
        Контекст: бухгалтер разговаривает с {caller_info}.

        Текст разговора: {text}

        Ответь ТОЛЬКО JSON:
        {{
            "is_fraud": true/false,
            "confidence": 0.0-1.0,
            "reason": "причина на русском",
            "trigger_category": "категория"
        }}
        """
        if self.provider == "openai" and self.client:
            try:
                resp = await self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                return json.loads(resp.choices[0].message.content)
            except Exception as e:
                print(f"LLM Error: {e}")

        # Fallback if no LLM
        return {"is_fraud": True, "confidence": 0.5, "reason": "Detected by triggers (LLM fallback)", "trigger_category": "suspicious"}

    async def analyze(self, text: str, caller_info: str = "Unknown") -> FraudReport:
        triggers = self.level1_regex(text)
        if not triggers:
            return FraudReport(
                id=str(uuid.uuid4()), is_fraud=False, confidence=0.0,
                reason="No triggers found", triggers=[], trigger_category="safe",
                transcript=text, caller_info=caller_info
            )

        llm_res = await self.level2_llm(text, caller_info)
        return FraudReport(
            id=str(uuid.uuid4()),
            is_fraud=llm_res["is_fraud"],
            confidence=max(min(len(triggers) * 0.2, 0.9), llm_res["confidence"]),
            reason=llm_res["reason"],
            triggers=[t["phrase"] for t in triggers],
            trigger_category=llm_res["trigger_category"],
            transcript=text,
            caller_info=caller_info
        )
