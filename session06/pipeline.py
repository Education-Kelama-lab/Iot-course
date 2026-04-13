# pipeline.py
from cleansing import cleanse
from smoothing import moving_average
from llm_normalize import normalize
from test_data import generate_dirty_temperature_series, generate_sensor_patterns, generate_broken_data


def run_test1():
    print("\n==============================")
    print("TEST1: 異常値999°Cを含むデータ → クレンジング → 平滑化 → LLM正規化")
    print("==============================")

    temps = generate_dirty_temperature_series()

    result = cleanse(temps)
    if "error" in result:
        print("cleanse error:", result)
        return

    cleaned = result["cleaned"]
    smoothed = moving_average(cleaned, window=5)

    # LLMに渡す形式（例としてtemp/hum形式）
    raw_for_llm = {"temp": smoothed[-1], "hum": 60}

    normalized = normalize(raw_for_llm)

    print("Final normalized JSON:")
    print(normalized)


def run_test2():
    print("\n==============================")
    print("TEST2: フォーマットが異なる2種類のデバイスデータを同時変換")
    print("==============================")

    a, b, _ = generate_sensor_patterns()

    na = normalize(a)
    nb = normalize(b)

    print("\nNormalized A:")
    print(na)

    print("\nNormalized B:")
    print(nb)


def run_test3():
    print("\n==============================")
    print("TEST3: 全フィールドNoneの壊れたデータを入力したときの挙動確認")
    print("==============================")

    broken = generate_broken_data()

    normalized = normalize(broken)

    print("\nNormalized broken data:")
    print(normalized)


def main():
    run_test1()
    run_test2()
    run_test3()


if __name__ == "__main__":
    main()