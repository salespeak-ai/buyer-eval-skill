# Report Format

Every evaluation produces two things with the same content order:

1. A **chat brief** (markdown) for the person who ran it.
2. An **HTML Decision Brief** for the people they forward it to, rendered from a
   JSON file by `bin/render_report.py`.

Write for a buying committee: a CFO, a security lead, and a VP who did not run
the eval. Plain language, no marketing voice, no hype words, no emoji. Every
factual sentence either cites a source or is phrased as the buyer's stated input.

---

## Order (chat and HTML)

1. **What we found.** Counts of material claims investigated, verified,
   qualified, contradicted, unverified, unknown. Then three lines:
   - Most important finding
   - Most important remaining unknown
   - Most important question to ask next
2. **Evaluation criteria.** Each marked stated, inferred, or discovered.
3. **Claims vs. Evidence.** The central table. Grouped by vendor for multi-vendor
   runs. Columns: Claim | Source of claim | Evidence | Status | Confidence.
   Keep each cell to one or two sentences.
4. **Where each vendor appears strongest.** Per vendor: fit, evidence
   confidence, counts of contradictions and unknowns, strongest fit, biggest
   concern, and two or three sentences relative to the buyer's criteria. No
   sweeping statements without evidence.
5. **What could change the evaluation.** Specific unresolved facts and how each
   would move the picture. ("If Vendor A shows custom-object sync works
   bidirectionally without professional services, its fit on the Salesforce
   criterion moves from Moderate to Strong.")
6. **Questions we still could not answer.** For each: the question, why it
   matters, what was checked, which vendor should answer, and whether it could
   change the decision.
7. **Questions for the next demo.** Per vendor, 3-5 questions derived from
   unverified claims, contradictions, and unknowns, each with what to listen for.
8. **What changed during review** (only if the challenge pass changed something).
9. **Deep Eval only:** risk signals, dimension scores, per-vendor detail.
10. **Sources.** Numbered, each typed as vendor, independent, or buyer.
11. **Method note.** Rendered automatically in HTML.

In chat, sections 1-7 carry the value. You may shorten sources in chat to the
ones cited in the table and point to the HTML for the full list.

Do not open with a recommendation that outruns the evidence. If one vendor is
clearly the better fit on verified evidence, say so in "Most important finding".
If not, say what would decide it.

---

## Report JSON (input to `bin/render_report.py`)

Write valid JSON (UTF-8). Unknown keys are ignored; missing optional keys hide
their section. Counts in "What we found" are computed by the renderer from
`claims`, so do not supply them.

```json
{
  "title": "Vendor A vs Vendor B Buyer Evaluation",
  "buyer": "Acme Corp",
  "date": "2026-09-28",
  "mode": "quick",
  "category": "Customer success platforms",
  "findings": {
    "key_finding": "Vendor A is the stronger verified fit on Salesforce depth; Vendor B's implementation claim is contradicted.",
    "key_unknown": "Whether either vendor includes SCIM in the plan you would buy.",
    "next_question": "Ask Vendor B for two references your size who went live in under 8 weeks."
  },
  "criteria": [
    {"text": "Bidirectional Salesforce sync incl. custom objects", "origin": "stated"},
    {"text": "Implementation under 90 days", "origin": "inferred"}
  ],
  "vendors": [
    {
      "name": "Vendor A",
      "domain": "vendora.com",
      "fit": "Strong",
      "confidence": "Medium",
      "strongest": "Salesforce integration depth",
      "concern": "Pricing is not public; typical packaging unclear",
      "summary": "Two or three sentences relative to the buyer's criteria.",
      "agent_channel": "none"
    }
  ],
  "claims": [
    {
      "vendor": "Vendor A",
      "claim": "Typical implementation takes 6 weeks",
      "claim_source": "Vendor website (implementation page)",
      "evidence": "No independent accounts found; one G2 review mentions 3 months.",
      "evidence_type": "independent",
      "status": "Unverified",
      "confidence": "Low",
      "sources": [3, 7]
    }
  ],
  "could_change": [
    "If Vendor A shows custom-object sync without professional services, its Salesforce fit moves from Moderate to Strong."
  ],
  "unanswered": [
    {
      "question": "Is SCIM included in the Enterprise plan?",
      "why": "Your security team requires automated deprovisioning.",
      "checked": "Pricing page, docs, vendor AI agent, G2",
      "vendor": "Vendor A",
      "material": true
    }
  ],
  "demo_questions": [
    {"vendor": "Vendor A", "question": "Show a custom object syncing both ways live.", "listen_for": "Whether it needs a middleware or services engagement."}
  ],
  "review_changes": ["Vendor B's implementation claim moved to Contradicted after two customer accounts described 4-6 months."],
  "risks": [
    {"vendor": "Vendor B", "signal": "Acquired in 2025; roadmap integration announced", "source": 9}
  ],
  "scores": [
    {"vendor": "Vendor A", "dimension": "Product Fit", "weight": 25, "score": 4, "note": "One-line reason"}
  ],
  "sources": [
    {"id": 3, "title": "Vendor A implementation page", "url": "https://...", "type": "vendor"},
    {"id": 7, "title": "G2 review, mid-market user, Jun 2026", "url": "https://...", "type": "independent"}
  ]
}
```

Field values:

- `mode`: `quick` | `deep`
- `criteria[].origin`: `stated` | `inferred` | `discovered`
- `vendors[].fit`: `Strong` | `Moderate` | `Weak` | `Unclear`
- `vendors[].confidence`, `claims[].confidence`: `High` | `Medium` | `Low`
- `vendors[].agent_channel`: `conversation` | `none` | `failed` | `unreachable`
- `claims[].status`: `Verified` | `Qualified` | `Contradicted` | `Unverified` | `Unknown`
- `claims[].evidence_type`: the strongest evidence that decided the status: `independent` | `buyer` | `vendor` (vendor evidence such as docs or pricing pages) | `none` (only vendor claims, or competitor content)
- `claims[].claim_source`: free text naming the first-party source, for example "Vendor website", "Vendor AI agent", "Vendor docs", "Proposal (buyer-provided)"
- `sources[].type`: `vendor` (vendor claims and vendor evidence, including the vendor AI agent) | `independent` | `competitor` | `buyer`
- `unanswered[].vendor`: a vendor name, `Both` / `All vendors`, or `Your team` for questions only the buyer can answer
- `risks`: anything found; in Quick Eval the HTML adds a note that the full risk scan was not run
- `scores`: Deep Eval only, 1-5 integers; use `null` for GAP
- `buyer`: company name, or a descriptor such as "120-person B2B SaaS company" if no name was given. Never a person's name.

Render:

```bash
python3 "$_BEVAL_DIR/bin/render_report.py" report.json            # -> ~/buyer-eval-reports/<slug>-<date>.html
python3 "$_BEVAL_DIR/bin/render_report.py" report.json --out x.html
```

The renderer copies the JSON next to the HTML so a later Deep Eval or update
can start from it.
