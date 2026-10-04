# version: 0.1.0
# version-date: 2026-10-04
# checksum: sha256:0000000000000000000000000000000000000000000000000000000000000000

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from myevo.artifact_verify import is_version_greater


class VersionComparisonTests(unittest.TestCase):
    def test_patch_increase(self) -> None:
        self.assertTrue(is_version_greater("0.1.1", "0.1.0"))

    def test_minor_increase(self) -> None:
        self.assertTrue(is_version_greater("0.2.0", "0.1.9"))

    def test_equal_version_is_not_an_increase(self) -> None:
        self.assertFalse(is_version_greater("0.1.0", "0.1.0"))

    def test_decrease_is_rejected(self) -> None:
        self.assertFalse(is_version_greater("0.0.9", "0.1.0"))


if __name__ == "__main__":
    unittest.main()
