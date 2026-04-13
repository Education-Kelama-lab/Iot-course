# smoothing.py

def moving_average(data: list[float], window: int = 5) -> list[float]:
    """単純移動平均（不足分は存在する範囲で平均）"""
    if window <= 0:
        raise ValueError("window must be > 0")

    result = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        segment = data[start:i + 1]
        avg = sum(segment) / len(segment)
        result.append(avg)

    return result


def weighted_moving_average(data: list[float], weights: list[float]) -> list[float]:
    """加重移動平均（weightsの長さがwindow扱い。不足分は短縮計算）"""
    if not weights:
        raise ValueError("weights must not be empty")

    window = len(weights)
    result = []

    for i in range(len(data)):
        start = max(0, i - window + 1)
        segment = data[start:i + 1]

        # segmentに合わせてweightsを後ろ側から使う
        used_weights = weights[-len(segment):]

        weighted_sum = 0
        weight_total = 0

        for x, w in zip(segment, used_weights):
            weighted_sum += x * w
            weight_total += w

        result.append(weighted_sum / weight_total)

    return result


def exponential_smoothing(data: list[float], alpha: float = 0.2) -> list[float]:
    """指数平滑化 S[t] = αx[t] + (1-α)S[t-1]"""
    if not data:
        return []

    if alpha < 0 or alpha > 1:
        raise ValueError("alpha must be between 0 and 1")

    result = [data[0]]
    for i in range(1, len(data)):
        s = alpha * data[i] + (1 - alpha) * result[-1]
        result.append(s)

    return result


if __name__ == "__main__":
    from test_data import generate_dirty_temperature_series
    from cleansing import cleanse

    temps = generate_dirty_temperature_series()
    cleaned = cleanse(temps)["cleaned"]

    print("\n=== smoothing test ===")
    print("cleaned:", cleaned)

    print("\nMoving Average:", moving_average(cleaned, window=5))
    print("\nWeighted MA:", weighted_moving_average(cleaned, weights=[1, 2, 3, 4, 5]))
    print("\nExp Smooth (0.2):", exponential_smoothing(cleaned, alpha=0.2))