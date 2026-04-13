# visualize.py
# Bonus Lv.1: matplotlibで可視化する

import matplotlib.pyplot as plt

from test_data import generate_dirty_temperature_series
from cleansing import cleanse
from smoothing import moving_average, weighted_moving_average, exponential_smoothing


def plot_series(original, cleaned, ma, wma, exp):
    x = list(range(len(original)))

    # original（Noneをplotできるように変換）
    original_plot = [v if v is not None else float("nan") for v in original]

    plt.figure(figsize=(10, 6))
    plt.plot(x, original_plot, marker="o", linestyle="-", label="Original (dirty)")
    plt.plot(x, cleaned, marker="o", linestyle="-", label="Cleansed")
    plt.plot(x, ma, linestyle="--", label="Moving Average (window=5)")
    plt.plot(x, wma, linestyle="--", label="Weighted MA (1..5)")
    plt.plot(x, exp, linestyle="--", label="Exponential (alpha=0.2)")

    plt.title("Sensor Data Cleansing + Smoothing Comparison")
    plt.xlabel("Index (time)")
    plt.ylabel("Temperature (Celsius)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    temps = generate_dirty_temperature_series()

    cleanse_result = cleanse(temps)
    if "error" in cleanse_result:
        print("cleanse failed:", cleanse_result)
        return

    cleaned = cleanse_result["cleaned"]

    ma = moving_average(cleaned, window=5)
    wma = weighted_moving_average(cleaned, weights=[1, 2, 3, 4, 5])
    exp = exponential_smoothing(cleaned, alpha=0.2)

    plot_series(temps, cleaned, ma, wma, exp)


if __name__ == "__main__":
    main()