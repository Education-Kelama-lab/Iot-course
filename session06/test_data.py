# test_data.py
# テストデータ生成スクリプト（演習用）

from datetime import datetime


def generate_dirty_temperature_series():
    """STEP1用: 異常値・欠損値を含む温度配列"""
    temps = [
        25.3, 25.4, 999.0,   # 異常値
        25.5, None,  25.4,   # 欠損値
        25.3, 25.2, -50.0,   # 異常値
        25.4, 25.6
    ]
    return temps


def generate_sensor_patterns():
    """STEP3用: 3種類の入力パターン"""
    pattern_a = {"temp": 25.3, "hum": 60}

    pattern_b = {
        "t": "25.3C",
        "h": "60%",
        "ts": "2024-03-07 10:00"
    }

    pattern_c = {
        "sensor_val_1": 25.3,
        "sensor_val_2": 60,
        "device": "TMP-001"
    }

    return pattern_a, pattern_b, pattern_c


def generate_broken_data():
    """STEP4用: 全部Noneの壊れたデータ"""
    return {
        "temp": None,
        "hum": None,
        "ts": None
    }


def now_iso():
    """現在時刻ISO文字列"""
    return datetime.now().isoformat()


if __name__ == "__main__":
    print("=== test_data.py ===")

    temps = generate_dirty_temperature_series()
    print("Dirty temperature series:", temps)

    a, b, c = generate_sensor_patterns()
    print("\nPattern A:", a)
    print("Pattern B:", b)
    print("Pattern C:", c)

    broken = generate_broken_data()
    print("\nBroken data:", broken)