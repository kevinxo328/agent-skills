import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "writing-job-application"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_FILE.read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+)$", cls.content, re.MULTILINE)
        cls.description = match.group(1).lower()

    def test_description_matches_supported_application_materials(self):
        self.assertIn("cover letter", self.description)
        self.assertIn("self-introduction", self.description)
        self.assertIn("recruiter", self.description)
        self.assertNotIn("recommendation", self.description)
        self.assertNotIn("hr questions", self.description)

    def test_resume_persistence_requires_consent(self):
        self.assertRegex(
            self.content.lower(),
            r"(ask|obtain|get).{0,40}(consent|permission)",
        )

    def test_format_branches_are_disclosed_from_skill(self):
        reference = SKILL_DIR / "references" / "formats.md"

        self.assertTrue(reference.exists())
        self.assertIn("references/formats.md", self.content)

    def test_skill_has_no_truncated_duplicate_line(self):
        self.assertNotIn("ion must also be plain text", self.content)

    def test_version_is_1_3_1(self):
        self.assertRegex(self.content, r'metadata:\s+version: "1\.3\.1"')

    def test_scan_failure_is_not_treated_as_an_empty_result(self):
        self.assertIn(
            "Only treat `RESUME_COUNT=0` as an empty result after a successful scan.",
            self.content,
        )


if __name__ == "__main__":
    unittest.main()
