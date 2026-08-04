import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"


def load_check_format_module():
    module_path = SCRIPTS_DIR / "check-format.py"
    spec = importlib.util.spec_from_file_location("check_format", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckFormatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_check_format_module()

    def test_cjk_characters_are_not_double_counted(self):
        errors, count = self.module.check_format("中文")

        self.assertEqual(errors, [])
        self.assertEqual(count, 2)

    def test_technical_term_with_hash_is_not_treated_as_heading(self):
        errors, _ = self.module.check_format("Built C# services for internal tools.")

        self.assertFalse(any("Headers" in error for error in errors))

    def test_en_dash_is_allowed_for_date_ranges(self):
        errors, _ = self.module.check_format("2020–2022")

        self.assertFalse(any("En-dash" in error for error in errors))


class ScriptCliTests(unittest.TestCase):
    def test_missing_pdf_returns_failure_status(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "read-pdf.py"),
                "/tmp/nonexistent-job-application-resume.pdf",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("File not found", result.stderr)

    def test_resume_scanner_uses_explicit_directories_and_reports_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            local_dir = root / "local resumes"
            global_dir = root / "global resumes"
            local_dir.mkdir()
            global_dir.mkdir()
            older = local_dir / "older resume.md"
            newer = global_dir / "newer resume.pdf"
            older.write_text("older", encoding="utf-8")
            newer.write_text("newer", encoding="utf-8")
            os.utime(older, (1_700_000_000, 1_700_000_000))
            os.utime(newer, (1_800_000_000, 1_800_000_000))

            result = subprocess.run(
                [
                    "bash",
                    str(SCRIPTS_DIR / "scan-resumes.sh"),
                    str(local_dir),
                    str(global_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESUME_COUNT=2", result.stdout)
        self.assertIn(str(older), result.stdout)
        self.assertIn(str(newer), result.stdout)
        self.assertLess(
            result.stdout.index(str(newer)), result.stdout.index(str(older))
        )


if __name__ == "__main__":
    unittest.main()
