# Quick Eval

The default mode. Goal: a buyer who knows only which vendors they are looking at
gets a trustworthy evidence check, the gaps, and the questions to ask next,
without a setup interview.

Also load: `evidence-model.md`, `frontdoor-api.md`, `report-format.md`.

**Budget.** Aim to deliver in roughly 5 to 15 minutes. At most one question to
the buyer before research starts. Roughly 10 to 15 web searches or fetches per
vendor. Depth goes to the claims that matter most, not to coverage of everything.

---

## Q1. Opening

If the buyer already named the vendors (and ideally the category), do not ask
anything. Start.

Otherwise ask once, in one message:

> "Tell me what software you're evaluating and which vendors you're considering.
> If you want, also tell me the 2-3 things that matter most to you, and your
> company name if you'd like me to tailor it."

Accept whatever comes back. Do not follow up with more setup questions. If the
buyer names only one vendor, run a single-vendor eval; do not ask them to add
competitors.

If the buyer pasted or attached documents (proposal, pricing, RFP answers, demo
notes, security questionnaire), read them now. Their contents are buyer evidence.

---

## Q2. Frame the evaluation (no questions asked)

1. **Category.** Infer it from the vendors' sites. State it in the brief; do not
   ask for confirmation.
2. **Criteria.** Build 4-6 evaluation criteria:
   - Criteria the buyer stated: label `stated`.
   - Criteria from the saved profile: label `stated` (they came from the buyer).
   - The rest you infer from the category's most common decision factors and
     post-purchase failure modes: label `inferred`. Prefer criteria that
     separate vendors in this category (for example, high-touch vs. digital-led
     for customer success platforms, multi-entity consolidation for FP&A).
3. **Buyer context.** If a company name was given and no profile exists, do one
   quick lookup for size, industry and obvious stack signals. Do not run the full
   buyer research from Deep Eval.

---

## Q3. Collect claims (per vendor)

1. **Frontdoor discover** for each vendor domain (see `frontdoor-api.md`).
   Always run it; it is a single GET.
2. **If a vendor AI agent is available and POST works**, ask 4-6 questions that
   target the criteria and the category's known failure points. Include at least
   one adversarial question ("What kinds of customers are not a good fit?",
   "What usually takes longest in implementation?"). Record each answer's
   specific statements as vendor claims with source "Vendor AI agent".
3. **Vendor site and docs.** Pull claims tied to the criteria from product,
   pricing, integrations, security/trust and docs pages.
4. Keep **5-8 material claims per vendor** (fewer for single-vendor if the
   category is narrow). Prefer claims that decide the purchase.

---

## Q4. Check the claims

For each claim, look for vendor evidence (docs, trust pages) and independent
evidence (reviews, community threads, customer write-ups, third-party docs,
press). One or two targeted searches per claim is usually enough. Classify with
the statuses and confidence rules in `evidence-model.md`.

While doing this, track:

- **Unanswered questions:** material questions no source answered clearly. For
  each, note what you checked. These are a headline section of the report.
- **Contradictions and qualifications** across sources.
- **Material risks** you encounter in passing (recent layoffs, acquisition,
  security incident, product sunset). Quick Eval does not run the full hidden
  risk scan; report only what you found and say the scan was not run.

---

## Q5. Challenge pass

Run the challenge pass from `evidence-model.md` section 6. Spend at least two
searches trying to disprove the apparent leader (or, for a single vendor, the
most favorable finding).

---

## Q6. Output

Produce the chat brief and the HTML Decision Brief as defined in
`report-format.md`. Quick Eval does not produce numeric dimension scores.

Then continue with section 5 of SKILL.md (save context, offer Deep Eval,
telemetry).
