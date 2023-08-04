setup:
	conda env create -f environment.yml
.PHONY: setup

test:
	python -m unittest discover visualizer -p "*_test.py"
	cd visualizer && wal cache_measure.wal test
.PHONY: test