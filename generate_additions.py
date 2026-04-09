#!/usr/bin/env python3
"""
Generate Jira-import-compatible CSV rows for the new sprint 2 additions:
- 2 new epics (Epic 3 K8s Migration, Epic 4 AI Triage Service Hardening)
- 11 K8s migration stories (E3-00 through E3-10)
- 3 AI hardening stories (AI-01, AI-02, AI-03)

Output: Jira-additions.csv (in this directory)
Header structure (column count and duplicates) matches the existing Jira.csv exactly.
"""

import csv

# --- Constants reused on every row ---
PROJECT_KEY = "SCRUM"
PROJECT_NAME = "Digital Factory Observability Service"
PROJECT_TYPE = "software"
PROJECT_LEAD = "Lina Laaraich"
PROJECT_LEAD_ID = "610c1cb7a539cb0068b06a40"
PROJECT_DESCRIPTION = "Your first project"
USER_NAME = "Lina Laaraich"
USER_ID = "610c1cb7a539cb0068b06a40"
TEAM_ID = "6f3a0d39-46e6-4fe8-bd10-eaff50217004"
TEAM_NAME = "Observability Interns"
SPRINT_NAME = "SCRUM Sprint 2"
TODAY = "09/Apr/26 12:00 PM"
SPRINT_DUE = "23/Apr/26 12:00 AM"
SPRINT_START = "25/Mar/26 12:00 AM"

# Header MUST match the existing Jira.csv exactly: 56 columns with Labels x4 and Sprint x2
HEADERS = [
    "Summary", "Issue key", "Issue id", "Issue Type", "Status",
    "Project key", "Project name", "Project type", "Project lead", "Project lead id",
    "Project description", "Priority", "Resolution", "Assignee", "Assignee Id",
    "Reporter", "Reporter Id", "Creator", "Creator Id", "Created", "Updated",
    "Last Viewed", "Resolved", "Due date", "Votes",
    "Labels", "Labels", "Labels", "Labels",
    "Description", "Environment", "Watchers", "Watchers Id",
    "Original estimate", "Remaining Estimate", "Time Spent", "Work Ratio",
    "Σ Original Estimate", "Σ Remaining Estimate", "Σ Time Spent",
    "Security Level", "Custom field (Development)", "Custom field (Issue color)",
    "Custom field (Rank)",
    "Sprint", "Sprint",
    "Custom field (Start date)", "Custom field (Story point estimate)",
    "Team Id", "Team Name", "Custom field (Vulnerability)",
    "Parent", "Parent key", "Parent summary",
    "Status Category", "Status Category Changed",
]

def make_row(*, summary, key, iid, issue_type, priority, description, labels=None,
             story_points=None, parent_iid=None, parent_key=None, parent_summary=None,
             due_date=SPRINT_DUE, color=None):
    """Build a 56-column row matching the Jira CSV format."""
    labels = (labels or []) + [""] * (4 - len(labels or []))  # pad to 4
    row = [
        summary,                          # Summary
        key,                              # Issue key
        str(iid),                         # Issue id
        issue_type,                       # Issue Type
        "To Do",                          # Status
        PROJECT_KEY,                      # Project key
        PROJECT_NAME,                     # Project name
        PROJECT_TYPE,                     # Project type
        PROJECT_LEAD,                     # Project lead
        PROJECT_LEAD_ID,                  # Project lead id
        PROJECT_DESCRIPTION,              # Project description
        priority,                         # Priority
        "",                               # Resolution
        USER_NAME if issue_type != "Epic" else "",  # Assignee
        USER_ID if issue_type != "Epic" else "",    # Assignee Id
        USER_NAME,                        # Reporter
        USER_ID,                          # Reporter Id
        USER_NAME,                        # Creator
        USER_ID,                          # Creator Id
        TODAY,                            # Created
        TODAY,                            # Updated
        TODAY,                            # Last Viewed
        "",                               # Resolved
        due_date,                         # Due date
        "0",                              # Votes
        labels[0], labels[1], labels[2], labels[3],  # Labels x4
        description,                      # Description
        "",                               # Environment
        USER_NAME,                        # Watchers
        USER_ID,                          # Watchers Id
        "",                               # Original estimate
        "",                               # Remaining Estimate
        "",                               # Time Spent
        "",                               # Work Ratio
        "",                               # Σ Original Estimate
        "",                               # Σ Remaining Estimate
        "",                               # Σ Time Spent
        "",                               # Security Level
        "",                               # Custom field (Development)
        color or "",                      # Custom field (Issue color)
        "",                               # Custom field (Rank)
        SPRINT_NAME,                      # Sprint
        "",                               # Sprint (second column, blank in source)
        SPRINT_START if issue_type == "Epic" else "",  # Custom field (Start date)
        str(story_points) if story_points else "",     # Story point estimate
        TEAM_ID,                          # Team Id
        TEAM_NAME,                        # Team Name
        "",                               # Custom field (Vulnerability)
        str(parent_iid) if parent_iid else "",  # Parent
        parent_key or "",                 # Parent key
        parent_summary or "",             # Parent summary
        "To Do",                          # Status Category
        TODAY,                            # Status Category Changed
    ]
    assert len(row) == len(HEADERS), f"row length {len(row)} != header length {len(HEADERS)}"
    return row


# ============================================================================
# DEFINE ALL 16 NEW ITEMS
# ============================================================================

EPIC3_KEY = "SCRUM-86"
EPIC3_IID = 10149
EPIC3_SUMMARY = "Epic 3 -- Kubernetes Migration of Monitored Target"

EPIC4_KEY = "SCRUM-98"
EPIC4_IID = 10161
EPIC4_SUMMARY = "Epic 4 -- AI Triage Service Hardening"

items = []

# ---- Epic 3 ----
items.append(make_row(
    summary=EPIC3_SUMMARY,
    key=EPIC3_KEY, iid=EPIC3_IID,
    issue_type="Epic", priority="High", color="dark_blue",
    labels=["Kubernetes"],
    description=(
        "Migrate the monitored infrastructure (Spring Boot, Kong, AI RCA pipeline, Ollama) "
        "from per-VM docker-compose to a single-node k3s cluster on EC2. The monitoring stack "
        "(Prometheus, Grafana, Loki, Jaeger) stays on its own VM and reaches into the cluster "
        "via kubernetes_sd_configs and an in-cluster OTel Collector DaemonSet. This validates "
        "the architectural shift to declarative, reproducible deployment with K8s as a portable "
        "substrate while preserving the existing observability platform.\n\n"
        "Goals:\n"
        "- Single-node k3s cluster on EC2 (HA deferred to sprint 3)\n"
        "- Three Helm charts: Spring Boot (in-house), Kong (upstream), AI stack (in-house)\n"
        "- Image registry pipeline (ECR + GitHub Actions)\n"
        "- Monitoring VM unchanged but reconfigured to scrape the cluster\n"
        "- All 17 Grafana alert rules migrated to K8s label selectors\n"
        "- End-to-end validation against the K8s target\n\n"
        "Out of scope (sprint 3+):\n"
        "- Multi-node HA / k3s embedded etcd\n"
        "- ArgoCD/GitOps adoption\n"
        "- Calico/Cilium for NetworkPolicy enforcement\n"
        "- Longhorn for distributed storage\n"
        "- OpenTelemetry Operator for auto-instrumentation\n"
        "- Migrating the monitoring stack itself to K8s (deliberately rejected)"
    ),
))

# ---- E3-00 ----
items.append(make_row(
    summary="E3-00: Team K8s onboarding — Phases 1-4 of the Kubernetes guide on k3d",
    key="SCRUM-87", iid=10150,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Onboarding"],
    description=(
        "As a developer working on the Kubernetes migration, I need hands-on familiarity "
        "with K8s primitives so that I can build Epic 3 stories without fighting conceptual "
        "misunderstandings.\n\n"
        "Acceptance Criteria:\n"
        "- Each contributor brings up a local k3d cluster: k3d cluster create learn --servers 1 --agents 2\n"
        "- Walks through Phase 1 of the Kubernetes guide (deploy nginx, port-forward, watch self-healing)\n"
        "- Walks through Phase 2 (ConfigMap, Secret, PVC, namespaces, Job, DaemonSet)\n"
        "- Walks through Phase 3 (DNS resolution, Service vs Pod IPs, NetworkPolicy)\n"
        "- Walks through Phase 4 (install kube-prometheus-stack via Helm, override values)\n"
        "- Completes a 30-min pair walkthrough with at least one teammate to demonstrate understanding\n"
        "- Reference: https://github.com/linalaaraich/monitoring-docs/blob/main/kubernetes-guide.html\n\n"
        "Story Points: 3\n"
        "Estimate: 1 day per contributor\n"
        "Epic: K8s Migration\n"
        "Blocks: ALL other E3 stories"
    ),
))

# ---- E3-01 ----
items.append(make_row(
    summary="E3-01: Bootstrap k3s on EC2 via Ansible — xanmanning.k3s, pinned, Traefik disabled",
    key="SCRUM-88", iid=10151,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Ansible"],
    description=(
        "As a platform engineer, I need a single-node k3s cluster running on EC2 so that "
        "the Helm-deployed workloads have somewhere to run.\n\n"
        "Acceptance Criteria:\n"
        "- xanmanning.k3s role added to requirements.yml, version v3.4.4 pinned\n"
        "- New playbook playbooks/k3s.yml bootstraps k3s on a single host\n"
        "- k3s_release_version pinned to a specific v1.30.x+k3s1 release\n"
        "- Traefik disabled via k3s_server.disable: [traefik] (we use Kong)\n"
        "- write-kubeconfig-mode: '0644' so kubeconfig is fetchable\n"
        "- kubeconfig fetched back to control machine at artifacts/kubeconfig.yaml\n"
        "- Server URL in fetched kubeconfig rewritten from 127.0.0.1 to the EC2 host IP\n"
        "- New inventory group k3s_cluster wired into site.yml\n"
        "- Verification: kubectl --kubeconfig=artifacts/kubeconfig.yaml get nodes returns 1 Ready node\n"
        "- README updated with the new bootstrap step\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-03, E3-04, E3-05, E3-06, E3-07, E3-08, E3-09, E3-10\n"
        "Blocked by: E3-00, SCRUM-63 (rescoped Terraform)"
    ),
))

# ---- E3-02 ----
items.append(make_row(
    summary="E3-02: Image build + k3s containerd import via Ansible (no registry, no CI)",
    key="SCRUM-89", iid=10152,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Ansible", "Images"],
    description=(
        "As a platform engineer, I need first-party container images (triage service + 5 MCP "
        "servers) loaded into the k3s host's containerd cache so that Helm-deployed pods can "
        "run them without a registry.\n\n"
        "Why no registry/CI: this is a single-node k3s cluster with one or two contributors. "
        "ECR + GitHub Actions adds operational surface area we don't need at this scale. "
        "k3s's containerd lets us import images directly from a tarball, which is enough.\n\n"
        "Acceptance Criteria:\n"
        "- Dockerfiles for triage service and 5 MCP servers exist (extracted from current docker-compose builds)\n"
        "- New Ansible role/tasks that, for each image:\n"
        "  1. docker build -t cires/<name>:<tag> <context>\n"
        "  2. docker save cires/<name>:<tag> -o /tmp/<name>.tar\n"
        "  3. ssh to k3s host (or run locally if same host) and: sudo k3s ctr images import /tmp/<name>.tar\n"
        "- Image tag pinned via a single image_tag variable in group_vars (e.g. '1.0.0' or git short-sha)\n"
        "- All Helm charts reference cires/<name>:<image_tag> with imagePullPolicy: IfNotPresent\n"
        "- Verification: sudo k3s crictl images on the host shows all 6 cires/* images present\n"
        "- Verification: helm install of the AI stack chart succeeds without ImagePullBackOff\n"
        "- Documentation: README explains the build+import flow and the upgrade path to ECR+CI when multi-node is needed\n\n"
        "Defensible scope decision: registry+CI is the right answer at multi-node scale or with many contributors. "
        "We can swap to ECR with a one-line Helm values change when that's needed. Sprint 2 doesn't need it.\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-05 (AI stack chart can't run without images loaded)\n"
        "Blocked by: E3-00, E3-01"
    ),
))

# ---- E3-03 ----
items.append(make_row(
    summary="E3-03: Helm chart — Spring Boot backend (Deployment + Service + ConfigMap + probes)",
    key="SCRUM-90", iid=10153,
    issue_type="Story", priority="High", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Helm"],
    description=(
        "As a developer, I need a Helm chart that deploys the Spring Boot backend into the "
        "k3s cluster so that the application is reachable from Kong and can talk to RDS.\n\n"
        "Acceptance Criteria:\n"
        "- New chart at charts/spring-boot/ with Chart.yaml, values.yaml, templates/\n"
        "- Deployment template with: 1+ replicas (configurable), resource requests + limits, "
        "liveness probe (/actuator/health/liveness), readiness probe (/actuator/health/readiness)\n"
        "- Service template (ClusterIP, port 80 -> targetPort 8080)\n"
        "- ConfigMap for Spring application properties (profile, log levels, etc.)\n"
        "- Secret reference for RDS credentials (DB_USERNAME, DB_PASSWORD, DB_URL)\n"
        "- ServiceAccount for the pod\n"
        "- Image references pinned by tag (no :latest)\n"
        "- values.yaml documents every override\n"
        "- Installable via helm install spring-boot charts/spring-boot/ --namespace app --create-namespace -f values/spring-boot.yaml\n"
        "- Pod reaches RDS successfully (verified via /actuator/health endpoint)\n"
        "- Spring Boot logs include trace_id (OTel Java agent injected via init container or baked into image)\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01"
    ),
))

# ---- E3-04 ----
items.append(make_row(
    summary="E3-04: Helm chart — Kong via upstream chart, DB-less mode, kong.yml as ConfigMap",
    key="SCRUM-91", iid=10154,
    issue_type="Story", priority="High", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Helm", "Kong"],
    description=(
        "As a platform engineer, I need Kong running inside the cluster as the API gateway "
        "so that external traffic reaches the Spring Boot backend through the existing "
        "declarative routing config.\n\n"
        "Acceptance Criteria:\n"
        "- Upstream kong/kong Helm chart used, chart_version pinned (e.g. 2.38.0)\n"
        "- DB-less mode enabled\n"
        "- Existing kong.yml declarative config converted to a ConfigMap mounted into the Kong pod\n"
        "- Upstream URLs in kong.yml rewritten from application_vm_ip:8080 to spring-boot.app.svc.cluster.local:80\n"
        "- React frontend route still points to CloudFront (unchanged)\n"
        "- OTel plugin enabled, sends spans to in-cluster OTel Collector via OTLP\n"
        "- Prometheus plugin enabled, /metrics endpoint scraped by Prometheus K8s SD\n"
        "- Service exposed externally via NodePort or LoadBalancer (decision documented)\n"
        "- Verification: curl through Kong reaches Spring Boot, traces appear in Jaeger\n"
        "- Decision documented: which Service type for Kong's external port and why\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, E3-03"
    ),
))

# ---- E3-05 ----
items.append(make_row(
    summary="E3-05: Helm chart — AI stack (triage service + 5 MCP servers + Ollama)",
    key="SCRUM-92", iid=10155,
    issue_type="Story", priority="High", story_points=5,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Helm", "AI"],
    description=(
        "As an SRE, I need the entire AI RCA pipeline deployed via a single Helm chart so that "
        "triage, MCP servers, and Ollama have a consistent lifecycle and can roll back together.\n\n"
        "Acceptance Criteria:\n"
        "- New chart at charts/ai-stack/ containing:\n"
        "  - Triage service Deployment + Service (port 8090)\n"
        "  - 5x MCP server Deployments + Services (Prometheus :8091, Loki :8092, Jaeger :8093, Drain3 :8094, RCA History :8095)\n"
        "  - Ollama Deployment with PVC for model storage (20Gi minimum, local-path StorageClass)\n"
        "  - GPU resource request on Ollama pod: resources.limits.nvidia.com/gpu: 1\n"
        "  - Init Job or postStart hook that pulls the Ollama model on first deploy\n"
        "  - Secret for SMTP credentials and Ollama config\n"
        "  - All inter-service references use Service DNS (no localhost, no hardcoded IPs)\n"
        "- All image references pinned to ECR tags from E3-02\n"
        "- Resource requests + limits set per container\n"
        "- Liveness + readiness probes per container\n"
        "- Installable via helm install ai-stack charts/ai-stack/ --namespace ai --create-namespace -f values/ai-stack.yaml\n"
        "- Verification: triage /health responds, MCP servers respond, Ollama returns model list\n\n"
        "Story Points: 5\n"
        "Estimate: 1 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, E3-02, E3-06"
    ),
))

# ---- E3-06 ----
items.append(make_row(
    summary="E3-06: NVIDIA device plugin DaemonSet + Ollama GPU verification spike",
    key="SCRUM-93", iid=10156,
    issue_type="Story", priority="Highest", story_points=5,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "GPU", "Spike"],
    description=(
        "As a platform engineer, I need to verify that GPU passthrough works on k3s so that "
        "Ollama can leverage the GPU for inference. This is a spike — plan for fiddly debugging.\n\n"
        "Acceptance Criteria:\n"
        "- NVIDIA Container Toolkit installed on the k3s host (via Ansible role nvidia_docker, repurposed)\n"
        "- containerd configured to recognize the nvidia runtime (k3s --default-runtime=nvidia or RuntimeClass)\n"
        "- NVIDIA device plugin DaemonSet deployed (nvidia/k8s-device-plugin v0.15.0 manifest)\n"
        "- Test pod requesting nvidia.com/gpu: 1 runs successfully and nvidia-smi output is visible\n"
        "- Troubleshooting guide added to monitoring-docs covering common failures (driver mismatch, runtime not configured, plugin pod CrashLoopBackOff)\n"
        "- Decision documented: GPU on the same EC2 as everything else, or separate g4dn.xlarge worker node\n"
        "- If a separate GPU node is chosen: node tainted, Ollama pod has matching toleration\n\n"
        "Story Points: 5\n"
        "Estimate: 1 day (spike, may extend to 1.5)\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-05 (Ollama in AI stack chart cannot run without this)\n"
        "Blocked by: E3-01"
    ),
))

# ---- E3-07 ----
items.append(make_row(
    summary="E3-07: In-cluster OTel Collector DaemonSet — log/trace forwarding to monitoring VM",
    key="SCRUM-94", iid=10157,
    issue_type="Story", priority="High", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Observability", "OpenTelemetry"],
    description=(
        "As an observability engineer, I need an OTel Collector running on every K8s node so "
        "that container logs and traces are enriched with K8s metadata and forwarded to the "
        "existing monitoring VM.\n\n"
        "Acceptance Criteria:\n"
        "- New manifest set or Helm chart deploys:\n"
        "  - Namespace observability\n"
        "  - ServiceAccount + ClusterRole granting access to nodes/pods/namespaces (for k8sattributes processor)\n"
        "  - DaemonSet running otel/opentelemetry-collector-contrib (version pinned)\n"
        "  - ConfigMap with collector config:\n"
        "    * filelog receiver tailing /var/log/pods/*/*/*.log\n"
        "    * k8sattributes processor enriching with pod, namespace, container, trace_id\n"
        "    * OTLP receiver on :4317 (gRPC) and :4318 (HTTP) for in-cluster traces\n"
        "    * OTLP exporter pushing to monitoring_vm_ip:4317\n"
        "- Three per-VM OTel Collector containers retired (otel-collector references in compose templates removed)\n"
        "- Verification: a Spring Boot log line appears in Loki on the monitoring VM with the correct pod/namespace/trace_id labels\n"
        "- Verification: a trace from Spring Boot or Kong appears in Jaeger on the monitoring VM\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-10\n"
        "Blocked by: E3-01, E3-03, E3-04, E3-05"
    ),
))

# ---- E3-08 ----
items.append(make_row(
    summary="E3-08: Prometheus kubernetes_sd_configs scrape job + RBAC for monitoring VM",
    key="SCRUM-95", iid=10158,
    issue_type="Story", priority="High", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Prometheus", "RBAC"],
    description=(
        "As an observability engineer, I need the existing external Prometheus to discover "
        "and scrape K8s-hosted services so that all metrics keep flowing to the same datastore.\n\n"
        "Acceptance Criteria:\n"
        "- New ServiceAccount prometheus-scraper in namespace observability\n"
        "- ClusterRole granting get/list/watch on nodes, pods, services, endpoints + nonResourceURLs /metrics\n"
        "- ClusterRoleBinding to the SA\n"
        "- SA token extracted, stored as Ansible vault secret on the monitoring VM at /etc/prometheus/k8s-token\n"
        "- Prometheus role updated with new scrape job using kubernetes_sd_configs:\n"
        "  - role: pod (with annotation-based filtering)\n"
        "  - api_server pointing at the k3s host's :6443\n"
        "  - bearer_token_file pointing to the new secret\n"
        "  - tls_config insecure_skip_verify true (sprint 2; proper CA in sprint 3)\n"
        "  - Relabel rules: keep only pods with annotation prometheus.io/scrape: 'true', use prometheus.io/port for port\n"
        "- Security group on k3s EC2 allows monitoring VM IP on :6443 and :10250\n"
        "- Verification: Prometheus scrape_targets page on the monitoring VM shows healthy K8s targets\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-09, E3-10\n"
        "Blocked by: E3-01, SCRUM-63 (security group update)"
    ),
))

# ---- E3-09 ----
items.append(make_row(
    summary="E3-09: Migrate the 17 Grafana alert rules to K8s pod-based label selectors",
    key="SCRUM-96", iid=10159,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Alerting", "Grafana"],
    description=(
        "As an SRE, I need every Grafana alert rule's selector updated to match the new "
        "K8s-hosted target so that alerts continue to fire correctly after migration. "
        "This is high-risk: silent failure if missed.\n\n"
        "Acceptance Criteria:\n"
        "- Audit current Grafana alerting configuration: 17 rules in 3 groups (per CLAUDE.md)\n"
        "- For each rule, rewrite the label selector:\n"
        "  - Old: instance='application_vm_ip:8080' -> New: pod=~'spring-boot.*', namespace='app'\n"
        "  - Old: instance='network_vm_ip:8000'     -> New: pod=~'kong.*',        namespace='network'\n"
        "  - Old: instance='ai_vm_ip:8090'           -> New: pod=~'triage.*',      namespace='ai'\n"
        "- Updated rules committed to git and applied via Grafana provisioning\n"
        "- Each rule manually triggered (stop a pod, generate latency, etc.) and verified to fire\n"
        "- Rule firing test results documented in a checklist\n"
        "- Triage service receives the test webhook for each rule\n"
        "- No rule is left with a stale selector\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocks: E3-10\n"
        "Blocked by: E3-03, E3-04, E3-05, E3-08"
    ),
))

# ---- E3-10 ----
items.append(make_row(
    summary="E3-10: End-to-end K8s validation playbook — full pipeline against K8s target",
    key="SCRUM-97", iid=10160,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC3_IID, parent_key=EPIC3_KEY, parent_summary=EPIC3_SUMMARY,
    labels=["Kubernetes", "Integration"],
    description=(
        "As an SRE, I need an automated end-to-end test that validates the full pipeline "
        "against the K8s-hosted target so that the migration is provably complete.\n\n"
        "Acceptance Criteria:\n"
        "- New playbook playbooks/integration-k8s.yml (or update existing integration.yml)\n"
        "- Test sequence:\n"
        "  1. Run load-test.sh against Kong's external endpoint\n"
        "  2. Verify Spring Boot pod metrics in Prometheus (RED metrics)\n"
        "  3. Verify Spring Boot logs in Loki, with trace_id label\n"
        "  4. Verify trace in Jaeger end-to-end (Kong -> Spring -> RDS)\n"
        "  5. Trigger an alert (e.g. high latency)\n"
        "  6. Verify Grafana alert rule fires\n"
        "  7. Verify webhook arrives at triage service\n"
        "  8. Verify triage service produces a verdict\n"
        "  9. Verify LLM analysis runs and returns RCA JSON\n"
        "  10. Verify escalation email is sent (or DISMISS logged)\n"
        "- All checks scripted, exit code 0 = pass\n"
        "- Runbook documented in monitoring-docs for manual reproduction\n"
        "- Coordinates with SCRUM-66 (E1-05) — that story is closed in favor of this one\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: K8s Migration\n"
        "Blocked by: E3-03, E3-04, E3-05, E3-06, E3-07, E3-08, E3-09"
    ),
))

# ---- Epic 4 ----
items.append(make_row(
    summary=EPIC4_SUMMARY,
    key=EPIC4_KEY, iid=EPIC4_IID,
    issue_type="Epic", priority="Medium", color="dark_purple",
    labels=["AI", "Reliability"],
    description=(
        "Targeted reliability and observability improvements to the AI triage pipeline "
        "beyond the MVP. Scope is deliberately narrow: three high-leverage stories covering "
        "the most impactful weaknesses identified after Epic 2 (the MVP). Larger AI maturity "
        "work (calibration sets, prompt engineering, model A/B testing) is deferred.\n\n"
        "Goals:\n"
        "- Eliminate Ollama-related pipeline hangs (the single biggest reliability issue)\n"
        "- Replace fragile free-text parsing with strict JSON schema enforcement\n"
        "- Add self-observability so future iteration is data-driven\n\n"
        "Out of scope (future sprint):\n"
        "- Prompt template versioning + iteration loop\n"
        "- Calibration set + regression testing for prompts\n"
        "- Model A/B testing across Ollama variants\n"
        "- Persistent decision history with database backend\n"
        "- Few-shot prompting / chain-of-thought\n"
        "- Per-alert-class prompt variants"
    ),
))

# ---- AI-01 ----
items.append(make_row(
    summary="AI-01: Ollama call hardening — timeout, retry, circuit breaker, fallback",
    key="SCRUM-99", iid=10162,
    issue_type="Story", priority="Highest", story_points=3,
    parent_iid=EPIC4_IID, parent_key=EPIC4_KEY, parent_summary=EPIC4_SUMMARY,
    labels=["AI", "Reliability"],
    description=(
        "As an SRE, I need the triage service's Ollama calls to be resilient to timeouts and "
        "failures so that a slow or hung Ollama doesn't stall the entire pipeline.\n\n"
        "Acceptance Criteria:\n"
        "- Configurable per-request timeout on Ollama calls (default 30s, override via env var)\n"
        "- Retry policy: up to 2 retries with exponential backoff on transient failures (network, 5xx)\n"
        "- Circuit breaker: after N consecutive failures (default 5) within a window, mark Ollama as 'down' "
        "and skip calls for a cooldown period (default 60s)\n"
        "- Fallback path: when circuit is open or all retries exhausted, the triage service produces a "
        "'NEEDS_HUMAN_REVIEW' verdict with the raw alert context, sent via the existing escalation email path\n"
        "- Metrics exposed: ollama_request_duration_seconds, ollama_request_total{status}, ollama_circuit_state\n"
        "- Unit tests for timeout, retry, circuit breaker open/close transitions\n"
        "- Manual test: kill Ollama mid-request, verify pipeline produces fallback verdict within timeout + retry budget\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: AI Triage Service Hardening"
    ),
))

# ---- AI-02 ----
items.append(make_row(
    summary="AI-02: JSON schema enforcement on LLM verdict — Ollama JSON mode + Pydantic validator",
    key="SCRUM-100", iid=10163,
    issue_type="Story", priority="Highest", story_points=2,
    parent_iid=EPIC4_IID, parent_key=EPIC4_KEY, parent_summary=EPIC4_SUMMARY,
    labels=["AI", "LLM", "Reliability"],
    description=(
        "As an SRE, I need the LLM verdict to be structured JSON validated against a strict schema "
        "so that the triage service can reliably parse it without fragile string matching.\n\n"
        "Acceptance Criteria:\n"
        "- Ollama API call uses 'format: json' parameter (Ollama JSON mode)\n"
        "- System prompt instructs the model to return JSON matching a documented schema\n"
        "- Pydantic model defined for the verdict:\n"
        "  { verdict: 'ESCALATE'|'DISMISS'|'INCONCLUSIVE',\n"
        "    confidence: 0-1,\n"
        "    root_cause: str,\n"
        "    evidence: [str],\n"
        "    recommended_actions: [str],\n"
        "    alert_id: str }\n"
        "- Validator runs on every LLM response; on schema failure, retry once with the validation error appended to the prompt\n"
        "- On second failure, escalate to NEEDS_HUMAN_REVIEW (uses fallback path from AI-01)\n"
        "- Existing free-text 'ESCALATE/DISMISS' parser removed\n"
        "- Unit tests for valid response, schema failure, retry recovery, double failure\n"
        "- Schema documented in monitoring-docs\n\n"
        "Story Points: 2\n"
        "Estimate: 0.5 day\n"
        "Epic: AI Triage Service Hardening"
    ),
))

# ---- AI-03 ----
items.append(make_row(
    summary="AI-03: Triage service self-observability — /metrics with queue depth, latency, error rates",
    key="SCRUM-101", iid=10164,
    issue_type="Story", priority="High", story_points=3,
    parent_iid=EPIC4_IID, parent_key=EPIC4_KEY, parent_summary=EPIC4_SUMMARY,
    labels=["AI", "Observability", "Metrics"],
    description=(
        "As an SRE, I need the triage service to expose its own operational metrics so that I can "
        "observe and improve its behavior the same way I observe everything else in the platform.\n\n"
        "Acceptance Criteria:\n"
        "- Triage service exposes /metrics endpoint in Prometheus format\n"
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
        "- Prometheus scrape annotation set on the triage Service (prometheus.io/scrape='true', "
        "prometheus.io/port='8090', prometheus.io/path='/metrics')\n"
        "- New Grafana dashboard panel 'Triage Service Health' added to unified-overview:\n"
        "  - Decision throughput (alerts/min)\n"
        "  - Decision latency p50/p95/p99\n"
        "  - Verdict breakdown pie chart\n"
        "  - MCP error rates by server\n"
        "  - Fallback rate trend\n"
        "- Dashboard JSON committed to git\n"
        "- Verification: triggering a test alert produces visible metric updates within 30s\n\n"
        "Story Points: 3\n"
        "Estimate: 0.5 day\n"
        "Epic: AI Triage Service Hardening"
    ),
))

# ============================================================================
# WRITE THE CSV
# ============================================================================
out_path = "Jira-additions.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADERS)
    for row in items:
        w.writerow(row)

print(f"Wrote {len(items)} rows to {out_path}")
print(f"  Epics: 2 (Epic 3 K8s Migration, Epic 4 AI Hardening)")
print(f"  K8s stories: 11 (E3-00 through E3-10)")
print(f"  AI stories:  3 (AI-01, AI-02, AI-03)")
print(f"Total story points: K8s={3+3+3+3+3+5+5+3+3+3+3} AI={3+2+3} -> {37+8} new points")
