# Jingzhong Success Package Artifact Manifest

Date archived: 2026-05-23

Raw archive:

| File | SHA-256 |
| --- | --- |
| `lab-jingzhong-success-2026-05-23.rar` | `1beecb6e522254ed05a21ad26e52627d80691167122a1da70c0ede1a05065228` |
| `report/autonomous-apt-agent-report-jingzhong-success-2026-05-23.docx` | `e6f05a3211c762c05eddf91baf04cabf31719e8de955c34dc388054f67e06fa7` |
| `report/autonomous-apt-agent-report-extracted-text.txt` | `0588c6b0b9b1e6107a8d55675141e752c7fd162d8f7bea40895fa495ee57856a` |

## Extracted Lab Inventory

| Path | SHA-256 | Role |
| --- | --- | --- |
| `lab/EC/Dockerfile` | `3e5ecbb520980cd5bfd4463bb93460464d83eb91d8a3dd2832679dc775a94af4` | Builds the EC image with Python, file, binutils, `/exploit`, `/triage`, and analyzer. |
| `lab/EC/analyze_target.py` | `0d8bcaf689fb4c4901ff53b5f896c9dcd8f2fafb4e133763286520054206b5ef` | Reads `/shared/blogic.copy` or `/shared/blogic`, extracts ELF metadata, symbols, strings, risky imports, gadgets, and offset-inference status. |
| `lab/EC/exploit` | `6b27b1c9f9ad51c4ba2ab2dfb48acfdff6be6de1b92fcbe1cbdf7cd507007f8e` | Runs analyzer, chooses target/gadget/offset strategy, writes `config.data`, and creates `exploit_done`. |
| `lab/EC/triage` | `a98a5e876387c731052a964906d931e85ab93fb03e6746a1923eb5e835a80df5` | Reads success/coredump/no-success feedback and updates `state.json` for adaptive probing. |
| `lab/EC/readme.txt` | `709b02bce75f8ad928629d8f4dc0787c13556c2197054c78f5ea83bb59c8e609` | Short original EC build/test note. |
| `lab/README.md` | `0bb884323e09cd9ef74283a26b478376384fe3af12688879ba3faa15184b9074` | Main package README explaining architecture, modes, test results, and limitations. |
| `lab/docker.sh` | `c2e44ff3d34c83eec968a862d708d12c1805c88685ee6c98cb7f67501ff85ef3` | Starts the IC phase container and copies the selected server to `/blogic` and `/shared/blogic`. |
| `lab/grader.sh` | `6ce77b99f1db7426b03a7843e60ee85c0143e205c935309b7c59a1c626ff42f8` | Round loop that runs `/exploit`, waits for IC, checks `success.txt`, and calls `/triage`. |
| `lab/IC/Dockerfile` | `fffb24c49198b6329efcc985bd7a042f0b4b529ed097669325b6d999a139779e` | IC image source. |
| `lab/IC/backdoor` | `008051e410ea72a5ea996dc99f2388563c1c12083d9dfc39cca3a56048c52a8c` | Writes `/shared/success.txt` when executed inside IC. |
| `lab/IC/runserver.sh` | `062e38b98021f92fdf32542ed030c35a498b2ba3a4964492c750e033e3b65c55` | Configures coredumps and loops `/blogic`. |
| `lab/IC/server.cpp` | `4cdbd9c0dada63f1e04333fcef28377dae3917d75bf269bf0ad13a3f1139f96f` | Source included in Jingzhong package for the current server shape. |
| `lab/IC/server_prev.cpp` | `f87171c3096731478c6398f935ea2c1a1bafea299ae8ab336c3bd0b65c9fe298` | Older server source included in the package. |
| `lab/IC/server_1` | `e3a7bd6957d6680982149239f86115f97ec0ea070fbf2f2821400b6002d866d1` | Phase 1 server binary included in Jingzhong package. |
| `lab/IC/server_2` | `465d7fd6058c6fa4aeddaa05d560ef548bc132cfd675d2d0aadad4b82c6c724b` | Phase 2/3 server binary included in Jingzhong package. |
| `lab/shared/blogic` | `e3a7bd6957d6680982149239f86115f97ec0ea070fbf2f2821400b6002d866d1` | Saved target binary from the archived final shared state. |
| `lab/shared/config.data` | `f1b443593643b7b366d1d8843b47447f1c240b6d4468a2b1353e0cb4d6752ab9` | Saved final-mode payload file. |
| `lab/shared/success.txt` | `dd67510490fde6a2b0e12dde95a59a10fe524031383d74077a6c0ab94d907f4c` | Success artifact: `Backdoor triggered` plus timestamp. |
| `lab/shared/exploit-log.txt` | `75bbcda86a9549c7cd18808350aee3fa01972b5731466f719cc0468bdae36e18` | Trackable text copy of the saved final exploit log. The original `exploit.log` is present in the extracted folder but ignored by the repo's `*.log` rule. |
| `lab/shared/state.json` | `d57fde9148c97a11f52a84ceacdd2e187256af816b260fceac58ea38122a9751` | Saved final-mode agent state. |
| `lab/shared/target-analysis-log.txt` | `1bf448d179acab01dcdc88f1adc3077ba300cb5c6cd149505d9d165e54ee77ca` | Trackable text copy of the analyzer log for the saved target. The original `target_analysis.log` is present in the extracted folder but ignored by the repo's `*.log` rule. |
| `lab/shared/target_info.json` | `4462bf927ae6db3705578759b25f8fd337e5af2fe67599d18602760759073546` | Structured analyzer output for the saved target. |
| `lab/phase2_adaptive_result.txt` | `ae7eb1ba8d7771d45f5a80a63cff05dae469872db2a9b1b8d9cee0b49554c720` | Saved adaptive-mode Phase 2 trace up to the move from offset `96` to `104`. |
| `lab/phase3_adaptive_result.txt` | `e1f794e448c2c2ad35b76613355d180e9ecb577034daa787680bc897f057dbda` | Saved adaptive-mode Phase 3 trace up to the move from offset `96` to `104`. |

## Report Media

The Word document contains four embedded images:

| File | SHA-256 |
| --- | --- |
| `report/extracted-media/image1.png` | `df3c639bf15d5210309b7a4e5ddd27ec7b01f15eb8de3c0ac475a33583129517` |
| `report/extracted-media/image2.png` | `249fa11406ff18356572dc5078cc330a9783919a4d94245080b3a8f87cdad43e` |
| `report/extracted-media/image3.png` | `6dff5ff56519f863c4e5564d1b29fa2fcfc9843505f7fb1f1dca93121c3dd8ec` |
| `report/extracted-media/image4.png` | `5942ab5d04eb97dea694f2ea7744b930e5543056700190f90165395013b66ac8` |

## Static Checks Run During Archive

Commands run from the repository root:

```sh
python3 -m py_compile \
  projects/project-ii-apt-agent/submissions/jingzhong-success/lab/EC/analyze_target.py \
  projects/project-ii-apt-agent/submissions/jingzhong-success/lab/EC/exploit \
  projects/project-ii-apt-agent/submissions/jingzhong-success/lab/EC/triage
```

Result: passed. Generated `__pycache__` output was removed after the check.

No Docker grading rerun was performed during this archive pass.
