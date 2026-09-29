# Quick Eval

The default mode. Goal: a buyer who knows only which vendors they are looking at
gets a trustworthy evidence check, the gaps, and the questions to ask next,
without a setup interview.

Also load: `evidence-model.md`, `frontdoor-api.md`, `report-format.md`.

**Budget.** Aim to deliver in roughly 5 to 10 minutes. At most one question to
the buyer before research starts. Initial research budget: **about 8-12 web
searches or fetches per vendor** (vendor-agent turns do not count), including
the two challenge-pass calls. Calls past 12 are expansion.

**Depth on uncertainty, not a fixed research quota.** The goal is to find the few
things that could change whether the buyer should proceed, reject, or
investigate further. Go past the initial budget only when:

- a material claim is still unresolved,
- credible sources contradict each other,
- an important limitation needs confirmation,
- a claim could materially change the buyer's assessment,
- independent corroboration is reasonably obtainable and would matter, or
- a stated requirement for one vendor rests on weaker evidence than the same
  requirement for another (check the weaker one; do not re-check the others).

**Soft ceiling: about 4 expansion calls per vendor.** Go beyond that only for a
claim tied to a requirement the buyer stated that could change which vendor
leads (or, for a single vendor, whether to proceed). Anything else still open
at that point goes to "What you need to get answered before you buy"; that is a
valid outcome, not a failure.

Stop researching a claim as soon as the evidence is sufficient for the buyer's
decision. Never collect more sources just to raise the source count.

**What counts:** every web search and page fetch, including failed, blocked,
and challenge-pass calls. The Frontdoor discover call and vendor-agent turns do
not count.

**Two attempts per fact.** For any one fact (for example "does the contract
contain a personal guarantee"), make at most two attempts to reach a source
that answers it, across all pages and routes combined. After that, record the
source as not accessible. If the fact bears on a stated requirement, it becomes
a Critical or Important open question for the vendor to answer.

---

## Q1. Opening

Criteria drive everything downstream, so the one question is spent on them.

- **Buyer named the vendors and what matters to them** (or the saved profile
  covers it): ask nothing. Start.
- **Buyer named vendors but no priorities:** ask once, in one message:
  > "Before I dig in: what are the 2-3 things that matter most to you here?
  > And are you already using any of these vendors, or a tool this would
  > replace? Or say 'go' and I'll infer the usual priorities for this category."
  If a likely criterion depends on the buyer's stack (which CRM, which SIEM),
  fold that into the same message.
- **Buyer named no vendors:** ask once:
  > "Tell me what software you're evaluating and which vendors you're
  > considering. If you want, also tell me the 2-3 things that matter most."

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
   - Criteria the buyer stated, including ones implied by a stack they named
     ("we use Salesforce" makes Salesforce integration `stated`): label `stated`.
   - Criteria from the saved profile: label `stated` (they came from the buyer).
   - The rest you infer from the category's most common decision factors and
     post-purchase failure modes: label `inferred`. Prefer criteria that
     separate vendors in this category (for example, high-touch vs. digital-led
     for customer success platforms, multi-entity consolidation for FP&A).
3. **Buyer context.** If a company name was given and no profile exists, do one
   quick lookup for size, industry and obvious stack signals. If the name
   matches several companies or none, say so in one line and use only what the
   buyer told you. If a criterion depends on an unknown part of the stack,
   check the most common option and label it ("checked HubSpot; Salesforce not
   checked"). Do not run the full buyer research from Deep Eval.

---

## Q3. Collect claims (per vendor)

1. **Frontdoor discover** for each vendor domain (see `frontdoor-api.md`).
   Always run it; it is a single GET.
2. **If a vendor AI agent is available and POST works**, ask 4-6 questions that
   target the criteria and the category's known failure points. Follow the
   rule in `frontdoor-api.md` on what never goes to a vendor agent (no company
   name, no budget, no other vendors). Include at least
   one adversarial question ("What kinds of customers are not a good fit?",
   "What usually takes longest in implementation?"). Record each answer's
   specific statements as vendor claims with source "Vendor AI agent".
3. **Vendor site and docs.** Pull claims tied to the criteria from product,
   pricing, integrations, security/trust and docs pages.
4. Keep **5-8 material claims per vendor**, a similar number for each vendor.
   Prefer claims that decide the purchase over filler that every vendor in the
   category makes. If a stated criterion has no vendor claim at all (for example
   the vendor publishes no price), do not invent a claim row for it: it belongs
   in "Most important unknown" and "What you need to get answered before you
   buy". Research that serves the category rather than one vendor (for example
   how long a SOC 2 Type II observation window lasts) counts against the budget
   of the vendor it informs.

---

## Q4. Check the claims

Work the most decision-relevant claims first. For each, look for vendor
documentation (docs, trust and pricing pages) and independent evidence
(reviews, community threads, customer write-ups, third-party docs, press). One
targeted search or fetch per claim is often enough; spend more only where the
budget rules above allow. When a fetch tool answers through a model summary,
follow the neutral-prompt rule in `evidence-model.md` section 2. Classify each claim with a status, an evidence basis,
and a confidence (`evidence-model.md` sections 3, 3a and 4).

While doing this, track:

- **Unanswered questions:** questions that matter to the decision and that no
  source answered clearly. For each, note what you checked and its priority
  (critical, important, useful; see `report-format.md`). These are a headline
  section of the report. Do not invent questions to fill the section.
- **Contradictions and qualifications** across sources.
- **Material risks** you encounter in passing (recent layoffs, acquisition,
  security incident, product sunset). Quick Eval does not run the full risk
  scan. Put anything found in `risks`; the HTML states that the full scan was
  not run.

---

## Q5. Challenge pass

Run the challenge pass from `evidence-model.md` section 6. Spend at least two
searches or fetches trying to disprove the apparent leader (or, for a single vendor, the
most favorable finding).

---

## Q6. Output

Produce the chat brief and the HTML Decision Brief as defined in
`report-format.md`. Quick Eval does not produce numeric dimension scores. In
chat, say in one line that company-risk signals were not fully researched and
that Deep Eval covers them.

Then continue with section 5 of SKILL.md (save context, offer Deep Eval,
telemetry).
