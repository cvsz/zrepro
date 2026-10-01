# Kubernetes / Helm Starter Pack

Adoption guide for generated projects that actually deploy to Kubernetes.

## Repository layout

```text
deploy/
  helm/<service>/
  environments/
```

## Required gates
- render Helm templates in CI;
- validate Kubernetes schema/policy;
- namespace/resource ownership is explicit;
- requests/limits are set where appropriate;
- probes reflect real application health;
- secrets are references, never committed values;
- service accounts/RBAC use least privilege;
- image tags/digests follow project supply-chain policy;
- rollout and rollback are tested;
- stateful workloads have backup/restore evidence;
- ingress/DNS ownership is not duplicated across repositories.

This pack does not assume Kubernetes is appropriate for every generated project.
