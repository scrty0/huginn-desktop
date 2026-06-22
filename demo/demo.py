import asyncio
import argparse
import sys
import os

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import FraudAnalyzer

async def run_demo(text=None):
    analyzer = FraudAnalyzer()
    if not text:
        text = "Здравствуйте! Это отдел безопасности КНБ. По вашему счету зафиксирована подозрительная операция. Вам нужно срочно перевести деньги на безопасный счет."

    print("-" * 40)
    print("Huginn AI-Охранник: ДЕМО")
    print("-" * 40)
    print(f"Текст разговора: {text}")
    print("-" * 40)

    report = await analyzer.analyze(text)

    if report.is_fraud:
        print("\033[91mВЕРДИКТ: МОШЕННИЧЕСТВО!\033[0m")
        print(f"Уверенность: {report.confidence:.1%}")
        print(f"Категория: {report.trigger_category}")
        print(f"Найдено триггеров: {', '.join(report.triggers)}")
    else:
        print("\033[92mВЕРДИКТ: БЕЗОПАСНО\033[0m")

    print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="Text to analyze")
    args = parser.parse_args()
    asyncio.run(run_demo(args.text))
