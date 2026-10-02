"""Repository tests for the zRepro reverse-engineering catalog."""

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scripts.validate_re_catalog as validator

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

    def test_sample_reports_reject_schema_invalid_nested_values(self):
        sample_path = validator.REPORTS_DIR / "pe.report.json"
        valid = json.loads(sample_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(dir=validator.ROOT) as temporary:
            report_dir = Path(temporary)
            for name in validator.REQUIRED_REPORTS:
                (report_dir / name).write_text(json.dumps(valid), encoding="utf-8")

            invalid = copy.deepcopy(valid)
            invalid["artifact"] = None
            (report_dir / "pe.report.json").write_text(json.dumps(invalid), encoding="utf-8")

            with patch.object(validator, "REPORTS_DIR", report_dir):
                errors = validate_reports()

        self.assertTrue(any("artifact" in error and "object" in error for error in errors), errors)

    def test_schema_rejects_unimplemented_keywords(self):
        schema_path = validator.SCHEMA_PATH
        with tempfile.TemporaryDirectory(dir=validator.ROOT) as temporary:
            temporary_schema = Path(temporary) / "schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["anyOf"] = []
            temporary_schema.write_text(json.dumps(schema), encoding="utf-8")
            with patch.object(validator, "SCHEMA_PATH", temporary_schema):
                errors = validator.validate_schema()
        self.assertTrue(any("unsupported schema keywords" in error for error in errors), errors)

    def test_fixture_evidence_references_cannot_escape_the_fixture_corpus(self):
        self.assertIsNone(validator._validate_fixture_source("fixtures/re/pe.sample.json"))
        self.assertEqual(
            validator._validate_fixture_source("fixtures/re/../../README.md"),
            "fixture evidence source escapes fixtures/re",
        )
        self.assertEqual(
            validator._validate_fixture_source("fixtures/re/pe\\..\\README.md"),
            "fixture evidence source uses an unsupported path separator",
        )

    def test_machine_readable_catalog(self):
        self.assertEqual(validate_catalog_index(self.skills), [])

    def test_catalog_rejects_invalid_shapes_and_domains(self):
        valid = json.loads(validator.CATALOG_PATH.read_text())
        malformed = [None, [], {"skills": None}, {"skills": [None]}, {"skills": [{"name": []}]}]
        for domain in (None, "", "   ", 4):
            altered = copy.deepcopy(valid)
            altered["skills"][0]["domain"] = domain
            malformed.append(altered)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "catalog.json"
            for index, data in enumerate(malformed):
                with self.subTest(case=index):
                    path.write_text(json.dumps(data))
                    with patch.object(validator, "CATALOG_PATH", path):
                        self.assertTrue(validate_catalog_index(self.skills))

    def test_reference_benchmarks(self):
        self.assertEqual(validate_benchmarks(self.skills), [])

    def test_supply_chain_evidence(self):
        self.assertEqual(validate_supply_chain_evidence(), [])


if __name__ == "__main__":
    unittest.main()
