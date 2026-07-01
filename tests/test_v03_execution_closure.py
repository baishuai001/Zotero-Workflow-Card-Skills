from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class FinalizeWorkflowCardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="zwc_v03_"))
        self.project = self.tmp / "workflow_cards"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=SKILL_ROOT,
            text=True,
            capture_output=True,
        )

    def read_csv_rows(self, path: Path) -> list[dict[str, str]]:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_finalize_writes_card_matrix_and_screening_backfill(self) -> None:
        init = self.run_script("scripts/init_project.py", "--project-root", str(self.project))
        self.assertEqual(init.returncode, 0, init.stderr)

        seed_screening = self.project / "seed_screening.json"
        seed_screening.write_text(
            json.dumps(
                {
                    "paper_id": "PAPER-001",
                    "title": "Example workflow paper",
                    "doi": "10.0000/example",
                    "zotero_item_key": "ABC123",
                    "screening_status": "ready-for-workflow-card",
                    "workflow_card_status": "not-started",
                    "action_next": "make-workflow-card",
                    "priority": "high",
                    "design_sample_role": "canonical-example",
                }
            ),
            encoding="utf-8",
        )
        seed = self.run_script(
            "scripts/update_screening_decisions.py",
            "--project-root",
            str(self.project),
            "--row-json",
            str(seed_screening),
        )
        self.assertEqual(seed.returncode, 0, seed.stderr)

        card_source = self.project / "card.md"
        card_source.write_text("# Workflow Card: Example workflow paper\n", encoding="utf-8")
        matrix_row = self.project / "matrix_row.json"
        matrix_row.write_text(
            json.dumps(
                {
                    "paper_id": "PAPER-001",
                    "title": "Example workflow paper",
                    "doi": "10.0000/example",
                    "zotero_item_key": "ABC123",
                    "priority": "high",
                    "design_sample_role": "canonical-example",
                    "main_workflow_type": "de novo atlas",
                }
            ),
            encoding="utf-8",
        )

        finalize = self.run_script(
            "scripts/finalize_workflow_card.py",
            "--project-root",
            str(self.project),
            "--slug",
            "example-paper",
            "--content-file",
            str(card_source),
            "--row-json",
            str(matrix_row),
        )
        self.assertEqual(finalize.returncode, 0, finalize.stderr + finalize.stdout)

        card_path = self.project / "cards" / "example-paper.md"
        self.assertTrue(card_path.exists())
        self.assertEqual(card_path.read_text(encoding="utf-8"), "# Workflow Card: Example workflow paper\n")

        matrix_rows = self.read_csv_rows(self.project / "workflow_matrix.csv")
        self.assertEqual(len(matrix_rows), 1)
        self.assertEqual(matrix_rows[0]["paper_id"], "PAPER-001")
        self.assertEqual(matrix_rows[0]["screening_status"], "full-card")
        self.assertEqual(matrix_rows[0]["card_path"], "cards/example-paper.md")

        screening_rows = self.read_csv_rows(self.project / "screening_decisions.csv")
        self.assertEqual(len(screening_rows), 1)
        self.assertEqual(screening_rows[0]["screening_status"], "full-card")
        self.assertEqual(screening_rows[0]["workflow_card_status"], "matrix-updated")
        self.assertEqual(screening_rows[0]["action_next"], "hold")
        self.assertEqual(screening_rows[0]["card_path"], "cards/example-paper.md")

        validate = self.run_script("scripts/validate_project.py", "--project-root", str(self.project))
        self.assertEqual(validate.returncode, 0, validate.stderr + validate.stdout)

    def test_stopping_criteria_are_practical_and_saturation_based(self) -> None:
        protocol = (SKILL_ROOT / "references" / "literature_screening_protocol.md").read_text(encoding="utf-8")
        search_template = (SKILL_ROOT / "references" / "search_protocol_template.md").read_text(encoding="utf-8")
        batch_template = (SKILL_ROOT / "references" / "batch_synthesis_template.md").read_text(encoding="utf-8")

        for text in (protocol, search_template, batch_template):
            self.assertIn("practical threshold", text)
            self.assertIn("design saturation", text)
            self.assertIn("stop / continue", text)


if __name__ == "__main__":
    unittest.main()
