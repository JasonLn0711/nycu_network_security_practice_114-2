CARGO ?= cargo
PYTHON ?= python3

.PHONY: test demo rust-fmt rust-test rust-lint rust-prepare-eicar rust-verify rust-demo rust-evidence report private-export release-check clean

test: rust-test

demo: rust-demo

rust-fmt:
	cd rust && $(CARGO) fmt --check

rust-test:
	cd rust && $(CARGO) test

rust-lint:
	cd rust && $(CARGO) clippy --all-targets -- -D warnings

rust-prepare-eicar:
	cd rust && $(CARGO) run -- prepare-eicar-demo --target ../demo/demo-tree

rust-verify: rust-fmt rust-test rust-lint rust-prepare-eicar
	cd rust && $(CARGO) run -- verify-demo --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json

rust-demo: rust-prepare-eicar
	cd rust && $(CARGO) run -- scan --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json --json ../reports/demo-report.json --markdown ../reports/demo-report.md; status=$$?; if [ $$status -ne 1 ]; then exit $$status; fi

rust-evidence: rust-demo
	cd rust && $(CARGO) run -- write-evidence --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json --report ../reports/demo-report.json --report ../reports/demo-report.md --output ../reports/demo-evidence-manifest.json

report:
	cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error final-report.tex

private-export:
	$(PYTHON) scripts/export_private_repo.py --clean

release-check:
	$(PYTHON) scripts/check_release.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf dist build rust/target
	rm -f report/*.aux report/*.fdb_latexmk report/*.fls report/*.log report/*.out report/*.synctex.gz
