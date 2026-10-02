#!/usr/bin/env python3
"""Configure and verify GitHub repository administration gates for zRepro.

The target repository is always explicit. Dry-run is the default. Use --apply
only with an authenticated gh CLI identity that has repository Administration
permission.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

DEFAULT_BRANCH = "main"
REQUIRED_CHECKS = (
    "repository-baseline",
    "Analyze GitHub Actions",
    "dependency-review",
)
GITHUB_ACTIONS_APP_SLUG = "github-actions"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9](?:[A-Za-z0-9._-]{0,99})$")

PROTECTION_RESPONSE_FIELDS = {
    "url",
    "required_status_checks",
    "enforce_admins",
    "required_pull_request_reviews",
    "restrictions",
    "required_signatures",
    "required_linear_history",
    "allow_force_pushes",
    "allow_deletions",
    "block_creations",
    "required_conversation_resolution",
    "lock_branch",
    "allow_fork_syncing",
}
STATUS_CHECK_RESPONSE_FIELDS = {"url", "contexts_url", "strict", "contexts", "checks"}
REVIEW_RESPONSE_FIELDS = {
    "url",
    "dismissal_restrictions",
    "bypass_pull_request_allowances",
    "dismiss_stale_reviews",
    "require_code_owner_reviews",
    "required_approving_review_count",
    "require_last_push_approval",
}
ALLOWANCE_RESPONSE_FIELDS = {"url", "users_url", "teams_url", "apps_url", "users", "teams", "apps"}


class GitHubAPIError(RuntimeError):
    """A gh API request failure with an HTTP status when gh reports one."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def repository_slug(value: str) -> str:
    if not REPOSITORY_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("repository must use OWNER/REPO form")
    return value


def gh_api(method: str, endpoint: str, payload: dict[str, Any] | None = None) -> Any:
    cmd = ["gh", "api", "--hostname", "github.com", "--method", method,
           "-H", "Accept: application/vnd.github+json", endpoint]
    if payload is not None:
        cmd += ["--input", "-"]
    proc = subprocess.run(
        cmd,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        match = re.search(r"\bHTTP(?:/\S+)?\s+(\d{3})\b", proc.stderr)
        status_code = int(match.group(1)) if match else None
        raise GitHubAPIError(f"{' '.join(cmd)} failed: {proc.stderr.strip()}", status_code)
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def require_gh() -> None:
    proc = subprocess.run(
        ["gh", "auth", "status", "--hostname", "github.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("GitHub CLI is not authenticated. Run: gh auth login")


def get_github_actions_app_id() -> int:
    app = gh_api("GET", f"apps/{GITHUB_ACTIONS_APP_SLUG}")
    app_id = app.get("id") if isinstance(app, dict) else None
    if not isinstance(app_id, int) or isinstance(app_id, bool):
        raise RuntimeError("GitHub Actions App ID could not be verified")
    return app_id


def _setting_enabled(value: Any, field: str, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if not isinstance(value, dict) or set(value) - {"url", "enabled"}:
        raise ValueError(f"unrecognized branch protection setting: {field}")
    enabled = value.get("enabled", default)
    if not isinstance(enabled, bool):
        raise ValueError(f"invalid enabled value for branch protection setting: {field}")
    return enabled


def _actor_names(value: Any, actor_type: str, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"invalid {actor_type} list in {field}")
    key = {"users": "login", "teams": "slug", "apps": "slug"}[actor_type]
    names: list[str] = []
    for actor in value:
        if isinstance(actor, str):
            name = actor
        elif isinstance(actor, dict):
            name = actor.get(key)
        else:
            name = None
        if not isinstance(name, str) or not name:
            raise ValueError(f"unrecognized actor entry in {field}.{actor_type}")
        if name not in names:
            names.append(name)
    return names


def _allowance_payload(value: Any, field: str) -> dict[str, list[str]] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"unrecognized actor allowance structure: {field}")
    unknown = set(value) - ALLOWANCE_RESPONSE_FIELDS
    if unknown:
        raise ValueError(f"unrecognized actor allowance fields in {field}: {', '.join(sorted(unknown))}")
    return {
        actor_type: _actor_names(value.get(actor_type, []), actor_type, field)
        for actor_type in ("users", "teams", "apps")
    }


def _status_check_payload(current: Any, actions_app_id: int) -> dict[str, Any]:
    if current is None:
        current = {}
    if not isinstance(current, dict):
        raise ValueError("unrecognized required status check structure")
    unknown = set(current) - STATUS_CHECK_RESPONSE_FIELDS
    if unknown:
        raise ValueError(f"unrecognized required status check fields: {', '.join(sorted(unknown))}")

    contexts = current.get("contexts", [])
    current_checks = current.get("checks", [])
    if not isinstance(contexts, list) or any(not isinstance(name, str) for name in contexts):
        raise ValueError("unrecognized required status contexts")
    if not isinstance(current_checks, list):
        raise ValueError("unrecognized required status check list")

    app_ids: dict[str, int | None] = {}
    ordered_contexts: list[str] = []
    for name in contexts:
        if name not in ordered_contexts:
            ordered_contexts.append(name)
    for check in current_checks:
        if not isinstance(check, dict) or set(check) - {"context", "app_id"}:
            raise ValueError("unrecognized required status check entry")
        name = check.get("context")
        app_id = check.get("app_id")
        if not isinstance(name, str) or not name:
            raise ValueError("required status check has no context")
        if app_id is not None and (not isinstance(app_id, int) or isinstance(app_id, bool)):
            raise ValueError(f"invalid GitHub App ID for required status check: {name}")
        if name in app_ids and app_ids[name] != app_id:
            raise ValueError(f"conflicting GitHub App bindings for required status check: {name}")
        app_ids[name] = app_id
        if name not in ordered_contexts:
            ordered_contexts.append(name)

    for name in REQUIRED_CHECKS:
        if name not in ordered_contexts:
            ordered_contexts.append(name)
        # The baseline checks must always originate from GitHub Actions.
        app_ids[name] = actions_app_id

    checks = []
    for name in ordered_contexts:
        app_id = app_ids.get(name)
        # GitHub uses -1 to preserve an explicitly unbound legacy context.
        checks.append({"context": name, "app_id": app_id if app_id is not None else -1})
    # GitHub accepts either legacy contexts or structured checks for this
    # request. They must not be sent together; checks carries App bindings.
    return {"strict": True, "checks": checks}


def protection_payload(
    current_protection: dict[str, Any] | None = None,
    actions_app_id: int | None = None,
) -> dict[str, Any]:
    """Merge baseline requirements into current rules without dropping controls.

    GitHub exposes required-signature protection through a separate endpoint;
    this payload leaves that independent setting untouched.
    """
    if not isinstance(actions_app_id, int) or isinstance(actions_app_id, bool):
        raise ValueError("GitHub Actions App ID is required to build protected status checks")

    current = {} if current_protection is None else current_protection
    if not isinstance(current, dict):
        raise ValueError("unrecognized branch protection response")
    unknown = set(current) - PROTECTION_RESPONSE_FIELDS
    if unknown:
        raise ValueError(f"unrecognized branch protection fields: {', '.join(sorted(unknown))}")

    signature_rule = current.get("required_signatures")
    if signature_rule is not None:
        if not isinstance(signature_rule, dict) or set(signature_rule) - {"url", "enabled"}:
            raise ValueError("unrecognized required-signature protection structure")
        if "enabled" in signature_rule and not isinstance(signature_rule["enabled"], bool):
            raise ValueError("invalid required-signature protection state")

    status_checks = _status_check_payload(current.get("required_status_checks"), actions_app_id)

    reviews = current.get("required_pull_request_reviews") or {}
    if not isinstance(reviews, dict):
        raise ValueError("unrecognized pull request review protection structure")
    unknown_reviews = set(reviews) - REVIEW_RESPONSE_FIELDS
    if unknown_reviews:
        raise ValueError(f"unrecognized pull request review fields: {', '.join(sorted(unknown_reviews))}")
    count = reviews.get("required_approving_review_count", 0)
    if not isinstance(count, int) or isinstance(count, bool) or count < 0 or count > 6:
        raise ValueError("invalid required approving review count")
    review_payload: dict[str, Any] = {
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,
        "required_approving_review_count": max(1, count),
        "require_last_push_approval": True,
    }
    for key in ("dismissal_restrictions", "bypass_pull_request_allowances"):
        if key in reviews:
            allowance = _allowance_payload(reviews[key], f"required_pull_request_reviews.{key}")
            if allowance is not None:
                review_payload[key] = allowance

    restrictions = _allowance_payload(current.get("restrictions"), "restrictions")
    return {
        "required_status_checks": status_checks,
        "enforce_admins": True,
        "required_pull_request_reviews": review_payload,
        "restrictions": restrictions,
        "required_linear_history": _setting_enabled(current.get("required_linear_history"), "required_linear_history", False),
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": _setting_enabled(current.get("block_creations"), "block_creations", False),
        "required_conversation_resolution": True,
        "lock_branch": _setting_enabled(current.get("lock_branch"), "lock_branch", False),
        "allow_fork_syncing": _setting_enabled(current.get("allow_fork_syncing"), "allow_fork_syncing", True),
    }


def print_plan(repo: str, branch: str) -> None:
    print(f"Repository: {repo}")
    print(f"Branch: {branch}")
    print("Planned administration changes:")
    print("- require pull requests with >=1 approval")
    print("- dismiss stale reviews")
    print("- require CODEOWNERS review")
    print("- require approval after the latest push")
    print("- require conversation resolution")
    print("- require branch to be up to date")
    print("- require checks from the GitHub Actions App:")
    for check in REQUIRED_CHECKS:
        print(f"  - {check}")
    print("- preserve existing required checks, actor restrictions, review exceptions, and stronger branch rules")
    print("- enforce rules for administrators")
    print("- block force pushes and branch deletion")
    print("- enable Dependabot vulnerability alerts and automated security fixes")
    print("- enable private vulnerability reporting")
    print("- enable secret scanning and push protection where GitHub supports them")
    print("- set default Actions GITHUB_TOKEN permission to read-only")
    print("- prevent Actions from approving pull requests")


def apply(repo: str, branch: str) -> None:
    actions_app_id = get_github_actions_app_id()
    protection_endpoint = f"repos/{repo}/branches/{branch}/protection"
    try:
        current_protection = gh_api("GET", protection_endpoint)
    except GitHubAPIError as exc:
        if exc.status_code != 404:
            raise
        current_protection = None
    else:
        if not isinstance(current_protection, dict) or not current_protection:
            raise ValueError("branch protection returned an invalid response")
    protection = protection_payload(current_protection, actions_app_id)

    # Read security capabilities before the first mutation so API/read failures
    # do not leave the branch protection half-applied.
    repo_state = gh_api("GET", f"repos/{repo}")
    if not isinstance(repo_state, dict):
        raise ValueError("repository settings returned an invalid response")
    security_state = repo_state.get("security_and_analysis")
    if security_state is not None and not isinstance(security_state, dict):
        raise ValueError("repository security settings returned an invalid response")
    security = dict(security_state or {})
    desired_security = {}
    if "secret_scanning" in security:
        desired_security["secret_scanning"] = {"status": "enabled"}
    if "secret_scanning_push_protection" in security:
        desired_security["secret_scanning_push_protection"] = {"status": "enabled"}

    gh_api("PUT", protection_endpoint, protection)
    gh_api("PUT", f"repos/{repo}/vulnerability-alerts")
    gh_api("PUT", f"repos/{repo}/automated-security-fixes")
    gh_api("PUT", f"repos/{repo}/private-vulnerability-reporting")
    if desired_security:
        gh_api("PATCH", f"repos/{repo}", {"security_and_analysis": desired_security})

    gh_api(
        "PUT",
        f"repos/{repo}/actions/permissions/workflow",
        {
            "default_workflow_permissions": "read",
            "can_approve_pull_request_reviews": False,
        },
    )


def verify(repo: str, branch: str) -> list[str]:
    errors: list[str] = []
    try:
        protection = gh_api("GET", f"repos/{repo}/branches/{branch}/protection")
    except RuntimeError as exc:
        return [f"branch protection not verified: {exc}"]
    if not isinstance(protection, dict):
        return ["branch protection response has an invalid structure"]

    try:
        actions_app_id = get_github_actions_app_id()
    except RuntimeError as exc:
        actions_app_id = None
        errors.append(f"GitHub Actions check source not verified: {exc}")

    status_checks = protection.get("required_status_checks") or {}
    if not isinstance(status_checks, dict):
        errors.append("required status checks have an invalid response")
        status_checks = {}
    contexts = status_checks.get("contexts") or []
    if not isinstance(contexts, list):
        contexts = []
        errors.append("required status check contexts have an invalid response")
    context_set = set(context for context in contexts if isinstance(context, str))
    check_entries = status_checks.get("checks") or []
    check_by_name: dict[str, dict[str, Any]] = {}
    if not isinstance(check_entries, list):
        errors.append("required status check source bindings have an invalid response")
        check_entries = []
    for item in check_entries:
        if isinstance(item, dict) and isinstance(item.get("context"), str):
            context = item["context"]
            if context in check_by_name and check_by_name[context].get("app_id") != item.get("app_id"):
                errors.append(f"required status check has conflicting source bindings: {context}")
            check_by_name[context] = item

    missing_checks = sorted(set(REQUIRED_CHECKS) - context_set)
    if missing_checks:
        errors.append(f"missing required status checks: {', '.join(missing_checks)}")
    for check in REQUIRED_CHECKS:
        configured = check_by_name.get(check)
        if configured is None:
            errors.append(f"required status check source is not pinned: {check}")
        elif actions_app_id is not None:
            source_id = configured.get("app_id")
            if not isinstance(source_id, int) or isinstance(source_id, bool) or source_id != actions_app_id:
                errors.append(f"required status check is not bound to GitHub Actions: {check}")

    if status_checks.get("strict") is not True:
        errors.append("required status checks are not strict/up-to-date")

    reviews = protection.get("required_pull_request_reviews") or {}
    if not isinstance(reviews, dict):
        errors.append("pull request review settings have an invalid response")
        reviews = {}
    approving_count = reviews.get("required_approving_review_count")
    if not isinstance(approving_count, int) or isinstance(approving_count, bool) or approving_count < 1:
        errors.append("at least one approving review is not required")
    if reviews.get("dismiss_stale_reviews") is not True:
        errors.append("stale approvals are not dismissed")
    if reviews.get("require_code_owner_reviews") is not True:
        errors.append("CODEOWNERS review is not required")
    if reviews.get("require_last_push_approval") is not True:
        errors.append("approval after the latest push is not required")

    enforce_admins = protection.get("enforce_admins") or {}
    conversation_resolution = protection.get("required_conversation_resolution") or {}
    force_pushes = protection.get("allow_force_pushes") or {}
    deletions = protection.get("allow_deletions") or {}
    for name, setting in (
        ("administrator enforcement", enforce_admins),
        ("conversation resolution", conversation_resolution),
        ("force-push setting", force_pushes),
        ("branch-deletion setting", deletions),
    ):
        if not isinstance(setting, dict) or not isinstance(setting.get("enabled"), bool):
            errors.append(f"{name} has an invalid response")
    if not isinstance(enforce_admins, dict):
        enforce_admins = {}
    if not isinstance(conversation_resolution, dict):
        conversation_resolution = {}
    if not isinstance(force_pushes, dict):
        force_pushes = {}
    if not isinstance(deletions, dict):
        deletions = {}
    if enforce_admins.get("enabled") is not True:
        errors.append("branch protection is not enforced for administrators")
    if conversation_resolution.get("enabled") is not True:
        errors.append("conversation resolution is not required")
    if force_pushes.get("enabled") is True:
        errors.append("force pushes are allowed")
    if deletions.get("enabled") is True:
        errors.append("branch deletion is allowed")

    actions = gh_api("GET", f"repos/{repo}/actions/permissions/workflow")
    if not isinstance(actions, dict):
        errors.append("Actions workflow permissions have an invalid response")
        actions = {}
    if actions.get("default_workflow_permissions") != "read":
        errors.append("default Actions workflow permission is not read-only")
    if actions.get("can_approve_pull_request_reviews") is not False:
        errors.append("Actions can approve pull requests")

    repo_state = gh_api("GET", f"repos/{repo}")
    if not isinstance(repo_state, dict):
        errors.append("repository settings have an invalid response")
        security = {}
    else:
        security = repo_state.get("security_and_analysis") or {}
    if not isinstance(security, dict):
        errors.append("repository security settings have an invalid response")
        security = {}
    for key, label in (
        ("secret_scanning", "secret scanning"),
        ("secret_scanning_push_protection", "secret scanning push protection"),
    ):
        setting = security.get(key) or {}
        if not isinstance(setting, dict):
            errors.append(f"{label} has an invalid response")
        elif setting.get("status") != "enabled":
            errors.append(f"{label} is not enabled")

    try:
        private_reporting = gh_api("GET", f"repos/{repo}/private-vulnerability-reporting")
        if not isinstance(private_reporting, dict) or private_reporting.get("enabled") is not True:
            errors.append("private vulnerability reporting is not enabled")
    except RuntimeError as exc:
        errors.append(f"private vulnerability reporting not verified: {exc}")

    try:
        gh_api("GET", f"repos/{repo}/vulnerability-alerts")
    except RuntimeError as exc:
        errors.append(f"Dependabot vulnerability alerts not verified: {exc}")

    try:
        security_fixes = gh_api("GET", f"repos/{repo}/automated-security-fixes")
        if not isinstance(security_fixes, dict) or security_fixes.get("enabled") is not True:
            errors.append("Dependabot automated security fixes are not enabled")
        elif security_fixes.get("paused") is not False:
            errors.append("Dependabot automated security fixes are paused or their state is unknown")
    except RuntimeError as exc:
        errors.append(f"Dependabot automated security fixes not verified: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=repository_slug, help="Explicit GitHub repository in OWNER/REPO form")
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--apply", action="store_true", help="apply administration changes")
    parser.add_argument("--verify", action="store_true", help="verify effective settings")
    args = parser.parse_args()

    try:
        require_gh()
        print_plan(args.repo, args.branch)

        if not args.apply and not args.verify:
            print("\nDry-run only. Re-run with --repo OWNER/REPO --apply to mutate GitHub settings.")
            return 0

        if args.apply:
            apply(args.repo, args.branch)
            print("\nAdministration changes applied.")

        if args.verify or args.apply:
            errors = verify(args.repo, args.branch)
            if errors:
                print("\nVerification failed:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print("\nVERIFIED: GitHub repository administration gate is enforced.")
    except (RuntimeError, ValueError) as exc:
        print(f"github-admin: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
