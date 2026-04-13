# llm_normalize.py
import json
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TARGET_SCHEMA = """
{
  "device_id": "string",
  "timestamp": "ISO8601",
  "measurements": {
    "temperature": {"value": N, "unit": "celsius"},
    "humidity": {"value": N, "unit": "percent"}
  }
}
"""


def fallback_normalize(raw: dict) -> dict:
    """LLMが使えない場合の縮退運用（推測できる範囲だけ変換）"""

    # 温度推測
    temp_val = raw.get("temp") or raw.get("temperature") or raw.get("sensor_val_1")
    hum_val = raw.get("hum") or raw.get("humidity") or raw.get("sensor_val_2")

    device_id = raw.get("device") or raw.get("device_id") or "unknown"
    ts = raw.get("ts") or raw.get("timestamp") or "unknown"

    return {
        "device_id": device_id,
        "timestamp": ts,
        "measurements": {
            "temperature": {"value": temp_val, "unit": "celsius"},
            "humidity": {"value": hum_val, "unit": "percent"}
        },
        "warning": "fallback_used"
    }


def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """LLM呼び出し（返答テキストを返す）"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return resp.choices[0].message.content


def normalize(raw: dict) -> dict:
    """LLMを使ってセンサーデータを統一スキーマに正規化"""

    prompt = f"""
以下のセンサーデータを統一スキーマに変換してください。
必ずJSONのみで出力してください。説明文は禁止です。

スキーマ:
{TARGET_SCHEMA}

入力データ:
{json.dumps(raw, ensure_ascii=False)}
"""

    # APIレート制限などを考慮してリトライ
    for attempt in range(3):
        try:
            text = call_llm(prompt)

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "raw": raw,
                    "error": "parse_failed",
                    "llm_output": text
                }

        except Exception as e:
            wait = 2 ** attempt
            print(f"[LLM ERROR] attempt={attempt+1} error={e} wait={wait}s")
            time.sleep(wait)

    # 3回失敗したらフォールバック
    return fallback_normalize(raw)


if __name__ == "__main__":
    from test_data import generate_sensor_patterns

    a, b, c = generate_sensor_patterns()

    print("=== normalize test ===")
    print("\nA:", normalize(a))
    print("\nB:", normalize(b))
    print("\nC:", normalize(c))