import logging
import sys
from sys import argv
from typing import List

OK = '\033[32m'
FAIL = '\033[91m'
ENDC = '\033[0m'

if "debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

sys.setrecursionlimit(10_000_000)


def test(name, expected, actual):
    if not "test" in argv:
        return
    elif not expected == actual:
        print(f"{FAIL}FAIL{ENDC} {name}\nExpected:\t{expected}\nActual:\t\t{actual}")
    else:
        print(f"{OK}PASS{ENDC} {name}")


def do_test() -> bool:
    return "test" in argv


def debug(msg: str, *args):
    if not "debug" in argv:
        return
    logger.log(logging.DEBUG, msg, *args)


def write(file: str, *content):
    with open(file, "w") as f:
        f.write("".join(str(content)))


def merge_indices(a: List[int], b: List[int]) -> List[int]:
    merged: List[int] = []

    i_a = 0
    i_b = 0
    while i_a < len(a) and i_b < len(b):
        if a[i_a] == b[i_b]:
            merged.append(a[i_a])
            i_a += 1
            i_b += 1
        elif a[i_a] > b[i_b]:
            i_b += 1
        elif a[i_a] < b[i_b]:
            i_a += 1

    return merged


def compute_latency(request: List[int], response: List[int], shortest_path: int = 1) -> List[int]:
    latencies: List[int] = []

    i_rq = 0
    i_rs = 0
    while i_rq < len(request):
        if i_rs >= len(response):
            debug("latency: RS=∅\t-> -1 (RQ++)")
            # Append "-1" for missing responses.
            latencies.append(-1)
            i_rq += 1
            continue

        req = request[i_rq]
        req_next = -1
        res = response[i_rs]

        if i_rq < len(request)-1:
            req_next = request[i_rq+1]
            if res >= req_next + shortest_path:
                debug("latency: RQ=%d,RS=%d (RQ+1=%d)\tRS >= RQ+\t-> -1 (RQ++)", req, res, req_next)
                # Response is for next request.
                latencies.append(-1)
                i_rq += 1
                continue

        if res >= req + shortest_path:
            debug("latency: RQ=%d,RS=%d (RQ+1=%d)\tRS >= RQ\t-> %d (RQ++,RS++)", req, res, req_next, res-req)
            # Valid response.
            latencies.append(res - req)
            i_rq += 1
            i_rs += 1
        else:
            debug("latency: RQ=%d,RS=%d (RQ+1=%d)\tRS < RQ\t-> - (RS++)", req, res, req_next)
            # Ignore invalid response.
            i_rs += 1

    return latencies
