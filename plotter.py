import argparse
from csv import reader
from typing import List

from visualizer.plotting import visualize_latency

parser = argparse.ArgumentParser(
    prog='Latency Plotter',
    description='Plot Latency Metrics',
)
parser.add_argument('file', type=str)
parser.add_argument('-w', '--window', default=3, type=int)
parser.add_argument('-o', '--output', default="metrics.png", type=str)

options = parser.parse_args()

requests: List[int] = []
latency: List[float] = []
with open(options.file, "r") as f:
    data = reader(f)
    next(data, None)  # skip the headers
    for r in data:
        requests.append(int(r[0]))
        latency.append(float(r[1]))

visualize_latency(requests, latency, window_size=options.window, save_path=options.output)
