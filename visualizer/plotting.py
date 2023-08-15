import math
from typing import Callable, List, Tuple, TypeVar, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

matplotlib.use("TkAgg")


def hit_ratio(latency: List[Union[int, float]], hit_threshold: float = 0.0) -> float:
    """Computes the average hit ratio.

    A "hit" can be defined with a threshold, any latency lower or equal is counted as a hit.
    Negative latency is registered as invalid (never responded) and counts towards misses.

    If `len(latency) == 0` the result is `1.0`.
    """
    if len(latency) == 0:
        return 1.0

    l = np.array(latency)
    # Convert negative entries to misses (above the threshold).
    l = np.where(l < 0, np.ones_like(l) * hit_threshold + 1, l)

    hits = l <= hit_threshold

    if hits.shape[0] == 0:
        return 1.0
    return np.sum(hits).item() / float(len(latency))


def response_time(latency: List[Union[int, float]], hit_threshold: float = 0.0) -> Tuple[float, float]:
    """Computes the mean and deviation response time.

    A "hit" can be defined with a threshold, any latency lower or equal is ignored.
    Negative latency is registered as invalid (never responded) but is ignored for numerical reasons.

    If `len(latency) == 0` the result is `(0.0, 0.0)`.
    """
    l = np.array(latency)
    # Filter out negative entries.
    l = np.extract(l >= 0, l)

    l = np.extract(l > hit_threshold, l)
    if l.shape[0] == 0:
        return (0.0, 0.0)

    return np.mean(l).item(), math.sqrt(np.var(l).item())


T = TypeVar("T")


def sliding_window(timepoints: List[int], latency: List[Union[int, float]], compute: Callable[[List[Union[int, float]]], T], default_entry: T, window_size: int = 5, stride: int = 1, **kwargs) -> List[T]:
    """Applies a computation function to latency data in a sliding window fashion.

    The provided `timepoints` represent the moments at which requests occured (i.e. `[3, 7, 22]`).
    While the value at position `latency[i]` contains the latency of the request which happend at timepoint `timepoints[i]`.

    The `window_size`must be odd. And the output has length of all timepoints (i.e. `timepoints[-1]`)
    and the `default entry` is used in case no latency measure is available for a certain time period.

    The remaining named arguments are passed to the computation function.
    """
    assert window_size > 0 and window_size % 2 == 1, "Window size must be positive and odd."
    assert stride > 0, "Stride must be positive."
    assert len(timepoints) == len(latency), "Timepoints and latency must be of equal lenght."

    t = np.array(timepoints)
    l = np.array(latency)

    idx = 0
    window_size = int((window_size - 1) / 2)
    # Ensure a non-negative array access.
    start = max(idx - window_size, 0)
    end = idx + window_size
    results: List[T] = []

    while idx <= timepoints[-1]:
        window_indices = np.flatnonzero((start <= t) & (t <= end))
        window_values = l[window_indices]
        w = window_values.tolist()
        if len(w) == 0:
            results.append(default_entry)
        else:
            r = compute(w, **kwargs)
            results.append(r)

        idx += stride
        # Ensure a non-negative array access.
        start = max(idx - window_size, 0)
        end = idx + window_size

    return results


def visualize_latency(timepoints: List[int], latency: List[Union[int, float]], save_path: str = "metrics.png", window_size: int = 5, window_stride: int = 1, hit_threshold: float = 0.0):
    """Visualize latency metrics and save the plots to a file.

    The temporal "resolution" can be changed by changing the `sliding_window` (must be odd).
    """
    # Filter out negative entries.
    l = np.array(latency)
    timepoints_valid: List[int] = np.extract(l >= 0, np.array(timepoints)).tolist()
    latency_valid: List[Union[int, float]] = np.extract(l >= 0, l).tolist()
    latency_hits: List[Union[int, float]] = np.extract(l > hit_threshold, l).tolist()

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 8))
    fig.tight_layout(pad=3)

    hr = hit_ratio(latency, hit_threshold)
    ax[0][0].bar(["hit", "miss"], [hr * 100, (1 - hr) * 100])
    ax[0][0].set_ylabel("%", rotation=0, fontsize=20)
    ax[0][0].set_title(f"Ø Hit Rate ({hr*100:.1f} %)", fontsize=20)

    rt_m, rt_d = response_time(latency_valid, hit_threshold)
    bin_values, _, _ = ax[0][1].hist(latency_hits)
    ax[0][1].set_ylabel("#", rotation=0, fontsize=20)
    ax[0][1].set_title(f"Ø Response Time Distribution excl. Hits (μ={rt_m:.2f}, σ={rt_d:.2f})", fontsize=20)
    x = np.arange(np.min(latency_hits), np.max(latency_hits) + 1, 0.1)
    if rt_d != 0.0:  # A density with zero deviation doesn't make any sense.
        ax[0][1].plot(x, norm.pdf(x, rt_m, rt_d) * np.max(bin_values))

    hr_sw = sliding_window(timepoints_valid, latency_valid, hit_ratio, -1.0, window_size, window_stride, hit_threshold=hit_threshold)
    t = np.arange(0, timepoints_valid[-1] + 1, window_stride)
    ax[1][0].plot(t, np.array(hr_sw) * 100)
    ax[1][0].set_ylabel("%", rotation=0, fontsize=20)
    ax[1][0].set_title(f"Ø Hit Rate over Time ({timepoints_valid[-1]+1} steps, Ø over {window_size})", fontsize=20)

    rt_sw = sliding_window(timepoints_valid, latency_valid, response_time, (-1.0, 0.0), window_size, window_stride, hit_threshold=hit_threshold)
    rt_sw = np.array(rt_sw)[:, 0]  # Extract just the average response time and drop the deviation.
    ax[1][1].plot(t, rt_sw)
    ax[1][1].set_ylabel("Response Time", fontsize=20)
    ax[1][1].set_title(f"Ø Response Time over Time excl. Hits ({timepoints_valid[-1]+1} steps, Ø over {window_size})", fontsize=20)

    fig.savefig(save_path)
