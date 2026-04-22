PYTHON ?= python3

.PHONY: test demo benchmark private-export report release-check clean

test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

demo:
	$(PYTHON) demo/run_demo.py

benchmark:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src $(PYTHON) scripts/benchmark_patterns.py

private-export:
	$(PYTHON) scripts/export_private_repo.py --clean

report:
	cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error final-report.tex

release-check:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src $(PYTHON) scripts/check_release.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf *.egg-info src/*.egg-info dist build
	rm -f report/final-report.aux report/final-report.fdb_latexmk report/final-report.fls report/final-report.log report/final-report.out
