# Changelog

## 4.1.1

- **Soft expansion ceiling:** about 4 expansion calls per vendor after the
  initial 8-12 (which now includes the two challenge-pass calls). More only for
  a stated-requirement claim that could change which vendor leads; otherwise
  the question goes to "What you need to get answered before you buy".
- **Two attempts per fact**, across all pages and routes, then record it as not
  accessible (was one retry per page).
- **Neutral fetch prompts:** ask fetch tools to quote page text on a topic,
  never to confirm a specific fact. Testing caught a fetch summarizer echoing
  the question back as a vendor claim. Facts that decide a stated requirement
  rest on quoted text only.

## 4.1.0: Refinement

- **Faster Quick Eval.** Initial research budget is about 8-12 searches or
  fetches per vendor (was 15-20). Research goes deeper only around material
  uncertainty: unresolved claims, contradictions, limitations that need
  confirming. "Depth on uncertainty, not a fixed research quota."
- **Evidence basis on every claim** (vendor claim only, vendor documentation,
  vendor + independent evidence, independent evidence, buyer-provided evidence,
  mixed evidence), shown in chat and HTML. A claim resting on a vendor claim
  alone, including a vendor AI agent answer, can never render as Verified; the
  renderer enforces this.
- **Claims table** is now Claim | Status | Evidence basis | What the evidence says.
- **Single-vendor reports** use "Vendor assessment", "Key strength" and "Key
  concern" instead of comparative wording.
- **"What you need to get answered before you buy"** replaces "Questions we
  still could not answer", ordered by priority: Critical, Important, Useful.
- JSON: `claims[].basis` replaces `evidence_type`; `unanswered[].priority`
  replaces `material`. Old reports still render.

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
- **Buyer privacy with vendor agents:** the buyer's company name, budget, other
  vendors under evaluation, and document contents are never sent to a vendor AI
  agent. (Testing showed the v3 tailoring instructions sent a budget ceiling to
  a vendor's sales agent.)
- **Competitor content** is its own evidence type and can never verify or
  contradict a claim. Search snippets and AI search summaries are leads, not
  evidence; blocked sources are recorded as gaps.
- **Deep Eval** asks the buyer two consolidated messages instead of five, and
  invites buyer evidence up front.
- **Modular methodology** under `references/`. `EVALUATION.md` is now a pointer.
- **Update check** only offers strictly newer versions (it previously offered
  any version that differed, including downgrades).
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
