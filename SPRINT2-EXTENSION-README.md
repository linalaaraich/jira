# Sprint 2 Extension — Manual Steps

This README accompanies `Jira-additions.csv` and covers the changes that **cannot be done via CSV import** (modifications to existing tickets, supersessions, and Sprint metadata updates).

## TL;DR

1. **Import** `Jira-additions.csv` into the SCRUM project (15 new items: 2 epics + 13 stories)
2. **Modify** 4 existing tickets in place (rescope, don't close)
3. **Close** 1 existing ticket as superseded
4. **Verify** Sprint 2 due date and capacity after the changes

> **Note:** Team K8s onboarding (working through Phases 1-4 of the Kubernetes guide on a k3d cluster) is communicated verbally to the team — not tracked as a story. Reference: <https://github.com/linalaaraich/monitoring-docs/blob/main/kubernetes-guide.html>

---

## Step 1 — Import the new CSV

The CSV contains 15 items in 12 clean columns. All items go into `SCRUM Sprint 2` with status `To Do`.

| Type | Count |
|---|---|
| Epic | 2 (Epic 3 K8s Migration, Epic 4 AI Hardening) |
| Story | 13 (E3-01 → E3-10, AI-01 → AI-03) |

**The 12 columns:**
`Summary`, `Issue Type`, `Status`, `Priority`, `Labels`, `Description`, `Sprint`, `Story Points`, `Parent`, `Reporter`, `Assignee`, `Due date`

**Jira import path:**
1. Project Settings → System → External system import → CSV
2. Upload `Jira-additions.csv`
3. Select the SCRUM project as the target
4. Field mapping: each of the 12 columns maps directly to its Jira field of the same name. The only one Jira may not auto-detect is `Story Points` — map it to `Custom field (Story point estimate)`. The `Parent` column contains the epic's Summary, which Jira should resolve automatically.
5. Run the dry-run preview, confirm 15 items, commit.

**If parent links don't resolve on import** (some Jira versions need the epics to exist first):
- Filter the CSV to just the 2 Epic rows, import those first
- Then import the 14 Story rows — Jira will find the epics by Summary and link them

---

## Step 2 — Modify these 4 existing tickets in place

These tickets are still in Sprint 2 and **stay open**, but their scope changes due to the K8s migration. Edit them in the Jira UI; do **not** close them.

### SCRUM-63 — `E1-02: Terraform — VPC, 3+1 EC2s, RDS, S3+CloudFront`

**Current status:** In Review

**Change Summary to:**
> E1-02: Terraform — VPC, 1 k3s EC2, RDS, S3+CloudFront

**Replace Description with:**
```
As a platform engineer, I provision the AWS infrastructure for the K8s-hosted target so
that the cluster, database, and frontend hosting are all version-controlled.

Acceptance Criteria:
- VPC with public + private subnets, one AZ minimum
- Security groups:
  - k3s host: ingress :80, :443, :6443 (from monitoring VM), :10250 (from monitoring VM); egress to RDS :3306
  - Monitoring VM: ingress :3000, :9090, :3100, :16686 (admin sources only); egress to k3s :6443, :10250
  - RDS: ingress :3306 from k3s host SG only
- ONE EC2 instance for k3s (instance type sized for Spring + Kong + AI stack + Ollama; if Ollama needs separate GPU,
  add a second GPU instance and document the decision in SCRUM-93)
- AMI ID pinned (no most_recent = true)
- RDS instance unchanged from prior scope
- S3 bucket + CloudFront distribution unchanged
- Terraform providers pinned in providers.tf
- terraform.lock.hcl committed
- Outputs: k3s_host_ip, rds_endpoint, cloudfront_domain

Story Points: 5 (was lower; bump for the rework)
Estimate: 1 day
Epic: AWS Infrastructure
Blocks: SCRUM-88 (E3-01 k3s bootstrap), SCRUM-95 (E3-08 Prometheus K8s SD)
Note: Original "3+1 EC2s" scope is replaced by K8s migration. This story is rescoped, not closed.
Note: ECR is NOT included — first-party images are built locally and imported into k3s containerd
(see SCRUM-89/E3-02). Adding ECR is a future optimization when going multi-node.
```

**Bump Story Points** from current value to **5**.

---

### SCRUM-64 — `E1-03: Ansible deploy to AWS — Spring Boot, React, Kong, observability stack`

**Current status:** In Review

**Change Summary to:**
> E1-03: Ansible deploy to AWS — monitoring VM only (Spring/Kong/AI move to K8s in Epic 3)

**Replace Description with:**
```
As a platform engineer, I deploy the monitoring VM to AWS via Ansible so that the
observability stack (Prometheus, Grafana, Loki, Jaeger, OTel Collector) is running and ready
to scrape the K8s cluster.

Acceptance Criteria:
- playbooks/monitoring.yml deploys the monitoring VM stack:
  - Prometheus, Grafana, Loki, Jaeger, OTel Collector, node_exporter, cAdvisor
- Existing roles unchanged: prometheus, loki, jaeger, grafana, otel-collector
- Grafana provisioning (datasources, dashboards) committed and applied
- Verification: Grafana UI reachable, all datasources show "Connected"
- Spring Boot, React, Kong, AI stack deployment is OUT OF SCOPE here — moves to E3-03/04/05
  (Helm charts) and E3-01 (k3s bootstrap)

Story Points: 3 (reduced from original — narrower scope)
Estimate: 0.5 day
Epic: AWS Infrastructure
Note: Scope narrowed because Spring/Kong/AI now deploy via Helm into k3s, not via Ansible+docker-compose.
```

**Reduce Story Points** to **3** (narrower scope).

---

### SCRUM-65 — `E1-04: Ollama + NVIDIA drivers on GPU instance`

**Current status:** In Review

**Change Summary to:**
> E1-04: NVIDIA driver install on GPU host (k3s runtime piece moved to E3-06)

**Replace Description with:**
```
As a platform engineer, I install the NVIDIA host driver on the GPU EC2 instance so that
the K8s NVIDIA device plugin (handled in E3-06/SCRUM-93) can expose GPU resources to pods.

Acceptance Criteria:
- nvidia_docker Ansible role updated/repurposed to install only the NVIDIA host driver
- nvidia-smi works on the host as the deploy user
- The container runtime configuration piece (nvidia-container-toolkit + containerd nvidia runtime)
  is OUT OF SCOPE here — that moves to SCRUM-93 (E3-06 NVIDIA device plugin spike)
- Verification: nvidia-smi shows the GPU and driver version

Story Points: 2 (reduced — narrower scope)
Estimate: 0.5 day
Epic: AWS Infrastructure
Blocks: SCRUM-93 (E3-06 NVIDIA device plugin spike)
Note: Original scope split between this story (host driver) and SCRUM-93 (K8s integration).
```

**Reduce Story Points** to **2**.

---

### SCRUM-66 — `E1-05: End-to-end cloud validation — all services healthy, dashboards live`

**Current status:** To Do

**Action: Close as "Won't Do — Superseded"** with a comment linking to SCRUM-97 (E3-10).

**Reason:** The end-to-end validation now needs to test the K8s-hosted target, which is exactly what SCRUM-97 (E3-10) does. Doing both is duplicate work.

**Comment to add:**
> Superseded by SCRUM-97 (E3-10: End-to-end K8s validation playbook). The original VM-target validation is no longer the ground truth — the K8s-target validation is. Closing this and consolidating the work into E3-10.

---

## Step 3 — Close this ticket as superseded

### SCRUM-82 — `E2-11: Docker-compose for AI stack — triage + 5 MCP servers + Ollama`

**Current status:** To Do

**Action: Close as "Won't Do — Superseded"** with a comment linking to SCRUM-92 (E3-05).

**Reason:** The AI stack is now packaged as a Helm chart (`charts/ai-stack/`) instead of a docker-compose template. The chart replaces the compose file entirely.

**Comment to add:**
> Superseded by SCRUM-92 (E3-05: Helm chart — AI stack). The K8s migration replaces docker-compose with a Helm chart for the AI namespace. Closing this and consolidating the work into E3-05.

---

## Step 4 — Verify Sprint 2 metadata

After import, confirm:

- [ ] **Sprint 2 due date** is `23/Apr/26` on both epics (SCRUM-84, SCRUM-85) and on the two new epics (SCRUM-86, SCRUM-98)
- [ ] **All 13 new stories** appear in the Sprint 2 board under their correct epic
- [ ] **Story point total** for Sprint 2 is roughly:
  - Existing in-flight (Done + In Review + In Progress + To Do): ~70 points (estimate based on current CSV)
  - New K8s stories: **34 points**
  - New AI stories: **8 points**
  - **New total: ~112 points** for the 2-week extension
- [ ] **Critical path** sequencing visible in the board (E3-01 → E3-02 → E3-03/04/05/06 → E3-07/08/09 → E3-10)

---

## Sprint 2 final story count

| | Before | After |
|---|---|---|
| Epics | 2 (Epic 1, Epic 2) | **4** (+ Epic 3 K8s, + Epic 4 AI Hardening) |
| Stories — Done | 9 | 9 (unchanged) |
| Stories — In Review | 5 | 5 (unchanged) |
| Stories — In Progress | 6 | 6 (unchanged) |
| Stories — To Do | 9 | 9 − 1 superseded (SCRUM-82) + 13 new = **21** |
| Total stories | 29 | **42** |
| Story points (rough) | ~70 | **~112** |

---

## Critical path / sequencing

```
SCRUM-63 (Terraform rescope) ──► E3-01 (k3s) ──┬─► E3-06 (NVIDIA spike)
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

---

## Risks to flag in your sprint review

1. **2 weeks is tight.** ~112 points is aggressive. If anything slips, descope the optional add-ons (none included here, so the only fat to cut is in AI-01/02/03 — not recommended).
2. **Team K8s onboarding (verbal, not tracked).** Anyone touching Epic 3 should work through Phases 1–4 of the [Kubernetes guide](https://github.com/linalaaraich/monitoring-docs/blob/main/kubernetes-guide.html) on a k3d cluster first. It will save more time than it costs. Communicate this verbally — it's not a story on the board.
3. **E3-02 (image build/import) blocks E3-05.** Sequence carefully — without images loaded into k3s containerd, the AI stack chart fails on `helm install` with `ImagePullBackOff`.
4. **E3-06 (NVIDIA spike) is unbounded.** Plan for 1–1.5 days. If it goes longer, time-box it and fall back to running Ollama CPU-only for the demo.
5. **E3-09 (alert rule migration) is a silent-failure risk.** All 17 rules must be tested individually after migration. Don't skip this.
6. **Network reachability** between monitoring VM and k3s cluster (port 6443, 10250) — confirm in SCRUM-63 (rescoped Terraform) before E3-08 starts.

---

## After import, delete this generator

Once the CSV is imported and the manual edits are done, you can safely delete:
- `Jira-additions.csv` (already imported)
- `generate_additions.py` (no longer needed)
- This README (or archive it)

The script is checked in for reproducibility — if you ever need to regenerate the rows (e.g. you re-run the import in a test project), just run `python3 generate_additions.py`.
