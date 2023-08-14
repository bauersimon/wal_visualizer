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

debug:
	cd visualizer && wal cache_measure.wal -l ../examples/cache/vexriscv-cached.fst debug > ../debug.txt 2>&1
.PHONY: debug

demo-plotter:
	python plotter.py examples/latency.csv
.PHONY: demo-plotter