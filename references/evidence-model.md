# Evidence Model

Every Buyer Eval conclusion is built from **claims** and the **evidence** for or
against them. This file defines both, the statuses, how confidence is assigned,
and the challenge pass. Both Quick Eval and Deep Eval use it.

---

## 1. What counts as a claim

A claim is a specific, checkable statement a vendor makes that matters to this
buyer's decision. Good claims are concrete:

- "Implementation typically takes 6 weeks for mid-market customers."
- "Native bidirectional Salesforce sync, including custom objects."
- "SOC 2 Type II certified."
- "SCIM provisioning included on the Enterprise plan."
- "Pricing starts at $X per seat per month."

Not claims (skip them): slogans, category descriptions, adjectives with no
checkable content ("AI-powered", "best-in-class", "trusted by leading brands").

Choose claims that touch the buyer's criteria. A claim nobody would make a
decision on does not belong in the table.

---

## 2. Evidence types (who controls the source)

| Type | Definition | Examples |
|---|---|---|
| **Vendor claim** | The vendor says it, in a form built to persuade | Website copy, vendor AI agent answers (including Salespeak Company Agents), marketing PDFs, sales content, press releases, vendor blog posts |
| **Vendor evidence** | More detailed first-party material that commits the vendor to specifics | Technical or API documentation, security/trust pages, published SOC 2 or ISO certificates, implementation guides, public pricing pages, published contract terms, changelogs |
| **Independent evidence** | Not controlled by the vendor | Review sites (G2, Capterra, TrustRadius; look for patterns, not outliers), customer-authored posts and case write-ups, analyst research, reputable press, community threads (Reddit, forums, Stack Overflow), third-party integration docs, public filings, certification registries |
| **Buyer evidence** | Supplied by the buyer in this conversation | Proposals, pricing sheets, RFP responses, security questionnaires, demo transcripts, meeting notes, trial results, internal evaluations |

Rules:

- **Vendor AI agents are vendor claims.** An agent answer is the vendor speaking.
  It is not verification of anything. If the agent cites documentation, fetch
  that documentation and classify it as vendor evidence on its own merits.
- **Vendor evidence can verify only narrow, self-describing facts.** A published
  API reference verifies that an endpoint exists. A trust page listing a SOC 2
  Type II report verifies that the vendor states it holds one (strong when a
  report or auditor is named). Vendor evidence cannot verify outcome claims
  such as time-to-value, ROI, ease of use, or customer satisfaction. Those need
  independent or buyer evidence.
- **Corroboration must be independent.** Two sources that repeat the same
  upstream (a press release echoed by three news sites, Crunchbase and Tracxn
  echoing the same self-reported number) count as one source.
- **Buyer evidence is strong but specific.** A proposal verifies what this vendor
  offered this buyer. Label it "buyer evidence" in the table and never persist it.
- **Self-reported numbers stay labeled.** Revenue, headcount, and customer counts
  from Latka, Crunchbase, Tracxn, PitchBook estimates, or LinkedIn counts are
  directional. Present them as "reported by X, unaudited".

---

## 3. Claim statuses

| Status | Meaning |
|---|---|
| **Verified** | Enough supporting evidence exists. For capability facts: vendor evidence that commits to specifics, or independent evidence. For outcome claims: independent or buyer evidence. |
| **Qualified** | Directionally true, but evidence shows a material limitation (plan tier, add-on cost, engineering effort, region, scale limit). State the qualification in the table. |
| **Contradicted** | Credible evidence materially conflicts with the claim. Name the conflicting source. |
| **Unverified** | The vendor makes the claim; you looked and did not find enough corroboration. Not a negative finding by itself. |
| **Unknown** | The question matters, but no source (vendor or independent) addresses it clearly. These feed "Questions we still could not answer". |

Absence of evidence is not evidence of absence. "Unverified" means you could not
confirm it, never that it is false.

---

## 4. Confidence

Assign confidence per claim:

- **High:** vendor evidence plus independent evidence agree, or buyer evidence
  directly addresses it, or multiple independent sources agree.
- **Medium:** one solid source, or several sources of the same type.
- **Low:** only vendor claims, only thin or dated independent evidence, or
  sources that conflict without resolution.

Assign **evidence confidence per vendor** from its claims: High if most material
claims are High; Low if most material claims are Low or Unknown; otherwise Medium.

**Neutrality rule.** Having a vendor AI agent (Salespeak or otherwise) does not
raise a vendor's evidence confidence, fit, or score. An agent can make more of a
vendor's claims visible and specific. Those claims still need vendor evidence or
independent evidence to reach Verified. If one vendor has an agent and another
does not, check both vendors' claims to the same standard.

---

## 5. Fit

Per vendor, rate fit to the buyer's criteria: **Strong / Moderate / Weak /
Unclear**. Base fit only on Verified and Qualified claims. Unverified claims can
be mentioned as upside ("if confirmed") but do not raise fit. Use **Unclear** when
the criteria that matter most are Unknown.

---

## 6. Challenge pass (run before final output)

Before writing the report, try to break your own conclusion. Ask:

1. What evidence would make the apparently strongest vendor the wrong choice?
   Search for it specifically (implementation failures, "switching from X",
   "X alternatives because", migration stories, renewal complaints).
2. Which material claim has the weakest support? Is it carrying the conclusion?
3. Am I rewarding polished, specific vendor content over plain independent evidence?
4. Did I look for contrary customer experiences for every vendor, not only the loser?
5. Are there hidden constraints: packaging tiers, add-ons, professional services,
   seat minimums, data migration, regional hosting, integration limits?
6. Do two sources describe the same capability differently? That is a
   contradiction or qualification to record.
7. Am I treating absence of evidence as evidence of absence?
8. Did one vendor get a stricter or looser standard than another, including
   because it had an AI agent?

Update statuses, fit, and the summary if the pass changes anything material.
In the report, include only results that changed or sharpened a finding (for
example "What changed during review: Vendor A's 6-week implementation claim
was downgraded to Contradicted after two customer accounts described 4-6 months").
Never print the checklist itself.
