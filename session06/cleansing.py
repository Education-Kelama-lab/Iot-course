# cleansing.py
import numpy as np

TEMP_MIN, TEMP_MAX = -40, 80


def detect_outliers(data: list, sigma: float = 3.0) -> list[int]:
    """標準偏差を使って外れ値インデックスを返す（Noneは除外して計算）"""
    valid_values = [x for x in data if x is not None]

    if len(valid_values) < 2:
        return []

    arr = np.array(valid_values, dtype=float)
    mean = arr.mean()
    std = arr.std()

    if std == 0:
        return []

    outlier_indexes = []
    for i, x in enumerate(data):
        if x is None:
            continue
        if abs(x - mean) > sigma * std:
            outlier_indexes.append(i)

    return outlier_indexes


def apply_physical_range(data: list) -> tuple[list, list[int]]:
    """物理範囲外の値をNoneにする。変更したインデックスも返す"""
    modified = data[:]
    removed_indexes = []

    for i, x in enumerate(modified):
        if x is None:
            continue
        if x < TEMP_MIN or x > TEMP_MAX:
            modified[i] = None
            removed_indexes.append(i)

    return modified, removed_indexes


def fill_missing(data: list) -> list:
    """Noneを線形補間で補完する（端のNoneは近い値で埋める）"""
    result = data[:]
    n = len(result)

    for i in range(n):
        if result[i] is not None:
            continue

        # 左側の有効値を探す
        left = i - 1
        while left >= 0 and result[left] is None:
            left -= 1

        # 右側の有効値を探す
        right = i + 1
        while right < n and result[right] is None:
            right += 1

        # ケース分岐
        if left >= 0 and right < n:
            # 線形補間
            lv = result[left]
            rv = result[right]
            ratio = (i - left) / (right - left)
            result[i] = lv + (rv - lv) * ratio
        elif left >= 0:
            # 右が無い → 左の値で埋める
            result[i] = result[left]
        elif right < n:
            # 左が無い → 右の値で埋める
            result[i] = result[right]
        else:
            # 全部None
            result[i] = None

    return result


def cleanse(data: list) -> dict:
    """統計的クレンジングを実行して結果を返す"""

    print("=== cleanse() start ===")
    print("original:", data)

    # 物理範囲チェック
    ranged, physical_removed = apply_physical_range(data)
    if physical_removed:
        print("physical range removed indexes:", physical_removed)

    # 標準偏差による外れ値検出
    outliers = detect_outliers(ranged, sigma=3.0)
    if outliers:
        print("sigma outliers indexes:", outliers)

    # 外れ値をNoneにする
    cleaned = ranged[:]
    for idx in outliers:
        cleaned[idx] = None

    print("after outlier removal:", cleaned)

    # 全部Noneなら終了
    valid = [x for x in cleaned if x is not None]
    if not valid:
        print("ERROR: no valid data")
        return {"error": "no_valid_data", "original": data}

    # 欠損値補完
    filled = fill_missing(cleaned)

    print("after fill_missing:", filled)
    print("=== cleanse() end ===")

    return {
        "original": data,
        "cleaned": filled,
        "removed_physical": physical_removed,
        "removed_outliers": outliers
    }


if __name__ == "__main__":
    from test_data import generate_dirty_temperature_series

    temps = generate_dirty_temperature_series()
    result = cleanse(temps)
    print("\nRESULT:", result)