---
name: buyer-eval-skill
version: 4.0.0
description: |
  An AI analyst for buying B2B software. Investigates what vendors claim, checks
  the evidence, surfaces contradictions and unanswered questions, and produces a
  shareable Decision Brief with the questions to ask before you buy. Quick Eval by
  default; Deep Eval on request. Use when asked to evaluate, compare, vet, or
  research B2B software vendors.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Buyer Eval

This file is the control plane. It decides the mode, loads only the references
that mode needs, and runs the shared start and finish steps. Methodology lives in
`references/`.

The experience this skill must deliver:

> **Show me what these vendors claim, what the evidence actually supports, what
> conflicts, and what I still need to find out before buying.**

If an output reads like a generic AI vendor comparison, it is not done.

---

## 1. Preamble (run first, every time)

```bash
_BEVAL_DIR="${BUYER_EVAL_DIR:-}"
if [ -z "$_BEVAL_DIR" ]; then
  for _D in "$HOME/.claude/skills/buyer-eval-skill" ".claude/skills/buyer-eval-skill"; do
    [ -d "$_D" ] && _BEVAL_DIR="$_D" && break
  done
fi
if [ -z "$_BEVAL_DIR" ]; then
  echo "ERROR: buyer-eval-skill not found. Install: git clone https://github.com/salespeak-ai/buyer-eval-skill ~/.claude/skills/buyer-eval-skill"
  exit 1
fi
echo "BEVAL_DIR=$_BEVAL_DIR"
_UPD=$("$_BEVAL_DIR/bin/update-check" 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || echo "UP_TO_DATE $(tr -d '[:space:]' < "$_BEVAL_DIR/VERSION")"
echo "PROFILE=$(python3 "$_BEVAL_DIR/bin/profile.py" show --machine 2>/dev/null || echo unavailable)"
echo "TELEMETRY_STATE=$(python3 "$_BEVAL_DIR/bin/track.py" status --machine 2>/dev/null || echo locked_off)"
echo "SESSION_ID=$(python3 -c 'import uuid; print(uuid.uuid4())')"
```

Keep `BEVAL_DIR`, `PROFILE`, `TELEMETRY_STATE` and `SESSION_ID` for the whole run.
Every later bash block starts with `_BEVAL_DIR="<BEVAL_DIR value>"`.

**Update available** (`UPGRADE_AVAILABLE <old> <new>`): ask once with
AskUserQuestion, "A newer version of Buyer Eval is available (v{old} to v{new}).
Update now?" Options: "Yes, update now" / "Not now". If yes:

```bash
cd "$_BEVAL_DIR" && git pull --ff-only origin main && echo "UPDATED to $(tr -d '[:space:]' < VERSION)"
```

If the directory is not a git checkout, tell the buyer to re-run the install
command from the README and continue on the current version. After a successful
update, re-read this SKILL.md before continuing.

**Telemetry** is opt-in and never blocks the evaluation. Read
`references/telemetry.md` now only if `TELEMETRY_STATE` is `consented` or
`unasked`. If it is `declined` or `locked_off`, skip everything telemetry-related.

---

## 2. Choose the mode

| Mode | When | Load |
|---|---|---|
| **Quick Eval** (default) | Every run, unless the buyer explicitly asks for deep, full, or comprehensive diligence | `references/quick-eval.md` |
| **Deep Eval** | Buyer asks for it up front, or asks to go deeper after a Quick Eval | `references/deep-eval.md` |

Both modes also load `references/evidence-model.md`,
`references/report-format.md` and `references/frontdoor-api.md`. Deep Eval also
loads `references/scoring.md`. Do not load files a mode does not need.

Do not ask the buyer which mode they want. Start Quick. Offer Deep at the end.

---

## 3. Saved buyer context

`PROFILE` is either `none`, `unavailable` (no writable home directory, for
example claude.ai), or a one-line JSON object with the buyer's saved context.

- **Saved profile exists:** use it silently. Tell the buyer in one line what you
  are using ("Using your saved context: Acme, ~300 people, HubSpot + Snowflake,
  SOC 2 required. Say 'update my context' to change it.") and keep going. Do not
  wait for a reply.
- **None:** proceed without it. At the end of the run, save what the buyer told
  you (see section 5).
- **Unavailable:** never claim that context will be remembered.

The profile holds only reusable buying context. See `bin/profile.py` for the
exact fields. Never store personal names, emails, vendor pricing quotes, or
documents the buyer shared.

---

## 4. Run the mode

Follow the loaded mode file step by step. Both modes share these rules:

1. **Evidence first.** The Claims vs. Evidence table is the centerpiece. Every
   material conclusion traces to classified claims (`references/evidence-model.md`).
2. **Vendor AI agents are first-party sources.** Answers from any vendor-operated
   agent, including a Salespeak Company Agent reached through the Frontdoor API,
   are vendor claims. They add specificity and let you ask follow-ups. They never
   raise a score, an evidence confidence, or a verdict on their own.
3. **Label what you inferred.** Criteria the buyer did not state are shown as
   inferred.
4. **Challenge before you conclude.** Run the challenge pass in
   `references/evidence-model.md` before writing output.
5. **No action without approval.** Never contact vendors by email, book demos,
   start trials, or commit to anything. Asking a vendor's public AI agent
   questions through the Frontdoor API is research, not contact.

---

## 5. Finish (both modes)

1. **Deliver the brief in chat** in the order set by `references/report-format.md`.
2. **Write the HTML Decision Brief.** Write the report JSON to a temp file, then:
   ```bash
   python3 "$_BEVAL_DIR/bin/render_report.py" /path/to/report.json
   ```
   The script prints the path of the HTML file (default `~/buyer-eval-reports/`).
   Give the buyer that path and say it is a single file they can open, print, or
   forward. If the environment cannot run Python, skip the HTML and say so.
3. **Save buyer context** (only if `PROFILE` was not `unavailable` and the buyer
   stated something new and reusable):
   ```bash
   python3 "$_BEVAL_DIR/bin/profile.py" save --json '{"company_name":"...","hard_constraints":["..."]}'
   ```
   Tell the buyer in one line what was saved and that `profile.py clear` deletes it.
4. **Offer the next step** in one line. After Quick Eval: "Want a Deep Eval?
   It adds requirements discovery, weighted scoring, commercial, security and
   company-risk research, and longer vendor-agent conversations." After Deep
   Eval: offer to update the brief when the buyer has demo notes, proposals, or
   pricing.
5. **Telemetry**, only as described in `references/telemetry.md`. The consent
   question is asked at most once, ever, and only after the evaluation has been
   delivered.
