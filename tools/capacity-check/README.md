# Capacity Check Tool

This tool answers small agenda-fit questions for course commitments. It is intentionally lightweight and is not a replacement for the main planning repository.

## Files

| Path | Purpose |
| --- | --- |
| [capacity/current.md](capacity/current.md) | Current sustainable focus-block budget, warning threshold, primary-goal cap, and protected domains |
| [goals/_template.md](goals/_template.md) | Template for active course goals that should be checked against capacity |
| [capacity_check.py](capacity_check.py) | Command-line checker |
| [test_capacity_check.py](test_capacity_check.py) | Unit tests |

One focus block currently means `90` minutes. Treat the number as a calibration baseline, not a reason to erase recovery time.

## How To Use

1. Update [capacity/current.md](capacity/current.md) when your real `7`-day or `14`-day course capacity changes.
2. Copy [goals/_template.md](goals/_template.md) into a new file under `goals/` when a course goal becomes active.
3. Fill the machine-readable metadata first. The checker depends on those fields.
4. Run `python3 tools/capacity-check/capacity_check.py status` before accepting more work.
5. Run `python3 tools/capacity-check/capacity_check.py can-add ...` when deciding whether a new commitment fits.

## Commands

Current status:

```bash
python3 tools/capacity-check/capacity_check.py status
```

Candidate commitment:

```bash
python3 tools/capacity-check/capacity_check.py can-add \
  --title "Security midterm review" \
  --domain course \
  --priority secondary \
  --deadline 2026-04-29 \
  --blocks-7d 2 \
  --blocks-14d 3 \
  --flexibility movable
```

Allowed verdicts are `fit`, `tight`, and `does not fit`.

## Response Contract

When answering a planning or agenda-fit question from this repo, respond in this order:

1. verdict: `fit`, `tight`, or `does not fit`
2. why: name the overloaded horizon, the primary-goal cap, or the protected-domain risk
3. recommendations: give `1` to `3` concrete next moves

If the next `7` or `14` days are overloaded, say so explicitly. If the plan is barely possible, call it `tight`. Do not solve overload by stealing first from `sleep`, `health`, `family`, or `recovery`.

## Example `does not fit` Response

```text
Verdict: does not fit
Why: the next 7 days would require 8.5 blocks against a capacity of 8.0; making it fit would pressure protected domains such as family, health
Recommendations:
- Defer `Journal fit revision` to its next checkpoint instead of stacking more work into this horizon.
- Replace an existing primary lane before accepting this new primary commitment.
- Set a later checkpoint or explicit defer date instead of forcing this into the next 7 to 14 days.
```

## Example `tight` Response

```text
Verdict: tight
Why: the task is technically possible, but it would leave little or no safe buffer for drift
Recommendations:
- Shrink `Security midterm readiness` from 4.0 to 2.5 blocks in the next 7 days.
- If you keep this, remove or downgrade one lower-value commitment rather than borrowing from protected life domains.
- Consider shrinking `New workshop abstract` to a smaller first milestone before you try to fit the full request.
```
