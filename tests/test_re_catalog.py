"""Repository tests for the zRepro reverse-engineering catalog."""

import unittest

from scripts.validate_re_catalog import (
    skill_metadata,
    validate_benchmarks,
    validate_catalog_index,
    validate_component_registration,
    validate_fixtures,
    validate_reports,
    validate_schema,
    validate_supply_chain_evidence,
)


class ReverseEngineeringCatalogTest(unittest.TestCase):
    def setUp(self):
        self.skills, self.skill_errors = skill_metadata()

    def test_skill_metadata(self):
        self.assertEqual(self.skill_errors, [])

    def test_component_registration(self):
        self.assertEqual(validate_component_registration(self.skills), [])

    def test_evidence_schema(self):
        self.assertEqual(validate_schema(), [])

    def test_safe_synthetic_fixtures(self):
        self.assertEqual(validate_fixtures(), [])

    def test_sample_reports(self):
        self.assertEqual(validate_reports(), [])

    def test_machine_readable_catalog(self):
        self.assertEqual(validate_catalog_index(self.skills), [])

    def test_reference_benchmarks(self):
        self.assertEqual(validate_benchmarks(self.skills), [])

    def test_supply_chain_evidence(self):
        self.assertEqual(validate_supply_chain_evidence(), [])


if __name__ == "__main__":
    unittest.main()
