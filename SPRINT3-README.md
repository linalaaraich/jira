# Sprint 3 Additions — Manual Steps

This README accompanies `Sprint3-additions.csv` and covers the changes that **cannot be done via CSV import** (Sprint, Story Points, and Due date custom fields don't carry over — same Jira CSV importer limitation that hit Sprint 2).

## TL;DR

1. **Import** `Sprint3-additions.csv` into the SCRUM project — 32 new items: 4 epics + 28 stories.
2. **Manually set** Sprint, Story Points, Due date on each imported item (the CSV columns are present but Jira's importer drops them — same as Sprint 2).
3. **Verify** Sprint 3 board layout: 4 epics, all stories under correct epic, 77 SP total.

> **Note:** Sprint 3 is purely additive. Unlike Sprint 2, no existing tickets need rescoping or supersession.

---

## Step 1 — Import the new CSV

The CSV contains 32 items in 13 columns matching the Sprint 2 format (the only delta is **numeric Work Item IDs**, which the current Jira importer requires — string IDs throw `For input string` NumberFormatException).

| Type | Count |
|---|---|
| Epic | 4 (Epic 5–8: RCA Quality close-out, Operator feedback loop, Drain3 baseline lifecycle, Hallucination firewall + trace depth) |
| Story | 28 (S3-CO-01 → S3-CO-13, S3-FB-01 → S3-FB-03, S3-DR-01 → S3-DR-03, S3-HF-01 → S3-HF-09) |

The 13 columns:

| # | Column | Maps to | Notes |
|---|---|---|---|
| 1 | `Work item Id` | Work item Id | **Numeric** (1–32). Used to resolve parent links within this CSV; Jira assigns final keys (SCRUM-132+) on import. |
| 2 | `Summary` | Summary | Carries the human-readable code prefix (`EPIC5:`, `S3-HF-01:`, etc.) so the import-time numeric ID stays cross-referenceable with `monitoring-docs/sprint3-plan.md`. |
| 3 | `Work type` | Work type | `Epic` or `Story` |
| 4 | `Status` | Status | `To Do`, `In Progress`, or `Done` (close-out items already shipped). |
| 5 | `Priority` | Priority | `Highest` / `High` / `Medium` / `Low` |
| 6 | `Labels` | Labels | One of `RCA-Quality`, `Feedback`, `Drain3`, `Hallucination-Firewall`. **Imports correctly** (verified against Sprint 2 — labels carry over). |
| 7 | `Description` | Description | Includes a `Cross-reference: US-3.X` line in the metadata footer mapping each Jira ID back to the plan doc. |
| 8 | `Sprint` | Sprint | All `SCRUM Sprint 3` — **but does NOT carry over via CSV**. See Step 2. |
| 9 | `Story Points` | Story Points | **Does NOT carry over via CSV**. See Step 2. |
| 10 | `Parent` | Parent | Numeric — references the parent epic's Work Item Id (`1`, `2`, `3`, or `4`). |
| 11 | `Reporter` | Reporter | `Lina Laaraich` |
| 12 | `Assignee` | Assignee | `Lina Laaraich` for stories, empty for epics. |
| 13 | `Due date` | Due date | All `08/May/26` — **does NOT carry over via CSV**. See Step 2. |

**Jira import path:**
1. Project Settings → System → External system import → CSV
2. Upload `Sprint3-additions.csv`
3. Select the SCRUM project as the target
4. Field mapping: each column should auto-map to its Jira field. The 3 columns Jira specifically asks about for child-parent relationships are all present: `Work item Id`, `Work type`, and `Parent`.
5. Run the dry-run preview, confirm 32 items and that all 28 stories show their parent epic, commit.

**If parent links don't resolve** (rare):
- Filter the CSV to just the 4 Epic rows (Work Item Ids `1`–`4`), import those first
- Then import the 28 Story rows — Jira will find the epics already in the project and link by `Parent`

---

## Step 2 — Manual fix-up of Sprint, Story Points, Due date

These three fields are documented in the CSV but **the Jira CSV importer drops them silently** (verified on Sprint 2 — SCRUM-119..131 came back with no values for these custom fields, and the Sprint 2 README captured the same gotcha).

The fastest fix is the **bulk-edit-by-Sprint-board** path:

1. Create the **SCRUM Sprint 3** sprint object first (Backlog → "Create sprint"; set name to `SCRUM Sprint 3`, start `2026-04-23`, end `2026-05-08`).
2. After import, all 32 new items appear in the backlog (no sprint assigned).
3. **Multi-select** all 32 → **Move to Sprint 3** (one bulk action).
4. **Story Points and Due date** still need per-row updates. Use the per-story values listed below — copy-paste in batches of 5–10:

### Story Points + Due date table (paste into bulk editor)

| Work Item Id (CSV) | Code | Story Points | Due date |
|---|---|---|---|
| 1 | EPIC5 | (epic, no SP) | 08/May/26 |
| 2 | EPIC6 | (epic, no SP) | 08/May/26 |
| 3 | EPIC7 | (epic, no SP) | 08/May/26 |
| 4 | EPIC8 | (epic, no SP) | 08/May/26 |
| 5 | S3-CO-01 | 3 | 08/May/26 |
| 6 | S3-CO-02 | 3 | 08/May/26 |
| 7 | S3-CO-03 | 5 | 08/May/26 |
| 8 | S3-CO-04 | 3 | 08/May/26 |
| 9 | S3-CO-05 | 5 | 08/May/26 |
| 10 | S3-CO-06 | 8 | 08/May/26 |
| 11 | S3-CO-07 | 5 | 08/May/26 |
| 12 | S3-CO-08 | 3 | 08/May/26 |
| 13 | S3-CO-09 | 3 | 08/May/26 |
| 14 | S3-CO-10 | 5 | 08/May/26 |
| 15 | S3-CO-11 | 3 | 08/May/26 |
| 16 | S3-CO-12 | 2 | 08/May/26 |
| 17 | S3-CO-13 | 1 | 08/May/26 |
| 18 | S3-FB-01 | 4 | 08/May/26 |
| 19 | S3-FB-02 | 2 | 08/May/26 |
| 20 | S3-FB-03 | 1 | 08/May/26 |
| 21 | S3-DR-01 | 3 | 08/May/26 |
| 22 | S3-DR-02 | 2 | 08/May/26 |
| 23 | S3-DR-03 | 1 | 08/May/26 |
| 24 | S3-HF-01 | 1 | **29/Apr/26** (shipped) |
| 25 | S3-HF-02 | 1 | **29/Apr/26** (shipped) |
| 26 | S3-HF-03 | 2 | **29/Apr/26** (shipped) |
| 27 | S3-HF-04 | 1 | 08/May/26 |
| 28 | S3-HF-05 | 1 | 08/May/26 |
| 29 | S3-HF-06 | 2 | 08/May/26 |
| 30 | S3-HF-07 | 3 | 08/May/26 |
| 31 | S3-HF-08 | 2 | 08/May/26 |
| 32 | S3-HF-09 | 2 | 08/May/26 |

The Story Points are also visible in each ticket's Description metadata footer (the `Story Points: N` line) — handy for double-checking when filling Jira.

---

## Step 3 — Verify Sprint 3 metadata

After import + bulk edit, confirm:

- [ ] **4 epics** in Sprint 3 board: Epic 5 (RCA Quality close-out), Epic 6 (Operator feedback loop), Epic 7 (Drain3 baseline lifecycle), Epic 8 (Hallucination firewall + trace depth)
- [ ] **28 stories** assigned under correct parent epic
- [ ] **Sprint 3 due date** is `08/May/26` on epic-level due dates
- [ ] **Story Points total** = 77 SP:
  - Epic 5 close-out: 49 SP (mostly Done)
  - Epic 6 feedback: 7 SP
  - Epic 7 Drain3: 6 SP
  - Epic 8 hallucination firewall: 15 SP (3 SP shipped 29/Apr)
- [ ] **3 stories already Done** (S3-HF-01, S3-HF-02, S3-HF-03) — committed to monitoring-triage-service main:
  - S3-HF-01 + S3-HF-02 → commit `b0f1d0c`
  - S3-HF-03 → commit `d6d10ef`

---

## Sprint 3 story count

| | Count |
|---|---|
| Epics | 4 (Epic 5–8) |
| Stories — Done | 13 (12 close-out + 3 hallucination firewall already shipped, less In-Progress S3-CO-02 = 13 actually shipped at import time) |
| Stories — In Progress | 1 (S3-CO-02 entity baselines verification, gated on S3-HF-04) |
| Stories — To Do | 14 |
| Total | **32 work items, 77 SP** |

---

## Cross-reference with the plan doc

Each story's `Description` carries a `Cross-reference: US-3.X` line in its metadata footer that maps the Jira Work Item Id (numeric) and the Sprint-3-specific code (`S3-CO-01`, `S3-HF-01`, etc.) back to the canonical `US-3.X` IDs used throughout `monitoring-docs/sprint3-plan.md`. So when Lina opens any Jira ticket, she can grep `sprint3-plan.md` for the matching US-3.X line and see file-path-level acceptance criteria.

Triage-service commit messages also use the `S3-HF-XX` codes (e.g., commit `b0f1d0c` references S3-HF-01 + S3-HF-02), so the chain is: Jira ticket title → Description footer → `US-3.X` in plan → triage-service commit.

---

## Notes / risks

1. **String-IDs in Sprint 2 but numeric required for Sprint 3** — the Jira CSV importer behavior changed between import attempts. Numeric Work Item IDs are the safe choice going forward. Saved to memory at `feedback_jira_csv_import.md`.
2. **Sprint, Story Points, Due date silently dropped** — known Jira CSV importer behavior. The above per-row table is the manual-fix-up reference. Same gotcha hit Sprint 2.
3. **Tier 0 (S3-HF-01) shipped same day** as the incident that triggered Epic 8. The 0b215ef3 templated-kubectl email won't ship again; the F-4 clamp now strips actions and emits read-only `diagnostic_steps` instead.
4. **Tier 3 (iterative agentic loop)** explicitly deferred to Sprint 4 — gates on Tier 4 measurement scaffold (S3-HF-09) being green first. See `monitoring-docs/sprint3-plan.md` § "Sprint 4 candidates" for the deferred design choices (per-severity budget, tree-narrowed definition, cost ceiling).

---

## After import, archive

Once the CSV is imported and the manual edits are done, you can safely archive:
- `Sprint3-additions.csv` (already imported)
- `jira-export.zip` (was a snapshot used to validate the CSV format)
- This README (or keep for the post-mortem)
