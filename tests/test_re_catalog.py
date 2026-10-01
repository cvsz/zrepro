"""Repository tests for the zRepro reverse-engineering catalog."""

import unittest

from scripts.validate_re_catalog import (
    validate_component_registration,
    validate_fixtures,
    validate_schema,
    validate_skills,
)


class ReverseEngineeringCatalogTest(unittest.TestCase):
    def test_skill_metadata(self):
        self.assertEqual(validate_skills(), [])

    def test_component_registration(self):
        self.assertEqual(validate_component_registration(), [])

    def test_evidence_schema(self):
        self.assertEqual(validate_schema(), [])

    def test_safe_synthetic_fixtures(self):
        self.assertEqual(validate_fixtures(), [])


if __name__ == "__main__":
    unittest.main()
