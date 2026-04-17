from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import capacity_check  # noqa: E402


def build_capacity_file(
    sustainable_blocks_7d: float = 8,
    sustainable_blocks_14d: float = 16,
    max_primary_goals: int = 2,
    warning_threshold: float = 0.9,
    protected_domains: str = "sleep, health, family, recovery",
    notes: str = "One focus block equals 90 minutes.",
) -> str:
    return textwrap.dedent(
        f"""\
        # Current Capacity

        ## Machine-readable metadata
        - sustainable_blocks_7d: {sustainable_blocks_7d}
        - sustainable_blocks_14d: {sustainable_blocks_14d}
        - max_primary_goals: {max_primary_goals}
        - warning_threshold: {warning_threshold}
        - protected_domains: {protected_domains}
        - notes: {notes}
        """,
    )


def build_goal_file(
    *,
    goal_name: str = "Sample goal",
    domain: str = "coursework",
    priority: str = "secondary",
    start_date: str = "2026-04-14",
    deadline: str = "2026-04-20",
    status: str = "active",
    required_blocks_7d: object = 2,
    required_blocks_14d: object = 4,
    minimum_viable_blocks_7d: object = 1,
    flexibility: str = "movable",
    why_now: str = "Because it matters now.",
) -> str:
    return textwrap.dedent(
        f"""\
        # Goal

        ## Machine-readable metadata
        - goal_name: {goal_name}
        - domain: {domain}
        - priority: {priority}
        - start_date: {start_date}
        - deadline: {deadline}
        - status: {status}
        - required_blocks_7d: {required_blocks_7d}
        - required_blocks_14d: {required_blocks_14d}
        - minimum_viable_blocks_7d: {minimum_viable_blocks_7d}
        - flexibility: {flexibility}
        - why_now: {why_now}

        ## Identity
        - Goal name: {goal_name}
        """,
    )


class CapacityCheckTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        (root / "capacity").mkdir(parents=True, exist_ok=True)
        (root / "goals").mkdir(parents=True, exist_ok=True)
        return temp_dir, root

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")

    def test_missing_goal_field_raises(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            goal_path = root / "goals" / "broken.md"
            self.write(goal_path, build_goal_file(why_now=""))
            with self.assertRaises(capacity_check.ValidationError):
                capacity_check.parse_goal_file(goal_path)

    def test_invalid_enum_raises(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            goal_path = root / "goals" / "broken.md"
            self.write(goal_path, build_goal_file(priority="urgent"))
            with self.assertRaises(capacity_check.ValidationError):
                capacity_check.parse_goal_file(goal_path)

    def test_invalid_numeric_and_date_raise(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            goal_path = root / "goals" / "broken.md"
            self.write(goal_path, build_goal_file(start_date="2026/04/14", required_blocks_7d="abc"))
            with self.assertRaises(capacity_check.ValidationError):
                capacity_check.parse_goal_file(goal_path)

    def test_status_returns_fit_below_threshold(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "exam.md",
                build_goal_file(goal_name="Exam prep", priority="primary", required_blocks_7d=4, required_blocks_14d=8),
            )
            self.write(
                root / "goals" / "notes.md",
                build_goal_file(goal_name="Note cleanup", required_blocks_7d=2, required_blocks_14d=4),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            assessment = capacity_check.assess_goals(capacity, goals)
            self.assertEqual(assessment.verdict, "fit")

    def test_status_returns_tight_at_threshold(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "journal.md",
                build_goal_file(goal_name="Journal", priority="primary", required_blocks_7d=7.2, required_blocks_14d=14.4),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            assessment = capacity_check.assess_goals(capacity, goals)
            self.assertEqual(assessment.verdict, "tight")

    def test_can_add_returns_does_not_fit_when_capacity_is_exceeded(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "midterm.md",
                build_goal_file(goal_name="Midterm", priority="primary", required_blocks_7d=7.5, required_blocks_14d=12),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            candidate = capacity_check.build_candidate_goal(
                title="New task",
                domain="build",
                priority="secondary",
                deadline_text="2026-04-20",
                blocks_7d=1.0,
                blocks_14d=2.0,
                flexibility="movable",
            )
            assessment = capacity_check.assess_goals(capacity, goals, candidate=candidate)
            self.assertEqual(assessment.verdict, "does not fit")

    def test_can_add_returns_does_not_fit_when_primary_cap_is_exceeded(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "goal-1.md",
                build_goal_file(goal_name="Goal 1", priority="primary", required_blocks_7d=2, required_blocks_14d=4),
            )
            self.write(
                root / "goals" / "goal-2.md",
                build_goal_file(goal_name="Goal 2", priority="primary", required_blocks_7d=2, required_blocks_14d=4),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            candidate = capacity_check.build_candidate_goal(
                title="Third primary",
                domain="dream",
                priority="primary",
                deadline_text="2026-04-21",
                blocks_7d=1.0,
                blocks_14d=1.0,
                flexibility="deferrable",
            )
            assessment = capacity_check.assess_goals(capacity, goals, candidate=candidate)
            self.assertEqual(assessment.verdict, "does not fit")

    def test_recommendations_do_not_tell_user_to_work_harder(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "mvp.md",
                build_goal_file(goal_name="MVP", priority="primary", required_blocks_7d=7.5, required_blocks_14d=14),
            )
            self.write(
                root / "goals" / "admin.md",
                build_goal_file(
                    goal_name="Admin cleanup",
                    priority="secondary",
                    required_blocks_7d=1.0,
                    required_blocks_14d=2.0,
                    minimum_viable_blocks_7d=0.5,
                    flexibility="deferrable",
                ),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            assessment = capacity_check.assess_goals(capacity, goals)
            joined = " ".join(assessment.recommendations).lower()
            self.assertEqual(assessment.verdict, "does not fit")
            self.assertNotIn("work harder", joined)

    def test_balance_warning_when_dream_project_crowds_out_protected_domains(self) -> None:
        temp_dir, root = self.make_repo()
        with temp_dir:
            self.write(root / "capacity" / "current.md", build_capacity_file())
            self.write(
                root / "goals" / "family.md",
                build_goal_file(
                    goal_name="Family dinner",
                    domain="family",
                    priority="maintenance",
                    required_blocks_7d=2,
                    required_blocks_14d=2,
                    minimum_viable_blocks_7d=2,
                    flexibility="fixed",
                ),
            )
            self.write(
                root / "goals" / "health.md",
                build_goal_file(
                    goal_name="Exercise",
                    domain="health",
                    priority="maintenance",
                    required_blocks_7d=1.5,
                    required_blocks_14d=3,
                    minimum_viable_blocks_7d=1.5,
                    flexibility="fixed",
                ),
            )
            self.write(
                root / "goals" / "study.md",
                build_goal_file(goal_name="Midterm", domain="coursework", priority="primary", required_blocks_7d=3.5, required_blocks_14d=7),
            )

            capacity = capacity_check.load_capacity(root)
            goals = capacity_check.load_active_goals(root)
            candidate = capacity_check.build_candidate_goal(
                title="Dream project",
                domain="dream",
                priority="secondary",
                deadline_text="2026-04-22",
                blocks_7d=1.0,
                blocks_14d=1.0,
                flexibility="deferrable",
            )
            assessment = capacity_check.assess_goals(capacity, goals, candidate=candidate)
            self.assertEqual(assessment.verdict, "tight")
            self.assertIsNotNone(assessment.balance_warning)
            self.assertIn("family", assessment.balance_warning)


if __name__ == "__main__":
    unittest.main()
