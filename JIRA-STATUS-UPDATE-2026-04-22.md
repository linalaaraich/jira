# Jira housekeeping — 2026-04-22

Paste-ready edits to bring the SCRUM board in line with code reality. Based on a full audit of `origin/main` across all 6 repos on **2026-04-22**. After this pass, Jira statuses should match what is actually committed, which unblocks an accurate sprint review.

Work to do, in order:

1. [Close 2 tickets as superseded](#1-close-as-superseded)
2. [Rescope 3 tickets in place](#2-rescope-in-place)
3. [Status bumps — 12 stories are code-complete on `origin/main`](#3-status-bumps)

---

## 1. Close as superseded

Do these first. In Jira: open each ticket → **Resolve** → select **Won't Do** → paste the comment below before saving.

### SCRUM-66 — E1-05: End-to-end cloud validation

**Resolution:** Won't Do — Superseded

**Comment:**

> Superseded by **SCRUM-128** (E3-10: End-to-end K8s validation playbook). The original VM-target validation is no longer the ground truth — the K8s-target validation is. The code for the replacement test lives at `playbooks/integration-k8s.yml` on `monitoring-project/main` and covers the same 10 steps (load-test → metrics → logs → traces → alert → webhook → triage → LLM → email) plus a k3s cluster-health pre-check. Closing this and consolidating into E3-10.

### SCRUM-82 — E2-11: Docker-compose for AI stack

**Resolution:** Won't Do — Superseded

**Comment:**

> Superseded by **SCRUM-123** (E3-05: Helm chart — AI stack). The K8s migration replaces the docker-compose template with a Helm chart at `charts/ai-stack/` on `monitoring-project/main` (13 templates: triage service, 5 MCP servers, Ollama with PVC + GPU resource). Closing this and consolidating into E3-05.

---

## 2. Rescope in place

Don't close these — edit Summary, Description, and Points. Full description text is in [`SPRINT2-EXTENSION-README.md`](SPRINT2-EXTENSION-README.md) in this repo; shortened summaries below.

| Ticket | New summary | Pts (old → new) |
|---|---|---|
| **SCRUM-63** | *E1-02: Terraform — VPC, 1 k3s EC2, RDS, S3+CloudFront* | 8 → **5** |
| **SCRUM-64** | *E1-03: Ansible deploy to AWS — monitoring VM only (Spring/Kong/AI move to K8s in Epic 3)* | 5 → **3** |
| **SCRUM-65** | *E1-04: NVIDIA driver install on GPU host (k3s runtime piece moved to E3-06)* | 5 → **2** |

For each, paste the corresponding full description block from `SPRINT2-EXTENSION-README.md` into the Jira description field, then bump the Story Point field to the new value.

### Ready-to-paste rescope comment (one for all 3)

> Rescoped per Sprint 2 extension plan (see monitoring-docs/sprint2-extension-guide.html). Original scope referenced the 4-VM docker-compose deployment; the extended Sprint 2 migrates Spring Boot / Kong / AI stack to k3s via Helm charts (Epic 3), leaving only the monitoring stack on a dedicated VM. Code reality on origin/main already reflects the rescope — this is a Jira cleanup, not new work.

---

## 3. Status bumps

All of the following are **code-complete on `origin/main`** as of 2026-04-22 but still show stale statuses in Jira. Update each to match.

### Move to Done

For each ticket: click **In Progress → Review → Done**, optionally with the paste comment below.

| Ticket | ID | Story | Current | Evidence on origin/main |
|---|---|---|---|---|
| SCRUM-67 | E2-01 | Grafana Alerting webhook (remove Alertmanager) | In Progress | `roles/grafana/templates/contactpoints.yml.j2` + `policies.yml.j2` + `alertrules.yml.j2` present; `alertmanager` role removed |
| SCRUM-72 | E2-13 | Drain3 setup | To Do | `monitoring-triage-service/app/drain_analyzer.py` fully implemented |
| SCRUM-73 | E2-14 | Drain3 + Loki integration | To Do | `drain_analyzer.py::annotate_logs` + pipeline integration |
| SCRUM-74 | E2-15 | Drain3 observability + MCP | To Do | `monitoring-mcp-servers/drain3_mcp/` + `/drain3/stats` endpoint |
| SCRUM-75 | E2-04 | FastAPI scaffold | In Review | `app/main.py` with 7 endpoints, BackgroundTasks |
| SCRUM-76 | E2-05 | Alert deduplication | In Review | `app/dedup.py` + `tests/test_dedup.py` (passing) |
| SCRUM-77 | E2-06 | Parallel context fan-out | In Progress | `app/context.py` with `asyncio.gather` + 8s timeout |
| SCRUM-78 | E2-07 | LLM prompt + parser | In Progress | `app/llm_client.py` with schema enforcement, INCONCLUSIVE support |
| SCRUM-79 | E2-08 | ESCALATE email via SMTP | In Progress | `app/notifier.py` with HTML email, aiosmtplib |
| SCRUM-80 | E2-09 | 5-min timeout fallback | In Progress | `app/pipeline.py` timeout handling + passthrough |
| SCRUM-81 | E2-10 | Decision history + RCA MCP + dashboard | To Do | `app/rca_store.py` + `rca_history_mcp/` + `/decisions` endpoint + `/dashboard` HTML |
| SCRUM-129 | AI-01 | Ollama call hardening | To Do | `app/circuit_breaker.py` + `ollama_circuit_state` metric + `NEEDS_HUMAN_REVIEW` fallback |
| SCRUM-130 | AI-02 | JSON schema enforcement | To Do | `"format": "json"` in Ollama call + `Decision.INCONCLUSIVE` + Pydantic validator with retry |

**Ready-to-paste comment for the bulk move:**

> Code-complete on `origin/main` as of 2026-04-22 (audited against the acceptance criteria). Moving to Done. If any detail needs verification it can be demoed from the deployed stack once the AWS new-account restrictions are lifted (Support Cases in flight as of 2026-04-21).

### Move to In Review

| Ticket | ID | Story | Current | Why In Review not Done |
|---|---|---|---|---|
| SCRUM-119 | E3-01 | Bootstrap k3s on EC2 via Ansible | To Do | Code complete (`playbooks/k3s.yml`, `xanmanning.k3s v3.4.4`, pinned `v1.30.6+k3s1`); awaits live deployment to verify `kubectl get nodes` returns Ready |
| SCRUM-120 | E3-02 | Image build + containerd import | To Do | `roles/k3s_images/` complete; needs live verification via `k3s crictl images` |
| SCRUM-121 | E3-03 | Helm chart — Spring Boot | To Do | `charts/spring-boot/` complete; needs `helm install` + `/actuator/health` verify |
| SCRUM-122 | E3-04 | Helm chart — Kong | To Do | `charts/kong/` complete; needs `helm install` + upstream routing verify |
| SCRUM-123 | E3-05 | Helm chart — AI stack | To Do | `charts/ai-stack/` complete; needs `helm install` + all 7 pods ready |
| SCRUM-124 | E3-06 | NVIDIA device plugin | To Do | `manifests/nvidia-device-plugin/daemonset.yaml` + `nvidia_docker` role; SPIKE — GPU passthrough still to validate on real hardware |
| SCRUM-125 | E3-07 | OTel Collector DaemonSet | To Do | `manifests/otel-collector/daemonset.yaml` complete; needs live log/trace forwarding verify |
| SCRUM-126 | E3-08 | Prometheus k8s_sd_configs + RBAC | To Do | `kubernetes-pods/nodes/cadvisor` scrape jobs present; needs SA token extraction + `/targets` verify |
| SCRUM-127 | E3-09 | Migrate 17 alert rules to K8s selectors | To Do | `roles/grafana/templates/alertrules.yml.j2` committed; each rule still needs individual trigger-and-verify (silent-failure risk) |
| SCRUM-128 | E3-10 | End-to-end K8s validation | To Do | `playbooks/integration-k8s.yml` (11 steps) committed; needs a green run against live stack |
| SCRUM-131 | AI-03 | Triage self-observability `/metrics` | To Do | `triage_llm_token_count`, `triage_email_sent_total`, `triage_queue_depth`, `triage_mcp_*` all present in `metrics.py`; dashboard JSON committed to `roles/grafana/files/dashboards/triage-service-health.json`; needs live scrape to confirm panels populate |

**Ready-to-paste comment for E3-*:**

> Code complete on `origin/main` (audited 2026-04-22). All E3 stories have their respective Helm charts / Ansible roles / K8s manifests merged. Moving to In Review; will flip to Done once the integration-k8s.yml playbook runs green against a live AWS stack (blocked on AWS Support Cases for new-account restrictions, filed 2026-04-21).

### Move to In Progress

| Ticket | ID | Story | Current | Reason |
|---|---|---|---|---|
| SCRUM-83 | E2-12 | E2E integration test | To Do | `integration.yml` committed; blocked on live AWS deployment before it can be run |

---

## Quick checklist

- [ ] SCRUM-66 closed as Superseded with comment
- [ ] SCRUM-82 closed as Superseded with comment
- [ ] SCRUM-63 summary + description + 5 pts
- [ ] SCRUM-64 summary + description + 3 pts
- [ ] SCRUM-65 summary + description + 2 pts
- [ ] 13 stories moved to Done (one bulk comment)
- [ ] 11 E3 / AI-03 stories moved to In Review (one bulk comment)
- [ ] SCRUM-83 moved to In Progress
- [ ] Sprint 2 due date verified as 23/Apr/26 on new epic items (SCRUM-117, SCRUM-118)

After this, the sprint board accurately reflects what ships vs. what's pending deployment verification.
