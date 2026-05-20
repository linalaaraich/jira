# Sprint 4 Additions — Manual Steps

This README accompanies `Sprint4-additions.csv` and `generate_sprint4_additions.py`. Mirrors the Sprint 3 import process — same 13-column format, same gotchas (Sprint, Story Points, Due date silently dropped by the importer; numeric Work Item IDs required).

## TL;DR

1. **Phase 0 — Jira hygiene clicks** (do this BEFORE importing — 5 small flips, ~10 min).
2. **Create Sprint 4** as a sprint object in Jira: name `SCRUM Sprint 4`, start `2026-05-20`, end `2026-06-03`.
3. **Close Sprint 3** via "Complete sprint" → tick "Move incomplete issues to Sprint 4" in the dialog. Six carry stories (SCRUM-149..154) move automatically.
4. **Import** `Sprint4-additions.csv` → 27 items: 3 epics (EPIC9/10/11) + 24 stories.
5. **Bulk-edit** Sprint, Story Points, Due date on the imported rows (the three columns Jira's importer drops — table below).
6. **Verify** Sprint 4 board: 3 epics, 24 stories under correct parent, ~88 SP total of which 2 SP already Done (P2 backfill).

---

## Phase 0 — Jira hygiene flips (do these FIRST)

These don't require Sprint 4 to exist; they correct the current Sprint 3 board:

1. **`SCRUM-135` (EPIC8 Hallucination firewall + trace depth) → Done.** All 9 child stories are Done; the epic banner shows To Do. One dropdown click.
2. **`SCRUM-148` (S3-CO-13 codify policy.py) → Dropped** (project status id 10036, exists in your workflow since 2026-04-10). Add a comment: *"Refactor superseded — policy logic stayed inline; not worth the 1 SP churn against shipped functionality."* The code files (`app/policy.py`, `app/bypass_llm.yaml`) don't exist; the Done state is currently a falsehood.
3. **`SCRUM-132` (EPIC5 RCA Quality v2 close-out) → Done** (assumes step 2 above flips S3-CO-13 to Dropped). With S3-CO-13 out of "live" status, all 12 remaining stories under EPIC5 are Done → epic should flip to Done.
4. **`SCRUM-133` (EPIC6 Operator feedback) → In Progress.** Three child stories already In Progress; the epic should reflect that.
5. **`SCRUM-134` (EPIC7 Drain3 baseline) → In Progress.** Same logic — three child stories already In Progress.

After Phase 0: the only "live" Sprint 3 work in Jira is the 6 carry stories under EPIC6 + EPIC7 (which Phase 3 will move into Sprint 4).

---

## Phase 1 — Create Sprint 4 sprint object

Jira UI → Project (SCRUM) → Backlog → "Create sprint".

- **Sprint name:** `SCRUM Sprint 4`
- **Start date:** `2026-05-20` (today)
- **End date:** `2026-06-03` (14-day cadence, matches the project's 2-week rhythm)

Don't start the sprint yet — wait until after Phase 4 so the import slots into the right sprint.

---

## Phase 2 — Close Sprint 3 (move incomplete → Sprint 4)

Open the Sprint 3 board → "..." menu → "Complete sprint".

In the close-dialog, Jira will list the 6 incomplete issues (SCRUM-149..154 = S3-FB-01..03 + S3-DR-01..03). Choose **"Move to Sprint 4"** from the dropdown (Sprint 4 must exist — that's why Phase 1 happens first). Click **Complete**.

Jira generates a Sprint 3 retro report — screenshot it. Useful for the FYP report's evaluation chapter.

---

## Phase 3 — Import `Sprint4-additions.csv`

**Jira UI path:** Project Settings → System → External system import → CSV.

1. Upload `Sprint4-additions.csv` (from this repo).
2. Select the SCRUM project as target.
3. Confirm field mapping — each column should auto-map (the format matches Sprint 3's). The three columns Jira asks about specifically for child-parent linkage are `Work item Id`, `Work type`, and `Parent`.
4. Run the dry-run preview → confirm 27 items, all 24 stories show their parent epic (EPIC9/10/11), commit.

If the parent links don't resolve (rare):
- Filter the CSV to just the 3 Epic rows (Work Item Ids 1, 2, 3), import those first.
- Then import the 24 Story rows — Jira will find the epics already in the project and link by Parent.

---

## Phase 4 — Bulk-edit Sprint, Story Points, Due date

Per the Sprint 3 lesson (`SPRINT3-README.md` §Step 2), Jira's CSV importer silently drops these three fields. Use the bulk-edit-by-board path:

1. After Phase 3 import, all 27 new items appear in the Backlog with no Sprint assigned.
2. Multi-select all 27 → "Move to Sprint" → choose **SCRUM Sprint 4**.
3. Story Points and Due date still need per-row updates. Use the per-story values below (copy-paste in batches of 5–10):

### Bulk-edit table — Story Points + Due date

| Work Item Id | Code | Status | Story Points | Due date |
|---|---|---|---|---|
| 1 | EPIC9 | To Do | (epic — no SP) | 03/Jun/26 |
| 2 | EPIC10 | To Do | (epic — no SP) | 03/Jun/26 |
| 3 | EPIC11 | To Do | (epic — no SP) | 03/Jun/26 |
| 4 | S4-LAT-01 | To Do | 5 | 03/Jun/26 |
| 5 | S4-LAT-02 | **Done** | 2 | **19/May/26** (shipped) |
| 6 | S4-LAT-03 | To Do | 2 | 03/Jun/26 |
| 7 | S4-LAT-04 | To Do | 2 | 03/Jun/26 |
| 8 | S4-PR-01 | To Do | 3 | 03/Jun/26 |
| 9 | S4-PR-02 | To Do | 5 | 03/Jun/26 |
| 10 | S4-PR-03 | To Do | 3 | 03/Jun/26 |
| 11 | S4-PR-04 | To Do | 1 | 03/Jun/26 |
| 12 | S4-PR-05 | To Do | 3 | 03/Jun/26 |
| 13 | S4-PR-06 | To Do | 5 | 03/Jun/26 |
| 14 | S4-CR-01 | To Do | 8 | 03/Jun/26 |
| 15 | S4-CR-02 | To Do | 5 | 03/Jun/26 |
| 16 | S4-CR-03 | To Do | 13 | 03/Jun/26 |
| 17 | S4-CR-04 | To Do | 5 | 03/Jun/26 |
| 18 | S4-CR-05 | To Do | 3 | 03/Jun/26 |
| 19 | S4-CR-06 | To Do | 1 | 03/Jun/26 |
| 20 | S4-CR-07 | To Do | 1 | 03/Jun/26 |
| 21 | S4-CR-08 | To Do | 5 | 03/Jun/26 |
| 22 | S4-CR-09 | To Do | 2 | 03/Jun/26 |
| 23 | S4-CR-10 | To Do | 3 | 03/Jun/26 |
| 24 | S4-CR-11 | To Do | 3 | 03/Jun/26 |
| 25 | S4-CR-12 | To Do | 5 | 03/Jun/26 |
| 26 | S4-CR-13 | To Do | 1 | 03/Jun/26 |
| 27 | S4-CR-14 | To Do | 2 | 03/Jun/26 |

Story Points also live in each ticket's Description metadata footer for cross-check.

---

## Phase 5 — Start Sprint 4

After Phase 4 verification, open Sprint 4 in the Jira board → "Start sprint".

Jira will prompt for sprint goal — paste:
> Close the output-quality and latency gaps surfaced by the 2026-05-19 live-load investigation (P0–P11). Anchor on the latency bundle (S4-LAT-01) and the deterministic diagnostic-steps generator (S4-PR-02) for week 1.

---

## What's in the import

### 3 themed epics

| Epic | Theme | Items from `sprint-history.html` ranked list | Stories |
|---|---|---|---|
| **EPIC9** Latency + suppression | Close the latency gap (90s median target, 6 min reality) + close the P2 cascade (DONE) + dashboard amber/grey | rows 1, 2, 6, 15 | S4-LAT-01..04 (4 stories) |
| **EPIC10** RCA prose honesty | Close the gap between RCA-prose intent and reality (no PromQL/raw floats in lede; no hallucinated metric names; no duplicate diagnostic_steps) | rows 3, 4, 7, 8, 9, 11 | S4-PR-01..06 (6 stories) |
| **EPIC11** Correlation + retrieval + carry | US-5.2 incident correlator + MCP native tool-calling + Tier 3 + curated RAG + resilience + polish | rows 5, 10, 12, 13, 14, 16–24 | S4-CR-01..14 (14 stories) |

### 24 stories with P-tag mapping

| Code | P-tag | Title | SP | Status |
|---|---|---|---|---|
| S4-LAT-01 | **P0+P9** | Latency bundle — 180s timeout + per-stage instrumentation + Ollama concurrency cap | 5 | To Do |
| S4-LAT-02 | **P2** | Suppression cascade fixes (synthetic-fingerprint filter + lookback 15→10 + recurrence gate widening) | 2 | **Done** |
| S4-LAT-03 | **P5** | Drain3 + empty-actions auto-downgrade | 2 | To Do |
| S4-LAT-04 | **P7** | Dashboard `dismiss_with_recommendation` colour | 2 | To Do |
| S4-PR-01 | **P1** | PromQL & numerical-noise scrubber | 3 | To Do |
| S4-PR-02 | **P3** | Deterministic diagnostic-steps generator | 5 | To Do |
| S4-PR-03 | **P4** | Hallucination on truncated metric names | 3 | To Do |
| S4-PR-04 | **P11** | Tighter `_classify_rca_quality` | 1 | To Do |
| S4-PR-05 | **P8** | Corpus reclassification + nightly post-hoc | 3 | To Do |
| S4-PR-06 | **P6** | Exemplar prose rewrites + overlap-detection validator | 5 | To Do |
| S4-CR-01 | **P10** | US-5.2 Incident correlator | 8 | To Do |
| S4-CR-02 | — | MCP native tool-calling rewrite | 5 | To Do |
| S4-CR-03 | — | Tier 3 — Iterative agentic gather | 13 | To Do |
| S4-CR-04 | — | Curated RAG retrieval (BM25 over feedback YAML) | 5 | To Do |
| S4-CR-05 | — | Weekly curation job | 3 | To Do |
| S4-CR-06 | — | Pod-level alert rule fixes | 1 | To Do |
| S4-CR-07 | — | O-9 webhook auth + O-10 nightly RCA-history S3 backup | 1 | To Do |
| S4-CR-08 | — | Sentence-transformers retriever (fallback) | 5 | To Do |
| S4-CR-09 | — | Trace-ID linkage from log anomalies | 2 | To Do |
| S4-CR-10 | — | RCA playbook templates | 3 | To Do |
| S4-CR-11 | — | US-5.7 Labelled corpus expansion + F1 tracking | 3 | To Do |
| S4-CR-12 | — | L2/L3 chaos scenarios (O-12) | 5 | To Do |
| S4-CR-13 | — | Drain3 self-monitoring loop allowlist | 1 | To Do |
| S4-CR-14 | — | Doc debt — CLAUDE.md + stale PNGs | 2 | To Do |

**Total: 88 SP across 24 stories** (2 SP already Done = P2 backfill). Sprint 4 realistic 2-week velocity per project history ≈ 25–35 SP — the long tail (EPIC11) is intentionally a backlog buffer, not all expected to ship in this sprint.

### Plus 6 carry-forward stories from Sprint 3 (moved by Phase 2 close-dialog, NOT in this CSV)

| Code | Jira key | Title | SP | Status |
|---|---|---|---|---|
| S3-FB-01 | SCRUM-149 | Feedback schema extension + 4 MCP tools | 4 | In Progress (carried) |
| S3-FB-02 | SCRUM-150 | Operator rating UI | 2 | In Progress (carried) |
| S3-FB-03 | SCRUM-151 | Feedback observability | 1 | To Do (carried) |
| S3-DR-01 | SCRUM-152 | Drain3 scheduled snapshots + boot restore | 3 | In Progress (carried) |
| S3-DR-02 | SCRUM-153 | Drain3 operator endpoints | 2 | In Progress (carried) |
| S3-DR-03 | SCRUM-154 | Drain3 IAM + Grafana visibility | 1 | In Progress (carried) |

These stay under their original Sprint 3 epics (EPIC6, EPIC7) — they're not re-attributed to Sprint 4 epics. Total carry = 13 SP.

### Sprint 4 grand total (after import + carry)

- **88 SP** new + **13 SP** carry = **101 SP nominal**, of which **2 SP** already Done (P2 backfill).
- Realistic-throughput burndown: top 8–10 items only (per `sprint-history.html` §"Suggested week-1 execution order"); the rest stays as ranked backlog inside Sprint 4 for visibility.

---

## Week-1 execution order (Sprint 4 day 1 — 2026-05-20)

From `sprint-history.html` §"Suggested execution order for week 1":

> Items 1 → 2 → 3 → 4 + 8 (paired). Items 1+2+8 together are ~8 hours of effort and deliver the biggest perceived-quality improvement.

Concrete order, mapped to the Sprint 4 CSV stories:

1. **S4-LAT-01 sub-task 3: Ollama concurrency cap = 1** (~30 min). Smallest blast radius, fastest validation.
2. **S4-LAT-01 sub-task 2: 180s pipeline timeout + raw-alert fallback** (~1 h).
3. **S4-LAT-01 sub-task 1: per-stage instrumentation** (~2 h). Find the scratch-branch draft from the investigation window first.
4. **S4-PR-04: Tighter `_classify_rca_quality`** (~1 h). 1 SP quick-win, same-day ship.
5. **S4-PR-01: PromQL scrubber** (~4 h, 3 SP).
6. **S4-PR-02: Deterministic diagnostic-steps generator** (~6 h, 5 SP) — pair with S3-DR-01..03 (carry — same Python loadout in `app/`).

Re-run `audit-live.sh` after each S4-LAT-01 sub-task to confirm the queue serialises and the timeout fires correctly.

---

## Notes / risks

1. **Numeric Work Item IDs required** — same constraint as Sprint 3. Saved at `feedback_jira_csv_import.md`.
2. **Sprint, Story Points, Due date silently dropped** — known Jira importer behaviour. Phase 4 above is the manual fix-up.
3. **88 SP of new stories in 2 weeks is unrealistic** for a 3-person team — the long tail (EPIC11) is intentionally a backlog buffer. Top 8–10 items only are the realistic Sprint 4 commitment.
4. **No new dependencies on dropped scope.** GPU migration explicitly dropped 2026-05-19; MCP native tool-calling rewrite (S4-CR-02) was its only dependency and is now unblocked on the laptop directly.
5. **S4-LAT-02 P2 backfill is already Done** — historical attribution only, no actual work pending. Audit trail completeness.

---

## After import, archive

Once the CSV is imported and the manual edits are done:
- `Sprint4-additions.csv` (already imported)
- This README (or keep for the post-mortem)
- `generate_sprint4_additions.py` keeps as the regenerable template if anything needs regeneration
