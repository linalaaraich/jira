#!/usr/bin/env python3
"""
Generate Sprint4-additions.csv — the Jira import CSV for Sprint 4.

Sprint 4 window: 2026-05-20 -> 2026-06-03 (2 weeks).
Goal: import 3 themed epics + 24 stories (1 already Done — the P2 hotfix backfill
shipped 2026-05-19) into Jira's SCRUM project. Mirrors the Sprint 3 format
(`Sprint3-additions.csv`): 13 columns, numeric Work Item IDs for parent linkage,
human-readable code prefixed onto Summary, P-tag and gate citation in Description.

Sprint 4 epic shape (4 themed epics — see SESSION_HANDOFF.md §Decision 2,
plus EPIC12 added 2026-05-21 per chat re: predictive observability roadmap):
  EPIC9  = Latency + suppression       (items 1, 2[done], 6, 15 = S4-LAT-01..04)
  EPIC10 = RCA prose honesty           (items 3, 4, 7, 8, 9, 11 = S4-PR-01..06)
  EPIC11 = Correlation + retrieval + carry (items 5, 10, 12, 13, 14, 16-24
                                            = S4-CR-01..14)
  EPIC12 = Predictive observability    (items 26-29 = S4-PRED-01..04 — added
                                        2026-05-21 from SESSION_HANDOFF.md §C
                                        predictive roadmap. Carve-out: P-3
                                        runway + P-5 saturation bands + P-2
                                        cascade predictor + detective-signals
                                        UI tab. P-1 / P-4 / P-6 deferred.)

Sprint 3 spillover stories (S3-FB-01..03, S3-DR-01..03 = SCRUM-149..154) are
moved into Sprint 4 via Jira's 'Close sprint -> Move incomplete to Sprint 4'
dialog. They are NOT re-imported via this CSV.

Numeric Work Item IDs in this CSV start at 1 and are used only for parent
linkage at import time. Jira will assign SCRUM-NNN keys on import. Per
Sprint 3 lesson, the Sprint / Story Points / Due-date columns are silently
dropped by the importer — SPRINT4-README.md has the per-row bulk-edit table.
"""

import csv

USER = "Lina Laaraich"
SPRINT_NAME = "SCRUM Sprint 4"
SPRINT_DUE = "03/Jun/26"
P2_SHIPPED_DUE = "19/May/26"  # P2 hotfix already shipped — historical due date

# NOTE: 11-column format for Sprint 4 (down from Sprint 3's 13).
#
# Sprint 3 used the canonical 13-column shape including Sprint + Story Points,
# both of which Jira's importer silently DROPPED at import time. By 2026-05-20
# the importer has been tightened: it now ERRORS on those two columns instead
# of dropping them silently ("Sprint id must be a number" + "Custom Field
# 'Story Points' is not associated with issue type 'Story'"). Since they were
# always going to be bulk-edited post-import anyway (see SPRINT4-README.md
# §Phase 4), we omit them from the CSV.
HEADERS = [
    "Work item Id", "Summary", "Work type", "Status", "Priority",
    "Labels", "Description",
    "Parent", "Reporter", "Assignee", "Due date",
]

# Epic Work Item IDs inside this CSV
#
# IMPORTANT: Jira's CSV importer treats numeric Work Item Ids as PERSISTENT
# per project when the import-screen field-mapping uses "Work item Id" (the
# parent-linkage field, not "Work item Key"). Sprint 3 used IDs 1..32, so any
# CSV id in that range collides with Sprint 3's mapped issues and triggers
# update-mode (Jira reports them as "already exist, skipped"). Start Sprint 4
# at 100 to leave a comfortable buffer for any future Sprint-3 backfills.
EPIC9_ID = "100"
EPIC10_ID = "101"
EPIC11_ID = "102"
EPIC12_ID = "200"  # gap-jump to 200 to keep EPIC band visually distinct from
                   # the story band (103-127 + 128-131 added 2026-05-21)


def desc(body: str, p_tag: str, evidence: str, gate: str,
         sprint_history_row: int, cross_ref: str = "") -> str:
    """Standard story description body with metadata footer for traceability."""
    lines = [body.strip(), "", f"Evidence (2026-05-19 live-load investigation): {evidence}",
             f"Gate: {gate}"]
    if cross_ref:
        lines += ["", cross_ref]
    lines += [
        "",
        "---",
        f"P-tag: {p_tag}" if p_tag else "P-tag: — (carry-forward from sprint3-backlog.md)",
        f"Source: monitoring-docs/sprint-history.html §Sprint 4 candidates row {sprint_history_row}",
    ]
    return "\n".join(lines)


def epic_desc(theme: str, items_summary: str, story_codes: str) -> str:
    return "\n".join([
        theme.strip(),
        "",
        f"Stories in this epic: {story_codes}",
        f"Items from the 24-item ranked list (sprint-history.html): {items_summary}",
        "",
        "Acceptance: all child stories Done by sprint end (2026-06-03), or carried with explicit rationale.",
    ])


# ------------------------------ EPICS ------------------------------

EPICS = [
    {
        "Work item Id": EPIC9_ID,
        "Summary": "EPIC9: Sprint 4 -- Latency + suppression",
        "Work type": "Epic",
        "Status": "To Do",
        "Priority": "Highest",
        "Labels": "Latency",
        "Description": epic_desc(
            "Close the latency gap between the laptop steady-state target "
            "(median <=90s, worst <=240s) and the observed reality (median "
            "6-7 min, worst 23 min on 2026-05-19 live load). Also closes the "
            "P2 suppression cascade (already shipped 2026-05-19 -- backfilled "
            "as Done story for audit trail) and the dashboard 'dismiss with "
            "recommendation' colour gap (P7).",
            "1 (P0+P9 latency bundle), 2 (P2 suppression cascade -- DONE), "
            "6 (P5 Drain3+empty-actions auto-downgrade), 15 (P7 dashboard colour)",
            "S4-LAT-01, S4-LAT-02, S4-LAT-03, S4-LAT-04",
        ),
        "Parent": "",
        "Reporter": USER, "Assignee": "", "Due date": SPRINT_DUE,
    },
    {
        "Work item Id": EPIC10_ID,
        "Summary": "EPIC10: Sprint 4 -- RCA prose honesty",
        "Work type": "Epic",
        "Status": "To Do",
        "Priority": "High",
        "Labels": "RCA-Prose",
        "Description": epic_desc(
            "Close the gap between RCA-prose intent (cause-first, "
            "evidence-cited, no PromQL or raw floats in the lede) and the "
            "2026-05-19 reality (Z-score equations and 16-digit floats "
            "appearing in cause prose; hallucinated metric names from "
            "truncation artifacts; word-for-word identical diagnostic_steps "
            "across distinct incidents).",
            "3 (P1 PromQL scrubber), 4 (P3 deterministic diagnostic-steps), "
            "7 (P4 truncated-name hallucination), 8 (P11 tighter classifier), "
            "9 (P8 corpus reclassify), 11 (P6 exemplar prose rewrites)",
            "S4-PR-01, S4-PR-02, S4-PR-03, S4-PR-04, S4-PR-05, S4-PR-06",
        ),
        "Parent": "",
        "Reporter": USER, "Assignee": "", "Due date": SPRINT_DUE,
    },
    {
        "Work item Id": EPIC11_ID,
        "Summary": "EPIC11: Sprint 4 -- Correlation + retrieval + carry",
        "Work type": "Epic",
        "Status": "To Do",
        "Priority": "Medium",
        "Labels": "Correlation",
        "Description": epic_desc(
            "Absorbs the long-tail Sprint 4 backlog: the incident correlator "
            "(US-5.2 carry from Sprint 2), the MCP native tool-calling rewrite "
            "(GPU-gate removed 2026-05-19), Tier 3 iterative agentic gather "
            "(now unblocked by S3-HF-09 Tier 4 scoreboard), curated RAG + "
            "weekly curation (deferred from Sprint 3), and resilience / "
            "polish items.",
            "5 (P10 US-5.2 correlator), 10 (MCP native tool-calling), "
            "12 (Tier 3), 13 (curated RAG), 14 (weekly curation), "
            "16 (pod-alert fixes), 17 (O-9+O-10), 18 (sentence-transformers), "
            "19 (trace-ID linkage), 20 (RCA playbook), 21 (US-5.7 corpus), "
            "22 (L2/L3 chaos), 23 (Drain3 self-mon allowlist), 24 (doc debt)",
            "S4-CR-01 through S4-CR-14",
        ),
        "Parent": "",
        "Reporter": USER, "Assignee": "", "Due date": SPRINT_DUE,
    },
    {
        "Work item Id": EPIC12_ID,
        "Summary": "EPIC12: Sprint 4 -- Predictive observability",
        "Work type": "Epic",
        "Status": "To Do",
        "Priority": "Medium",
        "Labels": "Predictive",
        "Description": epic_desc(
            "Surface forward-looking signals so the operator sees a "
            "developing problem BEFORE the post-incident page. Today the "
            "platform is reactive -- every code path assumes an alert has "
            "fired. EPIC12 adds a thin predictive layer using data the "
            "platform already collects: PromQL trajectory math via "
            "predict_linear() (capacity-runway dashboard), percentile-band "
            "entity baselines (saturation bands), historical cascade "
            "probabilities mined from rca_history.db (cascade predictor), "
            "and a UI tab that aggregates the detective signals already in "
            "the system (Drain3 novelty + entity sigma-claims + recurrence-"
            "gate fires). All four stories are PoC-test-bed-shippable in "
            "Sprint 4. The heavier ML lift (Prophet/Holt-Winters forecasting "
            "P-1, pre-deploy canary diff P-4, trace-shape predictor P-6) is "
            "deferred to Sprint 5+. Carve-out chosen 2026-05-21 from the "
            "SESSION_HANDOFF.md §C predictive-roadmap draft.",
            "26 (detective-signals UI tab), 27 (P-3 capacity-runway "
            "dashboard), 28 (P-5 saturation-band baselines), 29 (P-2 "
            "cascade predictor, partners with S4-CR-01)",
            "S4-PRED-01, S4-PRED-02, S4-PRED-03, S4-PRED-04",
        ),
        "Parent": "",
        "Reporter": USER, "Assignee": "", "Due date": SPRINT_DUE,
    },
]


# ------------------------------ STORIES ------------------------------

# Story tuple format:
#   (code, summary_tail, status, priority, parent_epic_id, p_tag, sp,
#    body, evidence, gate, history_row, due_date_override)
STORIES = [
    # ------ EPIC9: Latency + suppression ------
    ("S4-LAT-01",
     "Latency bundle -- 180s pipeline timeout + per-stage instrumentation + Ollama concurrency cap",
     "To Do", "Highest", EPIC9_ID, "P0+P9", "5",
     "Three sub-tasks that compound to pull median RCA latency from ~6 min "
     "to ~90s on the laptop runner: (1) Ollama concurrency cap = 1 (serial "
     "queue, no GPU time-sharing); (2) hard 180s asyncio.wait_for around "
     "the pipeline entry, with raw-alert fallback on TimeoutError; (3) "
     "per-stage histogram triage_pipeline_duration_seconds{stage} across "
     "webhook-receive / context-gather / exemplar-match / LLM-call / "
     "validate / retry / persist / notify. Per-stage instrumentation was "
     "drafted in a scratch branch during the investigation window -- find "
     "and rebase rather than re-scaffold.",
     "median 6-7 min, worst 23 min (PodHighMemoryUsage 2026-04-29); today's "
     "2nd TargetDown took 16.7 min queued behind first; audit-live run #3 on "
     "2026-05-20 hit the queue blowup again",
     "median investigation_duration_ms <= 90s, worst <= 240s, queue depth <= 3",
     1, None),
    ("S4-LAT-02",
     "P2: Suppression cascade fixes (synthetic-fingerprint filter + lookback 15->10 + recurrence-gate widening)",
     "Done", "High", EPIC9_ID, "P2", "2",
     "Three fixes shipped 2026-05-19, validated 2026-05-20 via 3-run "
     "audit-live gate:\n"
     "  (1) Synthetic-fingerprint filter in get_recent_decision_for_alert -- "
     "      audit-live-* and chaos-* fingerprints never poison real "
     "      suppression cache. (monitoring-triage-service@b96bbde)\n"
     "  (2) TRIAGE_HISTORY_LOOKBACK_MINUTES 15 -> 10. (same commit)\n"
     "  (3) recurrence_gate annotation widened to HighP95Latency + "
     "      HighKongP95Latency. (monitoring-project@54b18df)\n"
     "Suite stepped 249 -> 252 with 3 new regression tests. Backfilled as a "
     "Done ticket for audit-trail completeness.",
     "one synthetic dismiss at 13:32 silenced 4 real MediumCpuUsage fires "
     "through 13:41; one real dismiss at 13:54 silenced 3 TargetDown "
     "follow-ups through 14:07 (both observed 2026-05-19)",
     "3-run audit-live gate: zero audit-live-* /decisions rows have "
     "triage_decision=triage_suppressed (CLOSED 2026-05-20 09:00 UTC)",
     2, P2_SHIPPED_DUE),
    ("S4-LAT-03",
     "Drain3 + empty-actions auto-downgrade",
     "To Do", "High", EPIC9_ID, "P5", "2",
     "Post-LLM gate: if verdict=escalate AND suggested_actions=[] AND no "
     "service named -> auto-downgrade to dismiss, prose preserved with the "
     "tag 'awaiting correlation'. For Drain3AnomalyDetected specifically, "
     "require >=2 novel templates in the same 5-min window before "
     "escalating (raise the per-alert threshold inside drain_analyzer.py).",
     "73784801 (2026-04-29) escalated for 'GET /robots.txt and Kong "
     "deprecation warnings' -- two unrelated observations, no causal "
     "connection, shelved actions. False page.",
     "for the 28-decision rerun: zero RCAs with verdict=escalate AND "
     "suggested_actions=[] AND no named cause; Drain3 escalations require "
     "the >=2-novel-templates condition",
     6, None),
    ("S4-LAT-04",
     "Dashboard dismiss_with_recommendation colour",
     "To Do", "Low", EPIC9_ID, "P7", "2",
     "New verdict bucket / colour at the dashboard layer: amber for "
     "'dismiss but rule needs fixing' vs grey for 'dismiss, ignore'. Requires "
     "a schema migration on rca_history adding a "
     "dismiss_with_recommendation boolean (default false). Card legend in "
     "dashboard-guide.html updated.",
     "36c23530 (2026-05-19) was a correct dismiss with suggested actions "
     "targeting the alerting RULE for a static-threshold misfire. Operator "
     "skimming 'dismiss' missed the actions.",
     "dashboard renders amber for dismiss_with_recommendation=true; "
     "rca_history schema migration applied; >=1 verdict in the corpus "
     "carries the flag and renders correctly",
     15, None),

    # ------ EPIC10: RCA prose honesty ------
    ("S4-PR-01",
     "PromQL & numerical-noise scrubber",
     "To Do", "High", EPIC10_ID, "P1", "3",
     "New validator rule rejecting RCA prose containing: PromQL function "
     "calls, raw floats > 4 sig figs, Z-score equations, metric names "
     "ending in '...' (truncation artefacts). New translate_value(value, "
     "unit) helper pre-renders metric values BEFORE prompt assembly so the "
     "LLM cites 'CPU usage 6.72%' rather than '0.0015848932803859128'. "
     "Strip '# TYPE' / '# HELP' / '...truncated...' markers from context "
     "before LLM sees it.",
     "RCAs literally contain 'Z-score: (6.72-6.3)/0.65 = +0.6 sigma', "
     "'histogram_quantile(0.95) = 8203.846153846154 ms', "
     "'sum by(le)(rate(http_server_requests_seconds_bucket{...}[5m]))' in "
     "cause-prose (sampled from 2026-05-19 live-load).",
     "audit script grep on last 50 RCAs returns zero hits on "
     "'histogram_quantile|rate\\(|sum by\\(|\\.\\d{6,}|sigma'",
     3, None),
    ("S4-PR-02",
     "Deterministic diagnostic-steps generator",
     "To Do", "High", EPIC10_ID, "P3", "5",
     "Move diagnostic-step generation OUT of the LLM into a deterministic "
     "helper app/diagnostic_steps_for_alert(alert, ctx) that templates from "
     "the actual gathered evidence: deep_trace trace_id, alert service, "
     "window timestamps, observed value. LLM still writes RCA prose + "
     "suggested_actions; diagnostic_steps become auto-generated from "
     "concrete IDs.",
     "111ded21 and a4555bdd (two different TargetDown fires on 2026-05-19) "
     "have word-for-word identical diagnostic_steps -- boilerplate not "
     "incident-specific",
     "two TargetDown RCAs from different fires have >=3 distinct "
     "diagnostic-step strings each (zero duplicates)",
     4, None),
    ("S4-PR-03",
     "Hallucination on truncated metric names",
     "To Do", "High", EPIC10_ID, "P4", "3",
     "Context sanitiser drops any line ending in '(truncated)' or '...]' "
     "before LLM sees it. New validator cross-checks cited metric names in "
     "RCA prose against app/metrics.py + a known Prometheus exposition "
     "registry; rejects RCAs that invent metric names.",
     "d763a9c9 (2026-04-29) invented cause 'metric \\\"jvm_threads_daem\\\" "
     "not being updated correctly' -- jvm_threads_daem is the truncated "
     "form of jvm_threads_daemon. The LLM treated a string-truncation "
     "artefact as a real component name.",
     "validator rejects any RCA citing a metric name not in the Prometheus "
     "exposition registry; sanitiser drops truncated lines before prompt "
     "assembly",
     7, None),
    ("S4-PR-04",
     "Tighter _classify_rca_quality",
     "To Do", "High", EPIC10_ID, "P11", "1",
     "New 'actionable' bar in app/rca_quality.py: requires (>=1 specific "
     "evidence item) AND (named cause in prose) AND (>=1 suggested action "
     "OR explicit 'dismiss with reasoning'). The old definition lets "
     "thin-evidence RCAs claim actionable; the new MCP "
     "get_similar_decisions(min_quality='actionable') is degraded by this.",
     "73784801 (Drain3 escalate with no cause), 36c23530 (a dismiss), "
     "a4555bdd (16-min on a 2-scrape blip) all tagged actionable -- the "
     "label has lost meaning",
     "rerunning _classify_rca_quality over the last 28 decisions demotes "
     "the three sample rows above to needs_review",
     8, None),
    ("S4-PR-05",
     "Corpus reclassification + nightly post-hoc validator",
     "To Do", "Medium", EPIC10_ID, "P8", "3",
     "Two parts: (1) manual SQL fix to reclassify 0b215ef3 (the 2026-04-29 "
     "bad incident) to needs_review and clear its suggested_actions -- ~10 "
     "min; (2) nightly APScheduler job that re-runs the current validator "
     "over the last 7d of stored RCAs and demotes any that would now fail "
     "-- ~3-4 h. Depends on P11 (S4-PR-04) shipping first since the new "
     "classifier defines what 'would now fail' means.",
     "0b215ef3 is still in rca_history with quality=actionable + the "
     "wrong-archetype kubectl OOM remediations on a Kong p95 alert. The new "
     "get_similar_decisions(min_quality='actionable') returns it as a "
     "positive exemplar.",
     "0b215ef3 carries quality=needs_review post-fix; nightly job has run "
     ">=1 cycle and the audit log shows demotions",
     9, None),
    ("S4-PR-06",
     "Exemplar prose rewrites + overlap-detection validator",
     "To Do", "Medium", EPIC10_ID, "P6", "5",
     "Rewrite app/exemplars/library.yaml so each exemplar uses "
     "{INSTANCE}, {N}, {TIMESTAMP} placeholders the LLM must substitute "
     "with concrete values from gathered context. Add a validator regex: "
     "if RCA prose has >80% char overlap with the matched exemplar prose, "
     "trigger a retry.",
     "2026-05-19 TargetDown RCAs are near-identical to each other and to "
     "the exemplar prose -- too much template leakage, not enough adaptation",
     "two same-archetype RCAs from different fires have <80% char-overlap "
     "to each other and to the exemplar; validator catches >80% overlap "
     "and triggers retry",
     11, None),

    # ------ EPIC11: Correlation + retrieval + carry ------
    ("S4-CR-01",
     "US-5.2 Incident correlator -- 4-alert kill-chain RCA collapsed into one email",
     "To Do", "Medium", EPIC11_ID, "P10", "8",
     "Real outages produce alert clusters; the cluster signature IS the "
     "signal. Add a 5-min/15-min co-occurrence detector at the webhook "
     "fan-in: when N alerts of related types fire within window W, collapse "
     "into a single 'incident' record and run one RCA against the cluster "
     "rather than N independent RCAs. Originally Sprint 2 Tier-1 priority; "
     "carried forward.",
     "4 MediumCpuUsage in 5 min + 4 TargetDown in 15 min on 2026-05-19, all "
     "treated independently. None said 'this is the 4th in 5 min -- pattern'.",
     "a synthetic 4-alert kill-chain produces ONE escalation email with the "
     "cluster signature in the subject, not four; the RCA prose names the "
     "shared upstream cause",
     5, None),
    ("S4-CR-02",
     "MCP native tool-calling rewrite",
     "To Do", "Medium", EPIC11_ID, "", "5",
     "Replace the prompt-engineered JSON-schema output path with native "
     "tool-calling (Ollama's tools API). Smaller prompts -> faster inference "
     "(compounds with S4-LAT-01 latency bundle). The GPU-migration gate "
     "was removed 2026-05-19 on cost grounds, so this proceeds on the laptop "
     "qwen2.5:7b directly. Originally sprint3-backlog #5.",
     "current bounded-agency retry plus structured-output schema overhead "
     "adds ~30% to LLM round-trip latency on observed traces",
     "round-trip latency on a fixed prompt set drops >=20% vs. the "
     "structured-output path; suite still green",
     10, None),
    ("S4-CR-03",
     "Tier 3 -- Iterative agentic gather (3-iteration tool-call loop with hypothesis-tree state)",
     "To Do", "Low", EPIC11_ID, "", "13",
     "Replaces the single-shot bounded_agency retry with a 3-iteration "
     "tool-call loop: each iteration produces a partial hypothesis tree the "
     "model expands on the next iteration. Hypothesis tree stored in the "
     "prompt as a structured section. Termination: confidence threshold "
     "reached, max-depth limit hit, or total latency budget exhausted. "
     "S3-HF-09 Tier 4 scoreboard now in place (shipped 2026-05-19) so the "
     "regression-gate dependency is satisfied.",
     "single-shot bounded_agency is too constrained for data-starved cases "
     "(observed in multiple chaos runs)",
     "Tier 3 path is feature-flagged; chaos corpus regression gate "
     "(S3-HF-09) shows no quality regression at flag-on; latency-budget "
     "guard caps tail at 240s",
     12, None),
    ("S4-CR-04",
     "Curated RAG retrieval (BM25 over feedback-curated YAML)",
     "To Do", "Low", EPIC11_ID, "", "5",
     "Once the Epic 2 feedback table has accumulated rated entries: BM25 "
     "retrieval over library_curated.yaml supplements the exemplar section "
     "with top-K=3 positive + K=2 anti-example matches. Was US-3.4 in "
     "Sprint 3 -- gated on feedback volume.",
     "investigation-window dry-run showed BM25 over the 14-archetype BASE "
     "library is degenerate (top-1 always matched exemplars.find_for_alert); "
     "enriched library is the actual production scenario",
     "BM25 top-1 hit on a curated library of >=20 entries is different "
     "from exemplars.find_for_alert >=30% of the time on a held-out sample",
     13, None),
    ("S4-CR-05",
     "Weekly curation job (APScheduler, Sundays 02:00 UTC)",
     "To Do", "Low", EPIC11_ID, "", "3",
     "APScheduler in-process job; reads the SQLite feedback table for the "
     "last 7d; entries above a quality threshold are written as YAML to "
     "library_curated.yaml. Was US-3.3 in Sprint 3 -- gated on feedback "
     "volume.",
     "curated retrieval requires a curated source; the curation has to be "
     "automatic to stay fresh",
     "weekly job has run >=1 cycle in production; "
     "library_curated.yaml exists and contains >=20 entries",
     14, None),
    ("S4-CR-06",
     "Pod-level alert rule fixes (memory cgroup-churn + CPU label mismatch)",
     "To Do", "Low", EPIC11_ID, "", "1",
     "Two query bugs noted at Sprint 3 ship time: (a) "
     "PodHighMemoryUsage cumulative expression doesn't aggregate across "
     "cgroup restarts -- container restart churn splits the timeseries; "
     "(b) PodHighCpuUsage has a label-mismatch between numerator/denominator. "
     "~30 min each.",
     "Sprint 3 chaos Run 4 (2026-04-28 PM) captured 0/2 for these alerts "
     "because of these query bugs",
     "both rules fire correctly in a fresh chaos run; PodHighMemoryUsage "
     "stays firing across a synthetic OOMKill loop",
     16, None),
    ("S4-CR-07",
     "O-9 webhook auth + O-10 nightly RCA-history S3 backup",
     "To Do", "Medium", EPIC11_ID, "", "1",
     "Friday-slot hardening, previously overdue: (a) O-9 -- HMAC signature "
     "validation on /webhook/grafana (rejects un-signed requests); (b) O-10 "
     "-- nightly mysqldump of rca_history -> s3://cires-observability-demo-*"
     "/backups/rca_history/YYYY-MM-DD.sql.gz with 30-day retention. ~30 min "
     "each.",
     "webhook is open to any caller on the tailnet; rca_history has no "
     "off-site backup -- single PVC failure = total decision-corpus loss",
     "/webhook/grafana rejects unsigned requests with 401; "
     "s3://.../backups/rca_history/ has >=1 .sql.gz from the last 24h",
     17, None),
    ("S4-CR-08",
     "Sentence-transformers retriever (RAG fallback)",
     "To Do", "Low", EPIC11_ID, "", "5",
     "Only if BM25 (S4-CR-04) underperforms in A/B against the curated "
     "library. Adds sentence-transformers/all-MiniLM-L6-v2 as an alternate "
     "retriever; quality-graded fallback when BM25 misses.",
     "BM25 is a coarse retriever; curated YAML is small but heterogeneous "
     "-- semantic similarity might beat lexical overlap on near-misses",
     "A/B over the 28-decision sample: sentence-transformers vs BM25 "
     "top-K=3; pick the winner. SKIP if BM25 is the winner.",
     18, None),
    ("S4-CR-09",
     "Trace-ID linkage from log anomalies",
     "To Do", "Low", EPIC11_ID, "", "2",
     "When a Drain3 anomaly fires, scan the affected log lines for trace_id "
     "patterns and jump to the corresponding Jaeger trace for richer context. "
     "Originally sprint3-backlog #2a.",
     "log anomalies and trace anomalies are currently two parallel streams; "
     "linking them surfaces the underlying request boundary",
     "for log lines containing a trace_id, the RCA carries a deep_trace "
     "field with the matched trace_id (>=80% extraction success in test "
     "corpus)",
     19, None),
    ("S4-CR-10",
     "RCA playbook templates",
     "To Do", "Low", EPIC11_ID, "", "3",
     "Per-alert-type playbook templates that the LLM populates rather than "
     "free-forms. Originally sprint3-backlog #2b. Complements Epic 2 "
     "feedback work -- rated playbooks become the curation source.",
     "current RCA prose is free-form against an exemplar; structured "
     "playbooks would constrain hallucination further on common alert types",
     ">=4 playbook templates exist for the most-common alert types; LLM "
     "uses them when the alert type matches; chaos run scores >=0.85 mean "
     "cause-named on those alert types",
     20, None),
    ("S4-CR-11",
     "US-5.7 Labelled corpus expansion + F1 tracking",
     "To Do", "Medium", EPIC11_ID, "", "3",
     "Builds on S3-HF-09's seed corpus (the 0b215ef3 incident itself): "
     "expand the labelled set to >=30 incidents and track precision / recall / "
     "F1 of the validator + classifier against the labels weekly. Pair with "
     "S4-CR-04 / S4-CR-05 for measurement coverage.",
     "S3-HF-09 shipped the scoreboard mechanism + seed; without an expanded "
     "labelled corpus, the scoreboard is undersampled",
     "labelled corpus >= 30 incidents; weekly F1 calculation runs and "
     "publishes to Grafana",
     21, None),
    ("S4-CR-12",
     "L2/L3 chaos scenarios (O-12)",
     "To Do", "Low", EPIC11_ID, "", "5",
     "Two additional chaos test classes beyond the current L1 set: L2 "
     "(network partition between services) and L3 (cascading failure -- "
     "downstream OOM triggers upstream timeout cascade).",
     "current chaos harness exercises L1 (single-service fault) scenarios; "
     "real outages tend to involve cascade dynamics",
     "two new chaos scenario classes in monitoring-project/playbooks; "
     "chaos-run reports cover them; chaos scorer 5-axis output captures "
     "the new behaviour",
     22, None),
    ("S4-CR-13",
     "Drain3 self-monitoring loop allowlist",
     "To Do", "Low", EPIC11_ID, "", "1",
     "30-min fix: extend the Drain3 polling layer with a service_name "
     "allowlist that excludes the triage service itself from its own "
     "anomaly detection (currently the Drain3 anomaly stream sometimes "
     "self-reports on the triage service's own log volume).",
     "behavioural concern surfaced 2026-04-29 -- Drain3 firing on the "
     "triage service's own logs creates a self-reflexive loop",
     "Drain3 poller skips service_name in the configured allowlist; "
     "triage service is in the default allowlist",
     23, None),
    ("S4-CR-14",
     "Doc debt -- CLAUDE.md refresh + stale architecture PNGs replaced",
     "To Do", "Low", EPIC11_ID, "", "2",
     "monitoring-project/CLAUDE.md last touched 2026-04 -- needs a refresh "
     "to reflect Sprint 3 close-out reality (Epic 4 closed, MCP-only "
     "invariant + CI lint, deep_trace path). Architecture PNGs in "
     "monitoring-docs are pre-AI-RCA -- redraw to show the current 5-MCP "
     "topology.",
     "doc-vs-code drift; carried in audit reports across multiple weeks",
     "CLAUDE.md committed with current content; 2 architecture PNGs "
     "replaced with current diagrams; audit report's doc-drift list "
     "clears these two items",
     24, None),

    # S4-HF-01 (item 25 in sprint-history.html ranked list) — added to the
    # generator 2026-05-21 so it survives regen. Originally added directly to
    # Sprint4-additions.csv 2026-05-20 (commit a92e447) but never made it
    # into the generator script.
    ("S4-HF-01",
     "Widen bounded-agency trigger to low-confidence + clamp-fired verdicts (not just data_starved)",
     "To Do", "High", EPIC9_ID, "(no P-number -- surfaced 2026-05-20 chat)", "3",
     "Widen the bounded-agency 6-tool retry trigger so the system iterates "
     "on get_trace / prometheus.query / loki.query_range itself instead of "
     "emitting hint text via clamp_actions.py:diagnostic_steps_for_clamp("
     "'Open Jaeger and inspect the slowest trace...').\n\n"
     "Acceptance criteria:\n"
     "- Widen gate in app/pipeline.py:453-456 (should_retry_for_quality). "
     "New condition: data_starved OR (first_pass_confidence < 0.55 AND F-4 "
     "clamp fired) OR (suggested_actions == [] AND verdict in {dismiss, "
     "escalate})\n"
     "- Per-alert-family tool steering in agency prompt (extend "
     "TOOLS_DESCRIPTION at bounded_agency.py:98): latency-family -> "
     "jaeger.get_traces + prometheus.query range; resource-family (PodHigh*, "
     "*MemoryUsage, *CpuUsage) -> prometheus.query topk + jaeger.get_traces; "
     "availability -> prometheus.query on up{} + loki.query_range\n"
     "- Cost ceiling preserved: max 1 extra LLM+tool iteration per alert\n"
     "- Metric: existing triage_bounded_agency_invocations_total gains a "
     "'trigger' label with values data_starved | low_confidence | "
     "empty_actions\n"
     "- New setting triage_low_confidence_retry_enabled (default True) -- "
     "killable independent of triage_bounded_agency_enabled\n"
     "- Tests: extend tests/test_bounded_agency.py with 3 new fixtures (one "
     "per family) asserting trigger label + tool whitelist matches family\n\n"
     "Out of scope: Tier 3 hypothesis-tree state (multi-tool loops -- "
     "separate story S4-CR-03). This is the cheap widen-the-gate fix, not "
     "the deferred agentic rewrite.\n\n"
     "Files touched: app/pipeline.py:443-456 (trigger), "
     "app/bounded_agency.py:98 (TOOLS_DESCRIPTION family hints), "
     "app/metrics.py (trigger label), app/config.py (new flag), "
     "tests/test_bounded_agency.py.",
     "PodHighMemoryUsage RCA on 2026-05-20 was clamped to 0.40 confidence; "
     "F-4 clamp fired; clamp_actions populated diagnostic verbs telling the "
     "operator to investigate via Jaeger. The system already has Jaeger/"
     "Prometheus/Loki access via the 6-tool whitelist in "
     "app/bounded_agency.py:88-95 -- the retry just never fires for memory/"
     "cpu alerts because they don't reach data_starved, they reach "
     "low-confidence-but-non-empty.",
     "Replay the 2026-05-20 PodHighMemoryUsage decision through the patched "
     "pipeline. New RCA must cite at least one concrete span line (from "
     "jaeger.get_traces) OR a per-pod topk row (from prometheus.query), NOT "
     "just diagnostic_steps_for_clamp's hint text. Tier 0 clamp + "
     "diagnostic_steps remain the safety net for retries that still fail.",
     25, None),
]


# EPIC12 stories live in their own ID band (201+) to keep the EPIC9/10/11
# story band (103-127) reserved for follow-on stories under the original
# three themed epics + Sprint-3 carry-row backfill (128-133 per
# SESSION_HANDOFF.md §A). Predictive items were added 2026-05-21.
STORIES_PRED = [
    ("S4-PRED-01",
     "Detective-signals dashboard tab -- aggregate Drain3/sigma/recurrence into one early-warning surface",
     "To Do", "Medium", EPIC12_ID, "P-detective", "1",
     "Add a /dashboard/early-warning tab surfacing four panels of "
     "pre-alert signal already in the system: "
     "(1) Drain3 template novelty per service (recent new templates from "
     "/drain3/stats top_new_patterns_per_service); "
     "(2) entity-baseline sigma-claims from recent decisions (context "
     "pack injections of 'Xsigma above SERVICE 7d baseline' from "
     "entity_baselines.py); "
     "(3) adaptive-threshold widened-but-not-fired ratio (US-5.4 rules "
     "that crossed adaptive baseline but didn't reach the static-threshold "
     "floor); "
     "(4) recurrence-gate fires and force-escalates (US-5.8) per-rule "
     "cumulative counts from triage_recurrence_*_total counters. "
     "Zero new MCP routes, zero new data sources -- pulls from "
     "/drain3/stats + /metrics + recent /decisions. ~3 hours of HTML/JS in "
     "app/main.py near the existing /dashboard route.",
     "Detective signals already feed the LLM at fire-time but aren't "
     "surfaced to operators directly; surfacing them as a tab means "
     "operators can spot building trends before an alert fires. The "
     "'detective signals' framing surfaced 2026-05-20 EOD chat as the "
     "zero-new-code reframe of the predictive question.",
     "4 panels render with live data from existing endpoints (/drain3/stats "
     "+ /metrics + recent /decisions); zero new MCP routes (MCP-invariant "
     "lint stays clean); tab is linked from /dashboard navigation; existing "
     "dashboard tests still green",
     26, None),
    ("S4-PRED-02",
     "Capacity-runway dashboard -- predict_linear() trajectories on disk, heap, CPU, JDBC pool",
     "To Do", "Medium", EPIC12_ID, "P-3", "2",
     "New Grafana dashboard using PromQL predict_linear() over a 6h "
     "trailing window for resource-saturation rates: container memory, "
     "container CPU, node disk free, JVM heap (if Spring actuator exposes "
     "it), JDBC pool usage (if exposed), Loki/Prometheus TSDB head series "
     "count. Single table panel with columns 'Resource | Current | "
     "Trajectory | Time-to-threshold', color-coded by urgency: "
     "<1h red, <24h amber, <7d yellow, >7d green. Pure PromQL -- no "
     "Python, no ML. Dashboard JSON committed to "
     "monitoring-project/roles/grafana/dashboards/. Cheapest+highest-impact "
     "predictive item: supervisor opens Grafana, sees the runway table, "
     "immediately understands the platform's forward-looking value.",
     "Today's platform is reactive -- supervisor sees no forward-looking "
     "signal until an alert fires. predict_linear is a Prometheus built-in "
     "that's been available since 2.0; using it for runway estimates is a "
     "near-free demo win.",
     "dashboard renders >=6 resources with live trajectory; a manually-"
     "induced disk-fill simulation produces a clear 'fills in N min' cell "
     "that updates in real-time; supervisor-demo dry-run completes without "
     "follow-up questions about 'is this real data'",
     27, None),
    ("S4-PRED-03",
     "Saturation-band entity baselines -- extend sigma-claims with 30-day percentile bands",
     "To Do", "Medium", EPIC12_ID, "P-5", "3",
     "Extend app/entity_baselines.py to compute percentile bands over a "
     "30-day rolling window in addition to sigma-claims. Inject 'entity "
     "novelty: top X% of values ever seen for this entity over 30 d' into "
     "the prompt context pack alongside the existing 'Xsigma above 7d "
     "baseline' claim. New PromQL queries via the prometheus-mcp using "
     "quantile_over_time(0.95, ...[30d]) and similar. Schema change to "
     "entity_baselines table: add percentile_band column. Additive -- the "
     "sigma-claim path keeps working, so prior RCAs in the corpus "
     "stay valid.",
     "sigma-claims are mathematically precise but operationally opaque "
     "('2.1sigma above baseline' doesn't communicate severity to a "
     "supervisor). Percentile band ('99.2 percentile') is immediately "
     "legible.",
     ">=5 recent RCAs cite percentile-band claim in prose; existing "
     "sigma-claim prose still works (additive, not replacement); MCP-"
     "invariant lint clean (new PromQL still routes through prometheus-mcp); "
     "entity_baselines.percentile_band column populated for >=2 services",
     28, None),
    ("S4-PRED-04",
     "Cascade predictor -- P(Y next 5min | X fired) from rca_history.db",
     "To Do", "Medium", EPIC12_ID, "P-2", "3",
     "Nightly APScheduler job builds the P(alert Y in next 5min | alert X "
     "fired now) transition matrix from rca_history.db over a 30-day "
     "trailing window with a minimum-support filter (>=5 co-occurrences). "
     "Surface via new MCP tool on rca_history_mcp: "
     "get_cascade_probabilities(alert_name, lookback_days=30, "
     "min_count=5) returning the top-K likely successors with their "
     "conditional probabilities. Pipeline injects 'Historical cascade: "
     "87% chance of TargetDown within 7 min when HighKongP95Latency fires' "
     "into the LLM context pack when the firing alert has a high-"
     "probability successor. Partners with S4-CR-01 (US-5.2 incident "
     "correlator): same data source, complementary purpose -- S4-CR-01 "
     "collapses concurrent clusters, S4-PRED-04 predicts the next cluster "
     "from a single fire.",
     "Current platform has no awareness of historical cascade dynamics. "
     "Real outages produce alert clusters with predictable transition "
     "patterns (4 MediumCpuUsage in 5 min + 4 TargetDown in 15 min on "
     "2026-05-19, treated independently); injecting cascade probability "
     "into the RCA helps the LLM reason about likely follow-ups.",
     ">=3 cascade patterns surface in real RCAs over 1 week of operation; "
     "nightly transition-matrix update job has run >=1 cycle and produced "
     "a transition_matrix.json artifact or DB rows; new MCP tool passes "
     "MCP-invariant lint; depends on S4-CR-01 shape (correlator's webhook "
     "fan-in informs which alert pairs to track)",
     29, None),
]


LABEL_FOR_PARENT = {
    EPIC9_ID: "Latency",
    EPIC10_ID: "RCA-Prose",
    EPIC11_ID: "Correlation",
    EPIC12_ID: "Predictive",
}


def _emit_story(work_id, story_tuple):
    code, summary_tail, status, priority, parent_id, p_tag, sp, body, evidence, gate, history_row, due_override = story_tuple
    return {
        "Work item Id": str(work_id),
        "Summary": f"{code}: {summary_tail}",
        "Work type": "Story",
        "Status": status,
        "Priority": priority,
        "Labels": LABEL_FOR_PARENT[parent_id],
        "Description": desc(body, p_tag, evidence, gate, history_row,
                            cross_ref=f"Cross-reference: sprint-history.html row {history_row}; "
                                      f"FYP report Chapter 11 table row {history_row}. "
                                      f"Story Points (bulk-edit post-import): {sp}."),
        "Parent": parent_id,
        "Reporter": USER,
        "Assignee": USER,
        "Due date": due_override if due_override else SPRINT_DUE,
    }


def main():
    rows = list(EPICS)

    # EPIC9/10/11 stories occupy the contiguous 103+ band.
    next_id = 103  # epics consumed 100, 101, 102
    for s in STORIES:
        rows.append(_emit_story(next_id, s))
        next_id += 1

    # EPIC12 stories live in the 201+ band (EPIC12 itself is at 200) so the
    # 103+ story-band stays free for follow-on stories under EPIC9/10/11
    # and the Sprint-3 carry-row backfill (128-133).
    pred_id = 201
    for s in STORIES_PRED:
        rows.append(_emit_story(pred_id, s))
        pred_id += 1

    with open("/root/jira/Sprint4-additions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    n_stories = len(STORIES) + len(STORIES_PRED)
    print(f"Wrote /root/jira/Sprint4-additions.csv with {len(rows)} rows "
          f"({len(EPICS)} epics + {n_stories} stories: "
          f"{len(STORIES)} in EPIC9/10/11 band + {len(STORIES_PRED)} in EPIC12 band).")
    total_sp = sum(int(s[6]) for s in (STORIES + STORIES_PRED) if s[6].isdigit())
    print(f"Total story points across {n_stories} stories: {total_sp} SP "
          f"(includes the 2 SP P2 backfill already Done).")


if __name__ == "__main__":
    main()
