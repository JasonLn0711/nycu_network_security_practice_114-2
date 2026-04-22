PYTHON ?= python3

.PHONY: test demo benchmark rust-test rust-demo private-export report release-check clean

test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src $(PYTHON) -m unittest discover -s python/tests -v

demo:
	$(PYTHON) demo/run_demo.py

benchmark:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src $(PYTHON) scripts/benchmark_patterns.py

rust-test:
	cd rust && cargo test

rust-demo:
	cd rust && cargo run -- scan --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json --json ../reports/demo-report-rust.json --markdown ../reports/demo-report-rust.md

private-export:
	$(PYTHON) scripts/export_private_repo.py --clean

report:
	cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error final-report.tex

release-check:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src $(PYTHON) scripts/check_release.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf *.egg-info python/*.egg-info python/src/*.egg-info dist build rust/target
	rm -f report/final-report.aux report/final-report.fdb_latexmk report/final-report.fls report/final-report.log report/final-report.out
