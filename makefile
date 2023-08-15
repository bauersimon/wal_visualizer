setup:
	conda env create -f environment.yml
.PHONY: setup

test:
	python -m unittest discover visualizer -p "*_test.py"
	cd visualizer && wal cache_measure.wal test
.PHONY: test

run:
	cd visualizer && wal cache_measure.wal -l ../examples/cache/vexriscv-cached.fst
.PHONY: run

run-vcd: clean trim-vexriscv
	cd visualizer && wal cache_measure.wal -l ../examples/cache/vexriscv_trimmed_10.vcd
.PHONY: run-vcd

run-vcd-native: clean trim-vexriscv
	@echo "!!! this fills 6GB of RAM !!!"
	cd visualizer && wal cache_measure.wal native -l ../examples/cache/vexriscv_trimmed_10.vcd
.PHONY: run-vcd-native

debug:
	cd visualizer && wal cache_measure.wal debug -l ../examples/cache/vexriscv-cached.fst > ../debug.txt 2>&1
.PHONY: debug

demo-plotter:
	python plotter.py examples/latency.csv
.PHONY: demo-plotter

trim-vexriscv:
	fst2vcd examples/cache/vexriscv-cached.fst | wc -l
	fst2vcd examples/cache/vexriscv-cached.fst > examples/cache/vexriscv_trimmed_100.vcd
	fst2vcd examples/cache/vexriscv-cached.fst | head -n 2708544 > examples/cache/vexriscv_trimmed_10.vcd
	fst2vcd examples/cache/vexriscv-cached.fst | head -n 270854 > examples/cache/vexriscv_trimmed_1.vcd
.PHONY: trim-vexriscv

clean:
	rm -f raw*.txt metrics*.png examples/cache/*.vcd
.PHONY: clean