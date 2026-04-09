# Sprint 2 Extension — Epics & Stories for Review

This is a human-readable view of everything in `Jira-additions.csv`. Read this **before importing** to confirm scope, descriptions, and acceptance criteria. If something looks wrong, edit it in `generate_additions.py` and re-run before import — that's faster than fixing it in Jira after.

**Total: 2 epics, 14 stories, 45 story points**

| | Count | Points |
|---|---|---|
| Epic 3 — K8s Migration | 11 stories | 37 |
| Epic 4 — AI Triage Hardening | 3 stories | 8 |

**Sprint:** SCRUM Sprint 2 (extended) · **Due date:** 23/Apr/26 · **Status (all):** To Do

---

# Epic 3 — Kubernetes Migration of Monitored Target

**Priority:** High · **Labels:** Kubernetes

Migrate the monitored infrastructure (Spring Boot, Kong, AI RCA pipeline, Ollama) from per-VM docker-compose to a single-node k3s cluster on EC2. The monitoring stack (Prometheus, Grafana, Loki, Jaeger) stays on its own VM and reaches into the cluster via `kubernetes_sd_configs` and an in-cluster OTel Collector DaemonSet.

**Goals:**
- Single-node k3s cluster on EC2 (HA deferred)
- Three Helm charts: Spring Boot (in-house), Kong (upstream), AI stack (in-house)
- First-party images built locally and imported into k3s containerd (no registry, no CI)
- Monitoring VM unchanged but reconfigured to scrape the cluster
- All 17 Grafana alert rules migrated to K8s label selectors
- End-to-end validation against the K8s target

**Out of scope (sprint 3+):**
- Multi-node HA / k3s embedded etcd
- ArgoCD / GitOps adoption
- Calico / Cilium for NetworkPolicy enforcement
- Longhorn for distributed storage
- Migrating the monitoring stack itself to K8s (deliberately rejected)

---

## E3-00: Team K8s onboarding — Phases 1-4 of the Kubernetes guide on k3d
**Priority:** Highest · **Points:** 3 · **Labels:** Kubernetes

> As a developer working on the Kubernetes migration, I need hands-on familiarity with K8s primitives so that I can build Epic 3 stories without conceptual misunderstandings.

**Acceptance Criteria:**
- Each contributor brings up a local k3d cluster
- Walks through Phases 1-4 of the Kubernetes guide:
  - Phase 1: deploy nginx, port-forward, watch self-healing
  - Phase 2: ConfigMap, Secret, PVC, namespaces, Job, DaemonSet
  - Phase 3: DNS resolution, Service vs Pod IPs, NetworkPolicy
  - Phase 4: install kube-prometheus-stack via Helm, override values
- 30-min pair walkthrough with a teammate to demonstrate understanding
- Reference: https://github.com/linalaaraich/monitoring-docs/blob/main/kubernetes-guide.html

**Blocks:** ALL other E3 stories

---

## E3-01: Bootstrap k3s on EC2 via Ansible
**Priority:** Highest · **Points:** 3 · **Labels:** Kubernetes

> As a platform engineer, I need a single-node k3s cluster running on EC2 so that the Helm-deployed workloads have somewhere to run.

**Acceptance Criteria:**
- `xanmanning.k3s` role added to `requirements.yml`, version `v3.4.4` pinned
- New playbook `playbooks/k3s.yml` bootstraps k3s on a single host
- `k3s_release_version` pinned to a specific `v1.30.x+k3s1` release
- Traefik disabled (`k3s_server.disable: [traefik]`)
- `write-kubeconfig-mode: "0644"`
- kubeconfig fetched back to control machine, server URL rewritten from `127.0.0.1` to EC2 IP
- New inventory group `k3s_cluster` wired into `site.yml`
- Verification: `kubectl get nodes` returns 1 Ready node from the control machine

**Blocks:** E3-03 → E3-10
**Blocked by:** E3-00, SCRUM-63 (rescoped Terraform)

---

## E3-02: Image build + k3s containerd import via Ansible (no registry, no CI)
**Priority:** Highest · **Points:** 3 · **Labels:** Kubernetes

> As a platform engineer, I need first-party container images (triage service + 5 MCP servers) loaded into the k3s host's containerd cache so that Helm-deployed pods can run them without a registry.

**Why no registry/CI:** single-node k3s with one or two contributors. ECR + GitHub Actions adds operational surface area we don't need. k3s containerd lets us import tarballs directly.

**Acceptance Criteria:**
- Dockerfiles for triage + 5 MCP servers exist (extracted from current docker-compose builds)
- Ansible role/tasks that, for each image:
  1. `docker build -t cires/<name>:<tag> <context>`
  2. `docker save cires/<name>:<tag> -o /tmp/<name>.tar`
  3. `sudo k3s ctr images import /tmp/<name>.tar` (on k3s host)
- Image tag pinned via single `image_tag` variable in group_vars
- All Helm charts reference `cires/<name>:<image_tag>` with `imagePullPolicy: IfNotPresent`
- Verification: `sudo k3s crictl images` shows all 6 `cires/*` images
- Verification: `helm install` of AI stack succeeds without `ImagePullBackOff`
- README documents build+import flow and the upgrade path to ECR+CI when multi-node is needed

**Blocks:** E3-05
**Blocked by:** E3-00, E3-01

---

## E3-03: Helm chart — Spring Boot backend
**Priority:** High · **Points:** 3 · **Labels:** Kubernetes

> As a developer, I need a Helm chart that deploys the Spring Boot backend into k3s so that the application is reachable from Kong and can talk to RDS.

**Acceptance Criteria:**
- New chart at `charts/spring-boot/` with `Chart.yaml`, `values.yaml`, `templates/`
- Deployment template: configurable replicas, resource requests + limits
- Liveness probe (`/actuator/health/liveness`), readiness probe (`/actuator/health/readiness`)
- Service template (ClusterIP, port 80 → targetPort 8080)
- ConfigMap for Spring application properties
- Secret reference for RDS credentials (`DB_USERNAME`, `DB_PASSWORD`, `DB_URL`)
- ServiceAccount for the pod
- Image pinned by tag (no `:latest`)
- Installable via `helm install spring-boot charts/spring-boot/ -n app --create-namespace`
- Pod reaches RDS (verified via `/actuator/health`)
- Spring Boot logs include `trace_id` (OTel agent injected)

**Blocks:** E3-09, E3-10
**Blocked by:** E3-01

---

## E3-04: Helm chart — Kong via upstream chart
**Priority:** High · **Points:** 3 · **Labels:** Kubernetes

> As a platform engineer, I need Kong running inside the cluster as the API gateway.

**Acceptance Criteria:**
- Upstream `kong/kong` Helm chart, `chart_version` pinned (e.g. `2.38.0`)
- DB-less mode enabled
- Existing `kong.yml` converted to a ConfigMap mounted into the Kong pod
- Upstream URLs in `kong.yml` rewritten from `application_vm_ip:8080` to `spring-boot.app.svc.cluster.local:80`
- React frontend route still points to CloudFront
- OTel plugin enabled, sends spans to in-cluster OTel Collector via OTLP
- Prometheus plugin enabled, `/metrics` scraped by Prometheus K8s SD
- Service exposed externally via NodePort or LoadBalancer (decision documented)
- Verification: curl through Kong reaches Spring Boot, traces appear in Jaeger

**Blocks:** E3-09, E3-10
**Blocked by:** E3-01, E3-03

---

## E3-05: Helm chart — AI stack
**Priority:** High · **Points:** 5 · **Labels:** Kubernetes

> As an SRE, I need the entire AI RCA pipeline deployed via a single Helm chart so triage, MCP servers, and Ollama share a lifecycle and can roll back together.

**Acceptance Criteria:**
- New chart at `charts/ai-stack/` containing:
  - Triage service Deployment + Service (port 8090)
  - 5× MCP server Deployments + Services (Prometheus :8091, Loki :8092, Jaeger :8093, Drain3 :8094, RCA History :8095)
  - Ollama Deployment with PVC for model storage (20Gi minimum)
  - GPU resource request on Ollama: `nvidia.com/gpu: 1`
  - Init Job or postStart hook that pulls the Ollama model on first deploy
  - Secret for SMTP credentials and Ollama config
  - All inter-service references use Service DNS (no `localhost`, no hardcoded IPs)
- All image references pinned to tags from E3-02
- Resource requests + limits per container
- Liveness + readiness probes per container
- Verification: triage `/health` responds, MCP servers respond, Ollama returns model list

**Blocks:** E3-09, E3-10
**Blocked by:** E3-01, E3-02, E3-06

---

## E3-06: NVIDIA device plugin DaemonSet + Ollama GPU verification spike
**Priority:** Highest · **Points:** 5 · **Labels:** Kubernetes

> As a platform engineer, I need to verify GPU passthrough on k3s so Ollama can use the GPU. **This is a spike — plan for fiddly debugging.**

**Acceptance Criteria:**
- NVIDIA Container Toolkit installed on the k3s host (via repurposed `nvidia_docker` role)
- containerd configured with the nvidia runtime
- NVIDIA device plugin DaemonSet deployed (`k8s-device-plugin v0.15.0`)
- Test pod requesting `nvidia.com/gpu: 1` runs and `nvidia-smi` output is visible
- Troubleshooting guide added to `monitoring-docs` (driver mismatch, runtime not configured, plugin CrashLoopBackOff)
- Decision documented: GPU on the same EC2 or separate `g4dn.xlarge` worker node
- If separate: node tainted, Ollama pod has matching toleration

**Blocks:** E3-05
**Blocked by:** E3-01

---

## E3-07: In-cluster OTel Collector DaemonSet
**Priority:** High · **Points:** 3 · **Labels:** Kubernetes

> As an observability engineer, I need an OTel Collector running on every K8s node so container logs and traces are enriched with K8s metadata and forwarded to the monitoring VM.

**Acceptance Criteria:**
- New manifest set or chart deploys:
  - Namespace `observability`
  - ServiceAccount + ClusterRole granting access to `nodes`/`pods`/`namespaces`
  - DaemonSet running `otel/opentelemetry-collector-contrib` (version pinned)
  - ConfigMap with collector config:
    - `filelog` receiver tailing `/var/log/pods/*/*/*.log`
    - `k8sattributes` processor enriching with `pod`, `namespace`, `container`, `trace_id`
    - OTLP receiver on `:4317` / `:4318`
    - OTLP exporter pushing to `monitoring_vm_ip:4317`
- Per-VM OTel Collector containers retired from compose templates
- Verification: Spring Boot log line appears in Loki on the monitoring VM with correct labels
- Verification: trace from Spring Boot or Kong appears in Jaeger

**Blocks:** E3-10
**Blocked by:** E3-01, E3-03, E3-04, E3-05

---

## E3-08: Prometheus kubernetes_sd_configs scrape job + RBAC
**Priority:** High · **Points:** 3 · **Labels:** Kubernetes

> As an observability engineer, I need the existing external Prometheus to discover and scrape K8s-hosted services so all metrics keep flowing to the same datastore.

**Acceptance Criteria:**
- New ServiceAccount `prometheus-scraper` in namespace `observability`
- ClusterRole granting `get/list/watch` on `nodes`, `pods`, `services`, `endpoints` + `nonResourceURLs /metrics`
- ClusterRoleBinding to the SA
- SA token extracted, stored as Ansible vault secret on the monitoring VM
- `roles/prometheus` updated with `kubernetes_sd_configs` scrape job:
  - `role: pod`, with annotation-based filtering
  - `api_server`: k3s host `:6443`
  - `bearer_token_file`: the new secret
  - `relabel_configs`: keep pods with `prometheus.io/scrape='true'`, use `prometheus.io/port`
- Security group on k3s EC2 allows monitoring VM IP on `:6443` and `:10250`
- Verification: Prometheus targets page shows healthy K8s targets

**Blocks:** E3-09, E3-10
**Blocked by:** E3-01, SCRUM-63 (security group update)

---

## E3-09: Migrate the 17 Grafana alert rules to K8s pod-based label selectors
**Priority:** Highest · **Points:** 3 · **Labels:** Kubernetes

> As an SRE, I need every Grafana alert rule's selector updated to match the K8s-hosted target so alerts continue to fire correctly. **High-risk: silent failure if missed.**

**Acceptance Criteria:**
- Audit current Grafana alerting: 17 rules in 3 groups (per `CLAUDE.md`)
- Rewrite each rule's label selector:
  - Old: `instance='application_vm_ip:8080'` → New: `pod=~'spring-boot.*', namespace='app'`
  - Old: `instance='network_vm_ip:8000'` → New: `pod=~'kong.*', namespace='network'`
  - Old: `instance='ai_vm_ip:8090'` → New: `pod=~'triage.*', namespace='ai'`
- Updated rules committed to git, applied via Grafana provisioning
- Each rule manually triggered and verified to fire
- Triage service receives the test webhook for each rule
- No rule left with a stale selector

**Blocks:** E3-10
**Blocked by:** E3-03, E3-04, E3-05, E3-08

---

## E3-10: End-to-end K8s validation playbook
**Priority:** Highest · **Points:** 3 · **Labels:** Kubernetes

> As an SRE, I need an automated end-to-end test against the K8s target so the migration is provably complete.

**Acceptance Criteria:**
- New playbook `playbooks/integration-k8s.yml` (or update existing `integration.yml`)
- Test sequence:
  1. Run `load-test.sh` against Kong's external endpoint
  2. Verify Spring Boot pod metrics in Prometheus (RED)
  3. Verify Spring Boot logs in Loki with `trace_id` label
  4. Verify trace in Jaeger end-to-end (Kong → Spring → RDS)
  5. Trigger an alert (high latency)
  6. Verify Grafana alert fires
  7. Verify webhook arrives at triage service
  8. Verify triage produces a verdict
  9. Verify LLM analysis runs and returns RCA JSON
  10. Verify escalation email sent (or DISMISS logged)
- All checks scripted, exit code 0 = pass
- Replaces SCRUM-66 (E1-05) — that ticket closes in favor of this one

**Blocked by:** E3-03, E3-04, E3-05, E3-06, E3-07, E3-08, E3-09

---

# Epic 4 — AI Triage Service Hardening

**Priority:** Medium · **Labels:** AI

Targeted reliability and observability improvements to the AI triage pipeline beyond the MVP. Three high-leverage stories covering the most impactful weaknesses identified after Epic 2. Larger AI maturity work (calibration sets, prompt engineering, model A/B testing) is deferred to a future sprint.

**Goals:**
- Eliminate Ollama-related pipeline hangs
- Replace fragile free-text parsing with strict JSON schema enforcement
- Add self-observability so future iteration is data-driven

---

## AI-01: Ollama call hardening — timeout, retry, circuit breaker, fallback
**Priority:** Highest · **Points:** 3 · **Labels:** AI

> As an SRE, I need the triage service's Ollama calls to be resilient to timeouts and failures so a slow or hung Ollama doesn't stall the pipeline.

**Acceptance Criteria:**
- Configurable per-request timeout (default 30s, override via env var)
- Retry policy: up to 2 retries with exponential backoff on transient failures
- Circuit breaker: after 5 consecutive failures, mark Ollama "down" for 60s cooldown
- Fallback: when circuit open or retries exhausted, produce `NEEDS_HUMAN_REVIEW` verdict with raw alert context, sent via existing escalation email path
- Metrics: `ollama_request_duration_seconds`, `ollama_request_total{status}`, `ollama_circuit_state`
- Unit tests for timeout, retry, circuit breaker open/close transitions
- Manual test: kill Ollama mid-request, verify pipeline produces fallback within timeout + retry budget

---

## AI-02: JSON schema enforcement on LLM verdict
**Priority:** Highest · **Points:** 2 · **Labels:** AI

> As an SRE, I need the LLM verdict to be structured JSON validated against a strict schema so triage can reliably parse it without fragile string matching.

**Acceptance Criteria:**
- Ollama API call uses `format: json` parameter (Ollama JSON mode)
- System prompt instructs the model to return JSON matching a documented schema
- Pydantic model for the verdict:
  ```
  {
    verdict: 'ESCALATE' | 'DISMISS' | 'INCONCLUSIVE',
    confidence: 0-1,
    root_cause: str,
    evidence: [str],
    recommended_actions: [str],
    alert_id: str
  }
  ```
- Validator runs on every LLM response; on schema failure, retry once with the validation error appended
- On second failure, escalate to `NEEDS_HUMAN_REVIEW` (uses fallback path from AI-01)
- Existing free-text `ESCALATE/DISMISS` parser removed
- Unit tests for valid response, schema failure, retry recovery, double failure
- Schema documented in `monitoring-docs`

---

## AI-03: Triage service self-observability — /metrics endpoint
**Priority:** High · **Points:** 3 · **Labels:** AI

> As an SRE, I need the triage service to expose its own operational metrics so I can observe and improve its behavior.

**Acceptance Criteria:**
- Triage service exposes `/metrics` in Prometheus format
- Metrics:
  - `triage_alerts_received_total{source}`
  - `triage_alerts_processed_total{verdict}`
  - `triage_decision_duration_seconds` (histogram)
  - `triage_queue_depth` (gauge)
  - `triage_mcp_request_total{server,status}`
  - `triage_mcp_duration_seconds{server}` (histogram)
  - `triage_llm_token_count{type='prompt'|'completion'}` (histogram)
  - `triage_fallback_total{reason}`
  - `triage_email_sent_total{status}`
- Prometheus annotations on the triage Service (`prometheus.io/scrape`, `/port`, `/path`)
- New Grafana panel "Triage Service Health" added to `unified-overview`:
  - Decision throughput, latency p50/p95/p99, verdict breakdown, MCP error rates, fallback rate
- Dashboard JSON committed to git
- Verification: test alert produces visible metric updates within 30s

---

# Critical path

```
E3-00 (learning) ──────► blocks ALL E3 work
                             │
SCRUM-63 (Terraform rescope) ┴─► E3-01 (k3s) ──┬─► E3-06 (NVIDIA spike)
                                                │
                                E3-02 (images) ─┤
                                                │
                                                ▼
                                E3-03 (Spring) ──┐
                                E3-04 (Kong) ────┤
                                E3-05 (AI stack) ┤
                                                  │
                                                  ▼
                                E3-07 (OTel DS) ──┐
                                E3-08 (Prom SD) ──┤
                                E3-09 (alerts) ───┤
                                                  │
                                                  ▼
                                              E3-10 (e2e validation)

AI-01, AI-02, AI-03 ──► independent of K8s, can run anytime in parallel
                        easier to test once E3-10 is green
```

**Spine:** E3-00 → E3-01 → E3-02 → (E3-03/04/05 in parallel with E3-06) → (E3-07/08/09 in parallel) → E3-10

---

# Sprint 2 totals after extension

| | Count |
|---|---|
| Existing in-flight stories | ~11 still need finishing (of 20 total) |
| New K8s stories | 11 (37 points) |
| New AI stories | 3 (8 points) |
| Existing stories rescoped | 3 (SCRUM-63, 64, 65 — see README) |
| Existing stories closed as superseded | 2 (SCRUM-66, 82 — see README) |
| **Total to ship by Apr 23** | **~25 stories, ~115 points** |

---

# Review checklist

Before importing the CSV, confirm:

- [ ] All 16 items above match your understanding of the work
- [ ] Story points feel right for your team's velocity
- [ ] Priorities feel right (Highest = on the critical path, High = important, Medium = lower)
- [ ] Labels feel right (Kubernetes for E3, AI for Epic 4)
- [ ] You're OK with the architectural decisions documented:
  - Monitoring stack stays on its own VM (not migrated to K8s)
  - k3s as the K8s distribution
  - 3 separate Helm charts (not one umbrella)
  - No registry / CI for first-party images (k3s containerd import instead)
  - Single-node cluster (HA deferred)
  - Disable Traefik, keep Kong as gateway
- [ ] You're OK closing SCRUM-66 and SCRUM-82 as superseded
- [ ] You're OK rescoping SCRUM-63, 64, 65 in place (descriptions in README)

If any of those is "no", **edit `generate_additions.py`** and re-run before import — easier than fixing in Jira after.
