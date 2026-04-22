# Sentinel Demo Assets

This folder contains safe local demo fixtures for the Network Security Project I scanner.

Use `runbook.md` for the live-demo sequence and `demo-transcript.md` for the current observed command output.

The official EICAR safe anti-malware test file is generated at demo time by the
Rust command below:

```bash
cd ../rust
cargo run -- prepare-eicar-demo --target ../demo/demo-tree
```

The generated `demo-tree/nested/level-1/level-2/eicar.com.txt` file is ignored
by Git and excluded from private-repo export. This lets the live demo satisfy
the EICAR requirement without storing a literal EICAR file in the repository.
