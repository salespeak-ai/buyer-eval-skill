# Changelog

## 4.0.0: Evidence first

- **Quick Eval is the default.** One opening question at most, inferred criteria
  labeled as inferred, results in minutes. The previous workflow is Deep Eval,
  available on request.
- **Claims vs. Evidence is the centerpiece.** New evidence model: vendor claim,
  vendor evidence, independent evidence, buyer evidence. Statuses: Verified,
  Qualified, Contradicted, Unverified, Unknown.
- **Vendor AI agents are first-party sources.** Removed the rule that treated a
  vendor's Company Agent as authoritative, and the "evidence completeness"
  measure that rewarded vendors for having one. Having an agent never improves
  fit, confidence, or score.
- **New report structure:** What we found, criteria, claims vs. evidence, vendor
  assessment, what could change, questions we could not answer, demo questions.
  Numeric scores are Deep Eval only and appear lower in the report.
- **Challenge pass** before every final output.
- **HTML Decision Brief** rendered by `bin/render_report.py` (no dependencies).
- **Saved buyer context** now actually persists, via `bin/profile.py`.
- **Buyer evidence:** proposals, pricing, demo notes and similar can be included.
- **Modular methodology** under `references/`. `EVALUATION.md` is now a pointer.
- **Fixes:** `bin/track.py` crashed under Python 3.9 (macOS default), silently
  disabling telemetry; telemetry version now read from `VERSION`; skill name
  matches the install directory (`/buyer-eval-skill`); `BUYER_EVAL_DIR` override.
- **Telemetry:** new funnel fields (`mode`, `returning_user`, claim counts,
  `report_created`, `deep_eval_requested`). Privacy surface unchanged: no buyer
  text, no vendor answers, no claim text.
- **Removed the v3 evaluation gallery.** Its framing ("won by Company Agent
  vendor") contradicted the neutrality principle, and several entries stated
  unsourced facts about real companies. Archived at tag `v3.5.0`.
- README rewritten; examples now use clearly fictional vendors.

## 3.5.0
Vendor questions captured even without a Company Agent; discovery questions captured.

## 3.4.x
Optional telemetry for evaluation questions; privacy contact.

## 3.3
Salesforce AgentExchange / AppExchange as a conditional research source.

## 3.2
Source reliability tiers (T1-T4) for research data.

## 3.1
Domain-expert discovery questions; demo prep questions.

## 3.0
Evidence completeness, claims vs. evidence, hidden risks, TL;DR first, reusable buyer context.

## 2.x
Frontdoor REST API, environment matrix, redesign around a minimal entry point.

## 1.0
Initial version.
