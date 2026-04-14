#!/usr/bin/env python3
"""Check whether the current agenda can absorb another commitment."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sys


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_SECTION = "machine-readable metadata"
GOAL_REQUIRED_FIELDS = {
    "goal_name",
    "domain",
    "priority",
    "start_date",
    "deadline",
    "status",
    "required_blocks_7d",
    "required_blocks_14d",
    "minimum_viable_blocks_7d",
    "flexibility",
    "why_now",
}
CAPACITY_REQUIRED_FIELDS = {
    "sustainable_blocks_7d",
    "sustainable_blocks_14d",
    "max_primary_goals",
    "warning_threshold",
    "protected_domains",
    "notes",
}
PRIORITY_VALUES = {"primary", "secondary", "maintenance", "parked"}
STATUS_VALUES = {"active", "waiting", "paused", "done"}
FLEXIBILITY_VALUES = {"fixed", "movable", "deferrable"}


class ValidationError(ValueError):
    """Raised when a Markdown metadata block is malformed."""


@dataclass(frozen=True)
class CapacityConfig:
    sustainable_blocks_7d: float
    sustainable_blocks_14d: float
    max_primary_goals: int
    warning_threshold: float
    protected_domains: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class GoalRecord:
    goal_name: str
    domain: str
    priority: str
    start_date: date
    deadline: date
    status: str
    required_blocks_7d: float
    required_blocks_14d: float
    minimum_viable_blocks_7d: float
    flexibility: str
    why_now: str
    path: Path


@dataclass(frozen=True)
class Assessment:
    verdict: str
    reason: str
    committed_blocks_7d: float
    committed_blocks_14d: float
    capacity_7d: float
    capacity_14d: float
    ratio_7d: float
    ratio_14d: float
    active_primary_goals: int
    max_primary_goals: int
    top_causes: tuple[str, ...]
    recommendations: tuple[str, ...]
    balance_warning: str | None
    protected_domains_at_risk: tuple[str, ...]


def format_blocks(value: float) -> str:
    return f"{value:.1f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the near-term agenda can absorb more work.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(DEFAULT_REPO_ROOT),
        help=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "status",
        help="Diagnose the current 7-day and 14-day agenda load.",
    )

    can_add = subparsers.add_parser(
        "can-add",
        help="Simulate whether a new commitment fits the current agenda.",
    )
    can_add.add_argument("--title", required=True, help="Short title of the proposed task.")
    can_add.add_argument("--domain", required=True, help="Task domain such as coursework or family.")
    can_add.add_argument(
        "--priority",
        required=True,
        choices=sorted(PRIORITY_VALUES),
        help="Priority lane for the proposed task.",
    )
    can_add.add_argument(
        "--deadline",
        required=True,
        help="Task deadline in YYYY-MM-DD format.",
    )
    can_add.add_argument(
        "--blocks-7d",
        required=True,
        type=float,
        help="Required 90-minute focus blocks in the next 7 days.",
    )
    can_add.add_argument(
        "--blocks-14d",
        required=True,
        type=float,
        help="Required 90-minute focus blocks in the next 14 days.",
    )
    can_add.add_argument(
        "--flexibility",
        required=True,
        choices=sorted(FLEXIBILITY_VALUES),
        help="Whether the task is fixed, movable, or deferrable.",
    )
    return parser.parse_args()


def normalize_heading(text: str) -> str:
    return text.lstrip("#").strip().lower()


def extract_metadata_lines(text: str, path: Path) -> list[str]:
    lines = text.splitlines()
    in_section = False
    collected: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = normalize_heading(stripped)
            if in_section:
                break
            if heading == METADATA_SECTION:
                in_section = True
            continue
        if in_section:
            collected.append(line)

    if not in_section:
        raise ValidationError(f"{path}: missing '## Machine-readable metadata' section")
    return collected


def parse_metadata_block(text: str, path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}

    for line in extract_metadata_lines(text, path):
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if ":" not in stripped:
            raise ValidationError(f"{path}: invalid metadata line '{line.strip()}'")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValidationError(f"{path}: empty metadata key")
        if key in metadata:
            raise ValidationError(f"{path}: duplicate metadata key '{key}'")
        metadata[key] = value
    return metadata


def parse_non_negative_float(value: str, field_name: str, path: Path) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValidationError(f"{path}: '{field_name}' must be numeric") from exc
    if parsed < 0:
        raise ValidationError(f"{path}: '{field_name}' must be non-negative")
    return parsed


def parse_positive_int(value: str, field_name: str, path: Path) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValidationError(f"{path}: '{field_name}' must be an integer") from exc
    if parsed <= 0:
        raise ValidationError(f"{path}: '{field_name}' must be greater than zero")
    return parsed


def parse_iso_date(value: str, field_name: str, path: Path) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{path}: '{field_name}' must use YYYY-MM-DD") from exc


def validate_goal_metadata(metadata: dict[str, str], path: Path) -> GoalRecord:
    missing = [field for field in sorted(GOAL_REQUIRED_FIELDS) if not metadata.get(field, "").strip()]
    if missing:
        raise ValidationError(f"{path}: missing required goal metadata: {', '.join(missing)}")

    priority = metadata["priority"].strip().lower()
    if priority not in PRIORITY_VALUES:
        raise ValidationError(f"{path}: invalid priority '{metadata['priority']}'")

    status = metadata["status"].strip().lower()
    if status not in STATUS_VALUES:
        raise ValidationError(f"{path}: invalid status '{metadata['status']}'")

    flexibility = metadata["flexibility"].strip().lower()
    if flexibility not in FLEXIBILITY_VALUES:
        raise ValidationError(f"{path}: invalid flexibility '{metadata['flexibility']}'")

    start_date = parse_iso_date(metadata["start_date"], "start_date", path)
    deadline = parse_iso_date(metadata["deadline"], "deadline", path)
    if deadline < start_date:
        raise ValidationError(f"{path}: 'deadline' cannot be earlier than 'start_date'")

    required_blocks_7d = parse_non_negative_float(metadata["required_blocks_7d"], "required_blocks_7d", path)
    required_blocks_14d = parse_non_negative_float(metadata["required_blocks_14d"], "required_blocks_14d", path)
    minimum_viable_blocks_7d = parse_non_negative_float(
        metadata["minimum_viable_blocks_7d"],
        "minimum_viable_blocks_7d",
        path,
    )
    if required_blocks_14d < required_blocks_7d:
        raise ValidationError(f"{path}: 'required_blocks_14d' cannot be smaller than 'required_blocks_7d'")
    if minimum_viable_blocks_7d > required_blocks_7d:
        raise ValidationError(
            f"{path}: 'minimum_viable_blocks_7d' cannot be larger than 'required_blocks_7d'",
        )

    return GoalRecord(
        goal_name=metadata["goal_name"].strip(),
        domain=metadata["domain"].strip().lower(),
        priority=priority,
        start_date=start_date,
        deadline=deadline,
        status=status,
        required_blocks_7d=required_blocks_7d,
        required_blocks_14d=required_blocks_14d,
        minimum_viable_blocks_7d=minimum_viable_blocks_7d,
        flexibility=flexibility,
        why_now=metadata["why_now"].strip(),
        path=path,
    )


def validate_capacity_metadata(metadata: dict[str, str], path: Path) -> CapacityConfig:
    missing = [field for field in sorted(CAPACITY_REQUIRED_FIELDS) if not metadata.get(field, "").strip()]
    if missing:
        raise ValidationError(f"{path}: missing required capacity metadata: {', '.join(missing)}")

    sustainable_blocks_7d = parse_non_negative_float(metadata["sustainable_blocks_7d"], "sustainable_blocks_7d", path)
    sustainable_blocks_14d = parse_non_negative_float(metadata["sustainable_blocks_14d"], "sustainable_blocks_14d", path)
    if sustainable_blocks_14d < sustainable_blocks_7d:
        raise ValidationError(
            f"{path}: 'sustainable_blocks_14d' cannot be smaller than 'sustainable_blocks_7d'",
        )

    max_primary_goals = parse_positive_int(metadata["max_primary_goals"], "max_primary_goals", path)
    warning_threshold = parse_non_negative_float(metadata["warning_threshold"], "warning_threshold", path)
    if warning_threshold <= 0 or warning_threshold > 1:
        raise ValidationError(f"{path}: 'warning_threshold' must be greater than 0 and at most 1")

    protected_domains = tuple(
        item.strip().lower()
        for item in metadata["protected_domains"].split(",")
        if item.strip()
    )
    if not protected_domains:
        raise ValidationError(f"{path}: 'protected_domains' must contain at least one value")

    return CapacityConfig(
        sustainable_blocks_7d=sustainable_blocks_7d,
        sustainable_blocks_14d=sustainable_blocks_14d,
        max_primary_goals=max_primary_goals,
        warning_threshold=warning_threshold,
        protected_domains=protected_domains,
        notes=metadata["notes"].strip(),
    )


def parse_goal_file(path: Path) -> GoalRecord:
    text = path.read_text(encoding="utf-8")
    metadata = parse_metadata_block(text, path)
    return validate_goal_metadata(metadata, path)


def parse_capacity_file(path: Path) -> CapacityConfig:
    text = path.read_text(encoding="utf-8")
    metadata = parse_metadata_block(text, path)
    return validate_capacity_metadata(metadata, path)


def load_capacity(repo_root: Path) -> CapacityConfig:
    capacity_path = repo_root / "data" / "capacity" / "current.md"
    if not capacity_path.exists():
        raise FileNotFoundError(f"Missing capacity file: {capacity_path}")
    return parse_capacity_file(capacity_path)


def load_active_goals(repo_root: Path) -> list[GoalRecord]:
    goals_dir = repo_root / "data" / "goals"
    if not goals_dir.exists():
        return []

    active_goals: list[GoalRecord] = []
    for path in sorted(goals_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        goal = parse_goal_file(path)
        if goal.status == "active":
            active_goals.append(goal)
    return active_goals


def build_candidate_goal(
    title: str,
    domain: str,
    priority: str,
    deadline_text: str,
    blocks_7d: float,
    blocks_14d: float,
    flexibility: str,
) -> GoalRecord:
    today = date.today()
    deadline = parse_iso_date(deadline_text, "deadline", Path("<cli>"))
    priority = priority.strip().lower()
    flexibility = flexibility.strip().lower()
    if priority not in PRIORITY_VALUES:
        raise ValidationError(f"<cli>: invalid priority '{priority}'")
    if flexibility not in FLEXIBILITY_VALUES:
        raise ValidationError(f"<cli>: invalid flexibility '{flexibility}'")
    if blocks_7d < 0 or blocks_14d < 0:
        raise ValidationError("<cli>: block counts must be non-negative")
    if blocks_14d < blocks_7d:
        raise ValidationError("<cli>: '--blocks-14d' cannot be smaller than '--blocks-7d'")
    return GoalRecord(
        goal_name=title.strip(),
        domain=domain.strip().lower(),
        priority=priority,
        start_date=today,
        deadline=deadline,
        status="active",
        required_blocks_7d=blocks_7d,
        required_blocks_14d=blocks_14d,
        minimum_viable_blocks_7d=blocks_7d,
        flexibility=flexibility,
        why_now=f"Candidate task under consideration for deadline {deadline.isoformat()}",
        path=Path("<candidate>"),
    )


def pick_top_causes(goals: list[GoalRecord], limit: int = 3) -> tuple[str, ...]:
    ranked = sorted(
        goals,
        key=lambda goal: (goal.required_blocks_7d, goal.required_blocks_14d, goal.priority == "primary"),
        reverse=True,
    )
    return tuple(
        f"{goal.goal_name} ({format_blocks(goal.required_blocks_7d)} blocks/7d, {goal.priority}, {goal.domain})"
        for goal in ranked[:limit]
    )


def pick_deferrable_goal(goals: list[GoalRecord], exclude_name: str | None = None) -> GoalRecord | None:
    candidates = [
        goal
        for goal in goals
        if goal.goal_name != exclude_name
        and goal.flexibility in {"movable", "deferrable"}
        and goal.priority != "primary"
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda goal: goal.required_blocks_7d)


def pick_shrinkable_goal(goals: list[GoalRecord], exclude_name: str | None = None) -> GoalRecord | None:
    candidates = [
        goal
        for goal in goals
        if goal.goal_name != exclude_name
        and goal.flexibility in {"movable", "deferrable"}
        and goal.required_blocks_7d > goal.minimum_viable_blocks_7d
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda goal: goal.required_blocks_7d - goal.minimum_viable_blocks_7d)


def collect_protected_domains_at_risk(
    active_goals: list[GoalRecord],
    protected_domains: tuple[str, ...],
    ratio_7d: float,
    ratio_14d: float,
    candidate: GoalRecord | None,
) -> tuple[str, ...]:
    protected_in_use = sorted(
        {
            goal.domain
            for goal in active_goals
            if goal.domain in protected_domains
        },
    )
    if not protected_in_use:
        return ()
    if candidate is not None and candidate.domain in protected_domains:
        return ()
    if ratio_7d >= 0.9 or ratio_14d >= 0.9:
        return tuple(protected_in_use)
    return ()


def build_recommendations(
    verdict: str,
    goals: list[GoalRecord],
    capacity: CapacityConfig,
    primary_count: int,
    candidate: GoalRecord | None,
) -> tuple[str, ...]:
    recommendations: list[str] = []
    exclude_name = candidate.goal_name if candidate else None

    shrinkable = pick_shrinkable_goal(goals, exclude_name=exclude_name)
    if shrinkable is not None and verdict in {"tight", "overloaded", "reject"}:
        recommendations.append(
            f"Shrink `{shrinkable.goal_name}` from {format_blocks(shrinkable.required_blocks_7d)} to "
            f"{format_blocks(shrinkable.minimum_viable_blocks_7d)} blocks in the next 7 days.",
        )

    deferrable = pick_deferrable_goal(goals, exclude_name=exclude_name)
    if deferrable is not None and verdict in {"tight", "overloaded", "reject"}:
        recommendations.append(
            f"Defer `{deferrable.goal_name}` to its next checkpoint instead of stacking more work into this horizon.",
        )

    if candidate is not None and candidate.priority == "primary" and primary_count > capacity.max_primary_goals:
        recommendations.append(
            "Replace an existing primary lane before accepting this new primary commitment.",
        )

    if verdict == "fit":
        recommendations.append(
            "Keep the current buffer intact and only add more work if it replaces something lower-value.",
        )
    elif verdict == "tight":
        recommendations.append(
            "If you keep this, remove or downgrade one lower-value commitment rather than borrowing from protected life domains.",
        )
    else:
        recommendations.append(
            "Set a later checkpoint or explicit defer date instead of forcing this into the next 7 to 14 days.",
        )

    if candidate is not None and verdict in {"tight", "reject"}:
        recommendations.append(
            f"Consider shrinking `{candidate.goal_name}` to a smaller first milestone before you try to fit the full request.",
        )

    unique: list[str] = []
    for item in recommendations:
        if item not in unique:
            unique.append(item)
    return tuple(unique[:3])


def assess_goals(
    capacity: CapacityConfig,
    active_goals: list[GoalRecord],
    candidate: GoalRecord | None = None,
) -> Assessment:
    goals = list(active_goals)
    if candidate is not None:
        goals.append(candidate)

    committed_7d = sum(goal.required_blocks_7d for goal in goals)
    committed_14d = sum(goal.required_blocks_14d for goal in goals)
    ratio_7d = committed_7d / capacity.sustainable_blocks_7d if capacity.sustainable_blocks_7d else 0.0
    ratio_14d = committed_14d / capacity.sustainable_blocks_14d if capacity.sustainable_blocks_14d else 0.0
    primary_count = sum(1 for goal in goals if goal.priority == "primary")

    reasons: list[str] = []
    if ratio_7d > 1:
        reasons.append(
            f"the next 7 days would require {format_blocks(committed_7d)} blocks against a capacity of {format_blocks(capacity.sustainable_blocks_7d)}",
        )
    if ratio_14d > 1:
        reasons.append(
            f"the next 14 days would require {format_blocks(committed_14d)} blocks against a capacity of {format_blocks(capacity.sustainable_blocks_14d)}",
        )
    if primary_count > capacity.max_primary_goals:
        reasons.append(
            f"the plan would create {primary_count} primary goals even though the cap is {capacity.max_primary_goals}",
        )

    if candidate is None:
        if reasons:
            verdict = "overloaded"
        elif ratio_7d >= capacity.warning_threshold or ratio_14d >= capacity.warning_threshold:
            verdict = "tight"
            reasons.append(
                "the agenda is inside hard capacity but the remaining buffer is too small for normal drift",
            )
        else:
            verdict = "fit"
            reasons.append("the active goals still fit inside the near-term block budget")
    else:
        if reasons:
            verdict = "reject"
        elif ratio_7d >= capacity.warning_threshold or ratio_14d >= capacity.warning_threshold:
            verdict = "tight"
            reasons.append(
                "the task is technically possible, but it would leave little or no safe buffer for drift",
            )
        else:
            verdict = "fit"
            reasons.append("the proposed task still leaves reasonable near-term buffer")

    protected_domains_at_risk = collect_protected_domains_at_risk(
        active_goals=goals,
        protected_domains=capacity.protected_domains,
        ratio_7d=ratio_7d,
        ratio_14d=ratio_14d,
        candidate=candidate,
    )
    balance_warning = None
    if protected_domains_at_risk:
        protected_list = ", ".join(protected_domains_at_risk)
        balance_warning = (
            f"Protected domains at risk: {protected_list}. Do not fund this plan by cutting those blocks first."
        )
        if verdict == "reject" and candidate is not None:
            reasons.append(
                f"making it fit would pressure protected domains such as {protected_list}",
            )

    recommendations = build_recommendations(
        verdict=verdict,
        goals=goals,
        capacity=capacity,
        primary_count=primary_count,
        candidate=candidate,
    )
    return Assessment(
        verdict=verdict,
        reason="; ".join(reasons),
        committed_blocks_7d=committed_7d,
        committed_blocks_14d=committed_14d,
        capacity_7d=capacity.sustainable_blocks_7d,
        capacity_14d=capacity.sustainable_blocks_14d,
        ratio_7d=ratio_7d,
        ratio_14d=ratio_14d,
        active_primary_goals=primary_count,
        max_primary_goals=capacity.max_primary_goals,
        top_causes=pick_top_causes(goals),
        recommendations=recommendations,
        balance_warning=balance_warning,
        protected_domains_at_risk=protected_domains_at_risk,
    )


def render_assessment(assessment: Assessment, capacity: CapacityConfig, candidate: GoalRecord | None = None) -> str:
    lines = [
        f"Verdict: {assessment.verdict}",
        f"Why: {assessment.reason}",
        "",
        "Load summary:",
        (
            f"- 7d committed: {format_blocks(assessment.committed_blocks_7d)} / "
            f"{format_blocks(assessment.capacity_7d)} blocks ({assessment.ratio_7d:.0%})"
        ),
        (
            f"- 14d committed: {format_blocks(assessment.committed_blocks_14d)} / "
            f"{format_blocks(assessment.capacity_14d)} blocks ({assessment.ratio_14d:.0%})"
        ),
        (
            f"- Active primary goals: {assessment.active_primary_goals} / "
            f"{assessment.max_primary_goals}"
        ),
    ]

    if candidate is not None:
        lines.extend(
            [
                "",
                "Candidate task:",
                f"- Title: {candidate.goal_name}",
                f"- Domain: {candidate.domain}",
                f"- Priority: {candidate.priority}",
                f"- Deadline: {candidate.deadline.isoformat()}",
            ],
        )

    lines.extend(["", "Top load contributors:"])
    if assessment.top_causes:
        for cause in assessment.top_causes:
            lines.append(f"- {cause}")
    else:
        lines.append("- No active goals are currently consuming block budget.")

    lines.extend(["", "Recommendations:"])
    for item in assessment.recommendations:
        lines.append(f"- {item}")

    if assessment.balance_warning:
        lines.extend(["", f"Balance reminder: {assessment.balance_warning}"])

    lines.extend(["", f"Capacity note: {capacity.notes}"])
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()

    try:
        capacity = load_capacity(repo_root)
        active_goals = load_active_goals(repo_root)

        if args.command == "status":
            assessment = assess_goals(capacity, active_goals)
            print(render_assessment(assessment, capacity))
            return 0

        candidate = build_candidate_goal(
            title=args.title,
            domain=args.domain,
            priority=args.priority,
            deadline_text=args.deadline,
            blocks_7d=args.blocks_7d,
            blocks_14d=args.blocks_14d,
            flexibility=args.flexibility,
        )
        assessment = assess_goals(capacity, active_goals, candidate=candidate)
        print(render_assessment(assessment, capacity, candidate=candidate))
        return 0
    except (FileNotFoundError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
