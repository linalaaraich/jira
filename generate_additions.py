#!/usr/bin/env python3
"""
Generate a clean Jira-import CSV for the sprint 2 extension.

Output: Jira-additions.csv

Only 12 columns — the minimum Jira CSV import needs. No Jira export artifacts,
no duplicated Labels columns, no Team Id / Custom field (Vulnerability) / Σ fields.

Columns:
  1. Summary
  2. Issue Type
  3. Status
  4. Priority
  5. Labels
  6. Description
  7. Sprint
  8. Story Points
  9. Parent (epic key for stories, blank for epics)
 10. Reporter
 11. Assignee
 12. Due date

16 rows total: 2 epics + 11 K8s stories + 3 AI stories.
"""

import csv

USER = "Lina Laaraich"
SPRINT_NAME = "SCRUM Sprint 2"
SPRINT_DUE = "23/Apr/26"

HEADERS = [
    "Summary",
    "Issue Type",
    "Status",
    "Priority",
    "Labels",
    "Description",
    "Sprint",
    "Story Points",
    "Parent",
    "Reporter",
    "Assignee",
    "Due date",
]


def row(*, summary, issue_type, priority, description,
        labels="", story_points="", parent="", due_date=SPRINT_DUE):
    """Build a 12-column row."""
    return [
        summary,
        issue_type,
        "To Do",
        priority,
        labels,
        description,
        SPRINT_NAME,
        str(story_points) if story_points else "",
        parent,
        USER,
        USER if issue_type != "Epic" else "",
        due_date,
    ]


# ============================================================================
# 16 NEW ITEMS
# ============================================================================

EPIC3_SUMMARY = "Epic 3 -- Kubernetes Migration of Monitored Target"
EPIC4_SUMMARY = "Epic 4 -- AI Triage Service Hardening"

items = []

# ---- Epic 3 ----
items.append(row(
    summary=EPIC3_SUMMARY,
    issue_type="Epic", priority="High",
    labels="Kubernetes",
    description=(
        "Migrate the monitored infrastructure (Spring Boot, Kong, AI RCA pipeline, Ollama) "
        "from per-VM docker-compose to a single-node k3s cluster on EC2. The monitoring stack "
        "(Prometheus, Grafana, Loki, Jaeger) stays on its own VM and reaches into the cluster "
        "via kubernetes_sd_configs and an in-cluster OTel Collector DaemonSet.\n\n"
        "Goals:\n"
        "- Single-node k3s cluster on EC2 (HA deferred)\n"
        "- Three Helm charts: Spring Boot (in-house), Kong (upstream), AI stack (in-house)\n"
        "- First-party images built locally and imported into k3s containerd (no registry, no CI)\n"
        "- Monitoring VM unchanged but reconfigured to scrape the cluster\n"
        "- All 17 Grafana alert rules migrated to K8s label selectors\n"
        "- End-to-end validation against the K8s target\n\n"
        "Out of scope (sprint 3+):\n"
        "- Multi-node HA / k3s embedded etcd\n"
        "- ArgoCD / GitOps adoption\n"
        "- Calico / Cilium for NetworkPolicy enforcement\n"
        "- Longhorn for distributed storage\n"
        "- Migrating the monitoring stack itself to K8s (deliberately rejected)"
    ),
))

# ---- E3-00 ----
items.append(row(
    summary="E3-00: Team K8s onboarding — Phases 1-4 of the Kubernetes guide on k3d",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a developer working on the Kubernetes migration, I need hands-on familiarity with "
        "K8s primitives so that I can build Epic 3 stories without conceptual misunderstandings.\n\n"
        "Acceptance Criteria:\n"
        "- Each contributor brings up a local k3d cluster\n"
        "- Walks through Phases 1-4 of the Kubernetes guide:\n"
        "  Phase 1: deploy nginx, port-forward, watch self-healing\n"
        "  Phase 2: ConfigMap, Secret, PVC, namespaces, Job, DaemonSet\n"
        "  Phase 3: DNS resolution, Service vs Pod IPs, NetworkPolicy\n"
        "  Phase 4: install kube-prometheus-stack via Helm, override values\n"
        "- 30-min pair walkthrough with a teammate to demonstrate understanding\n"
        "- Reference: https://github.com/linalaaraich/monitoring-docs/blob/main/kubernetes-guide.html\n\n"
        "Blocks: ALL other E3 stories"
    ),
))

# ---- E3-01 ----
items.append(row(
    summary="E3-01: Bootstrap k3s on EC2 via Ansible — xanmanning.k3s, pinned, Traefik disabled",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a platform engineer, I need a single-node k3s cluster running on EC2 so that the "
        "Helm-deployed workloads have somewhere to run.\n\n"
        "Acceptance Criteria:\n"
        "- xanmanning.k3s role added to requirements.yml, version v3.4.4 pinned\n"
        "- New playbook playbooks/k3s.yml bootstraps k3s on a single host\n"
        "- k3s_release_version pinned to a specific v1.30.x+k3s1 release\n"
        "- Traefik disabled (k3s_server.disable: [traefik])\n"
        "- write-kubeconfig-mode: '0644'\n"
        "- kubeconfig fetched back to control machine, server URL rewritten from 127.0.0.1 to EC2 IP\n"
        "- New inventory group k3s_cluster wired into site.yml\n"
        "- Verification: kubectl get nodes returns 1 Ready node from the control machine\n\n"
        "Blocks: E3-03 through E3-10\n"
        "Blocked by: E3-00, SCRUM-63 (rescoped Terraform)"
    ),
))

# ---- E3-02 ----
items.append(row(
    summary="E3-02: Image build + k3s containerd import via Ansible (no registry, no CI)",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a platform engineer, I need first-party container images (triage service + 5 MCP "
        "servers) loaded into the k3s host's containerd cache so that Helm-deployed pods can "
        "run them without a registry.\n\n"
        "Why no registry/CI: single-node k3s with one or two contributors. ECR + GitHub Actions "
        "adds operational surface area we don't need. k3s containerd lets us import tarballs directly.\n\n"
        "Acceptance Criteria:\n"
        "- Dockerfiles for triage + 5 MCP servers exist (extracted from current docker-compose builds)\n"
        "- Ansible role/tasks that, for each image:\n"
        "  1. docker build -t cires/<name>:<tag> <context>\n"
        "  2. docker save cires/<name>:<tag> -o /tmp/<name>.tar\n"
        "  3. sudo k3s ctr images import /tmp/<name>.tar (on k3s host)\n"
        "- Image tag pinned via single image_tag variable in group_vars\n"
        "- All Helm charts reference cires/<name>:<image_tag> with imagePullPolicy: IfNotPresent\n"
        "- Verification: sudo k3s crictl images shows all 6 cires/* images\n"
        "- Verification: helm install of AI stack succeeds without ImagePullBackOff\n"
        "- README documents build+import flow and the upgrade path to ECR+CI when multi-node is needed\n\n"
        "Blocks: E3-05\n"
        "Blocked by: E3-00, E3-01"
    ),
))

# ---- E3-03 ----
items.append(row(
    summary="E3-03: Helm chart — Spring Boot backend (Deployment + Service + ConfigMap + probes)",
    issue_type="Story", priority="High", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a developer, I need a Helm chart that deploys the Spring Boot backend into k3s "
        "so that the application is reachable from Kong and can talk to RDS.\n\n"
        "Acceptance Criteria:\n"
        "- New chart at charts/spring-boot/ with Chart.yaml, values.yaml, templates/\n"
        "- Deployment template: configurable replicas, resource requests + limits\n"
        "- Liveness probe (/actuator/health/liveness), readiness probe (/actuator/health/readiness)\n"
        "- Service template (ClusterIP, port 80 -> targetPort 8080)\n"
        "- ConfigMap for Spring application properties\n"
        "- Secret reference for RDS credentials (DB_USERNAME, DB_PASSWORD, DB_URL)\n"
        "- ServiceAccount for the pod\n"
        "- Image pinned by tag (no :latest)\n"
        "- Installable via helm install spring-boot charts/spring-boot/ -n app --create-namespace\n"
        "- Pod reaches RDS (verified via /actuator/health)\n"
        "- Spring Boot logs include trace_id (OTel agent injected)\n\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01"
    ),
))

# ---- E3-04 ----
items.append(row(
    summary="E3-04: Helm chart — Kong via upstream chart, DB-less mode, kong.yml as ConfigMap",
    issue_type="Story", priority="High", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a platform engineer, I need Kong running inside the cluster as the API gateway.\n\n"
        "Acceptance Criteria:\n"
        "- Upstream kong/kong Helm chart, chart_version pinned (e.g. 2.38.0)\n"
        "- DB-less mode enabled\n"
        "- Existing kong.yml converted to a ConfigMap mounted into the Kong pod\n"
        "- Upstream URLs in kong.yml rewritten from application_vm_ip:8080 to spring-boot.app.svc.cluster.local:80\n"
        "- React frontend route still points to CloudFront\n"
        "- OTel plugin enabled, sends spans to in-cluster OTel Collector via OTLP\n"
        "- Prometheus plugin enabled, /metrics scraped by Prometheus K8s SD\n"
        "- Service exposed externally via NodePort or LoadBalancer (decision documented)\n"
        "- Verification: curl through Kong reaches Spring Boot, traces appear in Jaeger\n\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, E3-03"
    ),
))

# ---- E3-05 ----
items.append(row(
    summary="E3-05: Helm chart — AI stack (triage service + 5 MCP servers + Ollama)",
    issue_type="Story", priority="High", story_points=5,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As an SRE, I need the entire AI RCA pipeline deployed via a single Helm chart so "
        "triage, MCP servers, and Ollama share a lifecycle and can roll back together.\n\n"
        "Acceptance Criteria:\n"
        "- New chart at charts/ai-stack/ containing:\n"
        "  - Triage service Deployment + Service (port 8090)\n"
        "  - 5x MCP server Deployments + Services (Prometheus :8091, Loki :8092, Jaeger :8093, Drain3 :8094, RCA History :8095)\n"
        "  - Ollama Deployment with PVC for model storage (20Gi minimum)\n"
        "  - GPU resource request on Ollama: nvidia.com/gpu: 1\n"
        "  - Init Job or postStart hook that pulls the Ollama model on first deploy\n"
        "  - Secret for SMTP credentials and Ollama config\n"
        "  - All inter-service references use Service DNS\n"
        "- All image references pinned to tags from E3-02\n"
        "- Resource requests + limits per container\n"
        "- Liveness + readiness probes per container\n"
        "- Verification: triage /health responds, MCP servers respond, Ollama returns model list\n\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, E3-02, E3-06"
    ),
))

# ---- E3-06 ----
items.append(row(
    summary="E3-06: NVIDIA device plugin DaemonSet + Ollama GPU verification spike",
    issue_type="Story", priority="Highest", story_points=5,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As a platform engineer, I need to verify GPU passthrough on k3s so Ollama can use the GPU. "
        "This is a spike — plan for fiddly debugging.\n\n"
        "Acceptance Criteria:\n"
        "- NVIDIA Container Toolkit installed on the k3s host (via repurposed nvidia_docker role)\n"
        "- containerd configured with the nvidia runtime\n"
        "- NVIDIA device plugin DaemonSet deployed (k8s-device-plugin v0.15.0)\n"
        "- Test pod requesting nvidia.com/gpu: 1 runs and nvidia-smi output is visible\n"
        "- Troubleshooting guide added to monitoring-docs (driver mismatch, runtime not configured, plugin CrashLoopBackOff)\n"
        "- Decision documented: GPU on the same EC2 or separate g4dn.xlarge worker node\n"
        "- If separate: node tainted, Ollama pod has matching toleration\n\n"
        "Blocks: E3-05\n"
        "Blocked by: E3-01"
    ),
))

# ---- E3-07 ----
items.append(row(
    summary="E3-07: In-cluster OTel Collector DaemonSet — log/trace forwarding to monitoring VM",
    issue_type="Story", priority="High", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As an observability engineer, I need an OTel Collector running on every K8s node so "
        "container logs and traces are enriched with K8s metadata and forwarded to the monitoring VM.\n\n"
        "Acceptance Criteria:\n"
        "- New manifest set or chart deploys:\n"
        "  - Namespace observability\n"
        "  - ServiceAccount + ClusterRole granting access to nodes/pods/namespaces\n"
        "  - DaemonSet running otel/opentelemetry-collector-contrib (version pinned)\n"
        "  - ConfigMap with collector config:\n"
        "    * filelog receiver tailing /var/log/pods/*/*/*.log\n"
        "    * k8sattributes processor enriching with pod, namespace, container, trace_id\n"
        "    * OTLP receiver on :4317 / :4318\n"
        "    * OTLP exporter pushing to monitoring_vm_ip:4317\n"
        "- Per-VM OTel Collector containers retired from compose templates\n"
        "- Verification: Spring Boot log line appears in Loki on the monitoring VM with correct labels\n"
        "- Verification: trace from Spring Boot or Kong appears in Jaeger\n\n"
        "Blocks: E3-10\n"
        "Blocked by: E3-01, E3-03, E3-04, E3-05"
    ),
))

# ---- E3-08 ----
items.append(row(
    summary="E3-08: Prometheus kubernetes_sd_configs scrape job + RBAC for monitoring VM",
    issue_type="Story", priority="High", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As an observability engineer, I need the existing external Prometheus to discover and "
        "scrape K8s-hosted services so all metrics keep flowing to the same datastore.\n\n"
        "Acceptance Criteria:\n"
        "- New ServiceAccount prometheus-scraper in namespace observability\n"
        "- ClusterRole granting get/list/watch on nodes, pods, services, endpoints + nonResourceURLs /metrics\n"
        "- ClusterRoleBinding to the SA\n"
        "- SA token extracted, stored as Ansible vault secret on the monitoring VM\n"
        "- roles/prometheus updated with kubernetes_sd_configs scrape job:\n"
        "  - role: pod, with annotation-based filtering\n"
        "  - api_server: k3s host :6443\n"
        "  - bearer_token_file: the new secret\n"
        "  - relabel_configs: keep pods with prometheus.io/scrape='true', use prometheus.io/port\n"
        "- Security group on k3s EC2 allows monitoring VM IP on :6443 and :10250\n"
        "- Verification: Prometheus targets page shows healthy K8s targets\n\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, SCRUM-63 (security group update)"
    ),
))

# ---- E3-09 ----
items.append(row(
    summary="E3-09: Migrate the 17 Grafana alert rules to K8s pod-based label selectors",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As an SRE, I need every Grafana alert rule's selector updated to match the K8s-hosted "
        "target so alerts continue to fire correctly. High-risk: silent failure if missed.\n\n"
        "Acceptance Criteria:\n"
        "- Audit current Grafana alerting: 17 rules in 3 groups (per CLAUDE.md)\n"
        "- Rewrite each rule's label selector:\n"
        "  - Old: instance='application_vm_ip:8080' -> New: pod=~'spring-boot.*', namespace='app'\n"
        "  - Old: instance='network_vm_ip:8000'     -> New: pod=~'kong.*',        namespace='network'\n"
        "  - Old: instance='ai_vm_ip:8090'           -> New: pod=~'triage.*',      namespace='ai'\n"
        "- Updated rules committed to git, applied via Grafana provisioning\n"
        "- Each rule manually triggered and verified to fire\n"
        "- Triage service receives the test webhook for each rule\n"
        "- No rule left with a stale selector\n\n"
        "Blocks: E3-10\n"
        "Blocked by: E3-03, E3-04, E3-05, E3-08"
    ),
))

# ---- E3-10 ----
items.append(row(
    summary="E3-10: End-to-end K8s validation playbook — full pipeline against K8s target",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC3_SUMMARY,
    labels="Kubernetes",
    description=(
        "As an SRE, I need an automated end-to-end test against the K8s target so the migration "
        "is provably complete.\n\n"
        "Acceptance Criteria:\n"
        "- New playbook playbooks/integration-k8s.yml (or update existing integration.yml)\n"
        "- Test sequence:\n"
        "  1. Run load-test.sh against Kong's external endpoint\n"
        "  2. Verify Spring Boot pod metrics in Prometheus (RED)\n"
        "  3. Verify Spring Boot logs in Loki with trace_id label\n"
        "  4. Verify trace in Jaeger end-to-end (Kong -> Spring -> RDS)\n"
        "  5. Trigger an alert (high latency)\n"
        "  6. Verify Grafana alert fires\n"
        "  7. Verify webhook arrives at triage service\n"
        "  8. Verify triage produces a verdict\n"
        "  9. Verify LLM analysis runs and returns RCA JSON\n"
        " 10. Verify escalation email sent (or DISMISS logged)\n"
        "- All checks scripted, exit code 0 = pass\n"
        "- Replaces SCRUM-66 (E1-05) — that ticket closes in favor of this one\n\n"
        "Blocked by: E3-03, E3-04, E3-05, E3-06, E3-07, E3-08, E3-09"
    ),
))

# ---- Epic 4 ----
items.append(row(
    summary=EPIC4_SUMMARY,
    issue_type="Epic", priority="Medium",
    labels="AI",
    description=(
        "Targeted reliability and observability improvements to the AI triage pipeline beyond "
        "the MVP. Three high-leverage stories covering the most impactful weaknesses identified "
        "after Epic 2. Larger AI maturity work (calibration sets, prompt engineering, model "
        "A/B testing) is deferred to a future sprint.\n\n"
        "Goals:\n"
        "- Eliminate Ollama-related pipeline hangs\n"
        "- Replace fragile free-text parsing with strict JSON schema enforcement\n"
        "- Add self-observability so future iteration is data-driven"
    ),
))

# ---- AI-01 ----
items.append(row(
    summary="AI-01: Ollama call hardening — timeout, retry, circuit breaker, fallback",
    issue_type="Story", priority="Highest", story_points=3,
    parent=EPIC4_SUMMARY,
    labels="AI",
    description=(
        "As an SRE, I need the triage service's Ollama calls to be resilient to timeouts and "
        "failures so a slow or hung Ollama doesn't stall the pipeline.\n\n"
        "Acceptance Criteria:\n"
        "- Configurable per-request timeout (default 30s, override via env var)\n"
        "- Retry policy: up to 2 retries with exponential backoff on transient failures\n"
        "- Circuit breaker: after 5 consecutive failures, mark Ollama 'down' for 60s cooldown\n"
        "- Fallback: when circuit open or retries exhausted, produce 'NEEDS_HUMAN_REVIEW' verdict "
        "with raw alert context, sent via existing escalation email path\n"
        "- Metrics: ollama_request_duration_seconds, ollama_request_total{status}, ollama_circuit_state\n"
        "- Unit tests for timeout, retry, circuit breaker open/close transitions\n"
        "- Manual test: kill Ollama mid-request, verify pipeline produces fallback within timeout + retry budget"
    ),
))

# ---- AI-02 ----
items.append(row(
    summary="AI-02: JSON schema enforcement on LLM verdict — Ollama JSON mode + Pydantic validator",
    issue_type="Story", priority="Highest", story_points=2,
    parent=EPIC4_SUMMARY,
    labels="AI",
    description=(
        "As an SRE, I need the LLM verdict to be structured JSON validated against a strict schema "
        "so triage can reliably parse it without fragile string matching.\n\n"
        "Acceptance Criteria:\n"
        "- Ollama API call uses 'format: json' parameter (Ollama JSON mode)\n"
        "- System prompt instructs the model to return JSON matching a documented schema\n"
        "- Pydantic model for the verdict:\n"
        "  { verdict: 'ESCALATE'|'DISMISS'|'INCONCLUSIVE',\n"
        "    confidence: 0-1,\n"
        "    root_cause: str,\n"
        "    evidence: [str],\n"
        "    recommended_actions: [str],\n"
        "    alert_id: str }\n"
        "- Validator runs on every LLM response; on schema failure, retry once with the validation error appended\n"
        "- On second failure, escalate to NEEDS_HUMAN_REVIEW (uses fallback path from AI-01)\n"
        "- Existing free-text 'ESCALATE/DISMISS' parser removed\n"
        "- Unit tests for valid response, schema failure, retry recovery, double failure\n"
        "- Schema documented in monitoring-docs"
    ),
))

# ---- AI-03 ----
items.append(row(
    summary="AI-03: Triage service self-observability — /metrics with queue depth, latency, error rates",
    issue_type="Story", priority="High", story_points=3,
    parent=EPIC4_SUMMARY,
    labels="AI",
    description=(
        "As an SRE, I need the triage service to expose its own operational metrics so I can "
        "observe and improve its behavior.\n\n"
        "Acceptance Criteria:\n"
        "- Triage service exposes /metrics in Prometheus format\n"
        "- Metrics:\n"
        "  - triage_alerts_received_total{source}\n"
        "  - triage_alerts_processed_total{verdict}\n"
        "  - triage_decision_duration_seconds (histogram)\n"
        "  - triage_queue_depth (gauge)\n"
        "  - triage_mcp_request_total{server,status}\n"
        "  - triage_mcp_duration_seconds{server} (histogram)\n"
        "  - triage_llm_token_count{type='prompt'|'completion'} (histogram)\n"
        "  - triage_fallback_total{reason}\n"
        "  - triage_email_sent_total{status}\n"
        "- Prometheus annotations on the triage Service (prometheus.io/scrape, /port, /path)\n"
        "- New Grafana panel 'Triage Service Health' added to unified-overview:\n"
        "  - Decision throughput, latency p50/p95/p99, verdict breakdown, MCP error rates, fallback rate\n"
        "- Dashboard JSON committed to git\n"
        "- Verification: test alert produces visible metric updates within 30s"
    ),
))

# ============================================================================
# WRITE THE CSV
# ============================================================================
out_path = "Jira-additions.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADERS)
    for item in items:
        w.writerow(item)

print(f"Wrote {len(items)} rows to {out_path}")
print(f"  Columns: {len(HEADERS)} (was 56)")
print(f"  Epics: 2  Stories: {len(items) - 2}")
print(f"  Total story points: K8s={3+3+3+3+3+5+5+3+3+3+3} AI={3+2+3} -> {37+8} new points")
