import pytest
import asyncio
from core.analyzer import FraudAnalyzer

@pytest.mark.asyncio
async def test_regex_detection():
    analyzer = FraudAnalyzer()
    text = "Я из службы безопасности банка, продиктуйте код из смс"
    triggers = analyzer.level1_regex(text)
    assert len(triggers) >= 2
    assert any(t['phrase'] == "я из службы безопасности банка" for t in triggers)
    assert any(t['phrase'] == "код из смс" for t in triggers)

@pytest.mark.asyncio
async def test_safe_text():
    analyzer = FraudAnalyzer()
    text = "Привет, как дела? Давай встретимся завтра."
    report = await analyzer.analyze(text)
    assert report.is_fraud == False
