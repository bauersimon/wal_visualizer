import math
from typing import Callable, List, Tuple, TypeVar, Union

import numpy as np


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
