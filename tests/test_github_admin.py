"""Repository administration helper tests. No GitHub API calls are made."""

import io
import sys
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

import scripts.github_admin as admin


class GitHubAdminTest(unittest.TestCase):
    def test_new_protection_binds_required_checks_to_github_actions(self):
        payload = admin.protection_payload(None, actions_app_id=15368)
        status_checks = payload["required_status_checks"]

        self.assertTrue(status_checks["strict"])
        self.assertNotIn("contexts", status_checks)
        self.assertEqual(
            status_checks["checks"],
            [{"context": name, "app_id": 15368} for name in admin.REQUIRED_CHECKS],
        )
        self.assertNotIn("required_signatures", payload)

    def test_existing_protection_is_merged_without_losing_custom_controls(self):
        existing = {
            "url": "https://api.github.com/repos/example/project/branches/main/protection",
            "required_status_checks": {
                "url": "https://api.github.com/status-checks",
                "contexts_url": "https://api.github.com/status-checks/contexts",
                "strict": False,
                "contexts": ["custom-gate", "repository-baseline"],
                "checks": [
                    {"context": "custom-gate", "app_id": 42},
                    {"context": "repository-baseline", "app_id": None},
                ],
            },
            "enforce_admins": {"url": "https://api.github.com/enforce-admins", "enabled": False},
            "required_pull_request_reviews": {
                "url": "https://api.github.com/reviews",
                "required_approving_review_count": 2,
                "dismiss_stale_reviews": False,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
                "dismissal_restrictions": {
                    "users": [{"login": "reviewer"}],
                    "teams": [{"slug": "security"}],
                    "apps": [{"slug": "review-bot"}],
                },
                "bypass_pull_request_allowances": {
                    "users": [{"login": "release-manager"}],
                    "teams": [{"slug": "release"}],
                    "apps": [{"slug": "release-bot"}],
                },
            },
            "restrictions": {
                "url": "https://api.github.com/restrictions",
                "users_url": "https://api.github.com/restrictions/users",
                "teams_url": "https://api.github.com/restrictions/teams",
                "apps_url": "https://api.github.com/restrictions/apps",
                "users": [{"login": "deployer"}],
                "teams": [{"slug": "operations"}],
                "apps": [{"slug": "deploy-app"}],
            },
            "required_signatures": {"url": "https://api.github.com/signatures", "enabled": True},
            "required_linear_history": {"enabled": True},
            "allow_force_pushes": {"enabled": True},
            "allow_deletions": {"enabled": True},
            "block_creations": {"enabled": True},
            "required_conversation_resolution": {"enabled": False},
            "lock_branch": {"enabled": True},
            "allow_fork_syncing": {"enabled": False},
        }

        payload = admin.protection_payload(existing, actions_app_id=15368)
        status_checks = payload["required_status_checks"]
        checks = {item["context"]: item["app_id"] for item in status_checks["checks"]}

        self.assertTrue(status_checks["strict"])
        self.assertNotIn("contexts", status_checks)
        self.assertEqual(checks["custom-gate"], 42)
        self.assertEqual(checks["repository-baseline"], 15368)
        for required in admin.REQUIRED_CHECKS:
            self.assertEqual(checks[required], 15368)
        self.assertEqual(payload["restrictions"], {
            "users": ["deployer"], "teams": ["operations"], "apps": ["deploy-app"]
        })
        reviews = payload["required_pull_request_reviews"]
        self.assertEqual(reviews["required_approving_review_count"], 2)
        self.assertTrue(reviews["dismiss_stale_reviews"])
        self.assertTrue(reviews["require_code_owner_reviews"])
        self.assertTrue(reviews["require_last_push_approval"])
        self.assertEqual(reviews["dismissal_restrictions"], {
            "users": ["reviewer"], "teams": ["security"], "apps": ["review-bot"]
        })
        self.assertEqual(reviews["bypass_pull_request_allowances"], {
            "users": ["release-manager"], "teams": ["release"], "apps": ["release-bot"]
        })
        self.assertTrue(payload["required_linear_history"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])
        self.assertTrue(payload["block_creations"])
        self.assertTrue(payload["required_conversation_resolution"])
        self.assertTrue(payload["lock_branch"])
        self.assertFalse(payload["allow_fork_syncing"])
        self.assertNotIn("required_signatures", payload)

    def test_apply_reads_before_writing_and_sends_merged_rules(self):
        current = {
            "required_status_checks": {
                "contexts": ["custom-gate"],
                "checks": [{"context": "custom-gate", "app_id": 42}],
            },
            "restrictions": {
                "users": ["release-manager"],
                "teams": [],
                "apps": [],
            },
        }
        calls = []

        def fake_api(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if endpoint == "apps/github-actions":
                return {"id": 15368}
            if endpoint == "repos/example/project/branches/main/protection":
                return current if method == "GET" else None
            if endpoint == "repos/example/project":
                return {"security_and_analysis": {}}
            return None

        with patch.object(admin, "gh_api", side_effect=fake_api):
            admin.apply("example/project", "main")

        branch_read = calls.index(("GET", "repos/example/project/branches/main/protection", None))
        branch_write = next(
            index for index, call in enumerate(calls)
            if call[0] == "PUT" and call[1] == "repos/example/project/branches/main/protection"
        )
        self.assertLess(branch_read, branch_write)
        payload = calls[branch_write][2]
        checks = {item["context"]: item["app_id"] for item in payload["required_status_checks"]["checks"]}
        self.assertEqual(checks["custom-gate"], 42)
        self.assertEqual(payload["restrictions"]["users"], ["release-manager"])

    def test_apply_aborts_on_unknown_rules_without_mutating(self):
        calls = []

        def fake_api(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if endpoint == "apps/github-actions":
                return {"id": 15368}
            if endpoint == "repos/example/project/branches/main/protection":
                return {"future_security_rule": {"enabled": True}}
            return {"security_and_analysis": {}}

        with patch.object(admin, "gh_api", side_effect=fake_api):
            with self.assertRaisesRegex(ValueError, "unrecognized branch protection fields"):
                admin.apply("example/project", "main")
        self.assertFalse(any(method in {"PUT", "PATCH", "DELETE"} for method, _, _ in calls))

    def test_apply_treats_only_branch_protection_404_as_unprotected(self):
        calls = []

        def fake_api(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if endpoint == "apps/github-actions":
                return {"id": 15368}
            if endpoint == "repos/example/project/branches/main/protection":
                if method == "GET":
                    raise admin.GitHubAPIError("not found (HTTP 404)", status_code=404)
                return None
            if endpoint == "repos/example/project":
                return {"security_and_analysis": {}}
            return None

        with patch.object(admin, "gh_api", side_effect=fake_api):
            admin.apply("example/project", "main")

        self.assertTrue(any(
            method == "PUT" and endpoint == "repos/example/project/branches/main/protection"
            for method, endpoint, _ in calls
        ))

    def test_apply_rejects_invalid_success_response_before_mutating(self):
        calls = []

        def fake_api(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if endpoint == "apps/github-actions":
                return {"id": 15368}
            if endpoint == "repos/example/project/branches/main/protection":
                return None
            return {"security_and_analysis": {}}

        with patch.object(admin, "gh_api", side_effect=fake_api):
            with self.assertRaisesRegex(ValueError, "branch protection returned an invalid response"):
                admin.apply("example/project", "main")
        self.assertFalse(any(method in {"PUT", "PATCH", "DELETE"} for method, _, _ in calls))

    def test_unknown_protection_fields_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unrecognized branch protection fields"):
            admin.protection_payload({"future_security_rule": {"enabled": True}}, actions_app_id=15368)

    def test_verify_checks_status_sources_and_unpaused_dependabot(self):
        protection = {
            "required_status_checks": {
                "strict": True,
                "contexts": list(admin.REQUIRED_CHECKS),
                "checks": [{"context": name, "app_id": 15368} for name in admin.REQUIRED_CHECKS],
            },
            "required_pull_request_reviews": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True,
                "require_last_push_approval": True,
            },
            "enforce_admins": {"enabled": True},
            "required_conversation_resolution": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        responses = {
            "repos/example/project/branches/main/protection": protection,
            "apps/github-actions": {"id": 15368},
            "repos/example/project/actions/permissions/workflow": {
                "default_workflow_permissions": "read",
                "can_approve_pull_request_reviews": False,
            },
            "repos/example/project": {
                "security_and_analysis": {
                    "secret_scanning": {"status": "enabled"},
                    "secret_scanning_push_protection": {"status": "enabled"},
                }
            },
            "repos/example/project/private-vulnerability-reporting": {"enabled": True},
            "repos/example/project/vulnerability-alerts": None,
            "repos/example/project/automated-security-fixes": {"enabled": True, "paused": False},
        }

        with patch.object(admin, "gh_api", side_effect=lambda method, endpoint, payload=None: responses[endpoint]):
            self.assertEqual(admin.verify("example/project", "main"), [])

        protection["required_status_checks"]["checks"][0]["app_id"] = None
        responses["repos/example/project/automated-security-fixes"] = {"enabled": True, "paused": True}
        with patch.object(admin, "gh_api", side_effect=lambda method, endpoint, payload=None: responses[endpoint]):
            errors = admin.verify("example/project", "main")
        self.assertTrue(any("GitHub Actions" in error for error in errors), errors)
        self.assertTrue(any("paused" in error for error in errors), errors)

        protection["required_status_checks"]["strict"] = "false"
        protection["required_pull_request_reviews"]["required_approving_review_count"] = True
        with patch.object(admin, "gh_api", side_effect=lambda method, endpoint, payload=None: responses[endpoint]):
            errors = admin.verify("example/project", "main")
        self.assertTrue(any("not strict/up-to-date" in error for error in errors), errors)
        self.assertTrue(any("at least one approving review" in error for error in errors), errors)

        responses["repos/example/project"]["security_and_analysis"]["secret_scanning"] = "enabled"
        with patch.object(admin, "gh_api", side_effect=lambda method, endpoint, payload=None: responses[endpoint]):
            errors = admin.verify("example/project", "main")
        self.assertTrue(any("secret scanning has an invalid response" in error for error in errors), errors)

    def test_repository_argument_is_required(self):
        with patch.object(sys, "argv", ["github_admin.py", "--verify"]), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                admin.main()
        self.assertEqual(result.exception.code, 2)

    def test_gh_api_extracts_http_status_from_gh_error(self):
        process = type("Process", (), {
            "returncode": 1,
            "stderr": "gh: Not Found (HTTP 404)",
            "stdout": "",
        })()
        with patch.object(admin.subprocess, "run", return_value=process):
            with self.assertRaises(admin.GitHubAPIError) as result:
                admin.gh_api("GET", "repos/example/project")
        self.assertEqual(result.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
