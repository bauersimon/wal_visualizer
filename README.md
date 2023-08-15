# WAL visualizer

Project for "Hardware Design" SS2023 @ JKU

## Examples

Taken directly from [wal-lang](https://github.com/ics-jku/wal) ([docs](https://wal-lang.org/documentation/core)).

Additional examples provided by Lucas Klemmer (corresponding to [VexRiscv](https://github.com/SpinalHDL/VexRiscv) and [ibex](https://github.com/lowRISC/ibex)).

## Make Targets

- `make run`: run whole "pipeline" on `vexriscv-cached.fst`
- `make run-vcd`: convert `vexriscv-cached.fst` to `.vcd` and run whole "pipeline" on trimmed version (10% = `35.000` steps)
  - 100% cache hit rate (since there are no `ICache` accessed til step ~`40.000`)
  - no `DCache` indices can be extracted (since there are no `DCache` accessed til step ~`40.000`)
- `make run-vcd-native`: convert `vexriscv-cached.fst` to `.vcd` and run whole "pipeline" with **native** WAL implementation of "latency computation" (requires ~`6GB RAM`) on trimmed version (10% = `35.000` steps)
  - 100% cache hit rate (since there are no `ICache` accessed til step ~`40.000`)
  - no `DCache` indices can be extracted (since there are no `DCache` accessed til step ~`40.000`)
