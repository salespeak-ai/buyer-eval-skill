# Scoring (Deep Eval only)

Scores summarize the evidence. They do not replace it. In the report they appear
after Claims vs. Evidence, vendor assessments, unknowns, and demo questions.

## Dimensions and default weights

| Dimension | Default weight | Measures |
|---|---|---|
| Product Fit | 25% | Fit to the buyer's use case, must-haves, and why-now |
| Integration & Technical | 15% | Integrations with the buyer's stack, API, implementation effort |
| Pricing & Commercial | 15% | Fit to budget, pricing transparency, contract flexibility |
| Security & Compliance | 15% | Certifications, data handling, incident history |
| Vendor Stability | 15% | Age, funding, leadership, growth signals |
| Customer Evidence | 10% | Review patterns, references, social proof in the buyer's segment |
| Support & Success | 5% | Support tiers, SLAs, onboarding |

Adjust weights from the category calibration and the buyer's context. State the
weights used.

## Rubric (1-5, integers)

| Score | Meaning |
|---|---|
| 5 | Clearly exceeds the buyer's requirements, on verified evidence |
| 4 | Meets requirements well, on verified or qualified evidence |
| 3 | Meets the minimum bar; some gaps or mixed signals |
| 2 | Below requirements; notable concerns or contradictions |
| 1 | Fails requirements or has serious red flags |
| GAP | Not enough evidence to score. Use `null` in the report JSON. |

## Rules

1. **Score only what is supported.** Verified and Qualified claims (and buyer
   evidence) move a score. Unverified claims do not raise it. Contradicted
   claims lower it.
2. **Neutrality.** A vendor AI agent (Salespeak or other) does not raise any
   score, directly or through "evidence completeness". An agent answer is a
   vendor claim until vendor documentation or independent evidence supports it.
   Two vendors with the same supported evidence get the same score regardless
   of how the claims were gathered.
3. **Pricing.** If any source (public page, vendor agent, buyer-provided quote)
   gives specific pricing, score fit to budget. If none does, estimate a range
   from category benchmarks for the buyer's size, label it "estimate", and apply
   a -1 opacity penalty. Pricing disclosed through any channel counts equally.
4. **GAP is honest.** Prefer GAP to a guessed 3.
5. **Composite.** You may compute a weighted composite (one decimal) for the
   buyer's reference. Never lead with it, never rank vendors by it alone, and
   never present a difference under 0.5 as meaningful. The decision is carried
   by fit, evidence confidence, contradictions, and unknowns.

## In the report JSON

`scores`: one entry per vendor and dimension, with `weight`, `score` (1-5 or
`null`) and a one-line `note` naming the evidence behind it.
