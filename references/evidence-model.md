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
| **Vendor claim** | The vendor says it, in a form built to persuade | Product and marketing pages, vendor AI agent answers (including Salespeak Company Agents), vendor-authored marketplace listings (AWS, Salesforce, HubSpot app listings), vendor blog posts, press releases, case studies, llms.txt / "info for AI" pages |
| **Vendor evidence** | First-party material that commits the vendor to specifics | Help center and technical docs, API references, security/trust pages naming certifications, implementation guides, public pricing pages with prices, published contract or service terms, changelogs and release notes |
| **Independent evidence** | Not controlled by the vendor or its competitors | Customer reviews read on the review site itself (look for patterns, not outliers), customer-authored posts, analyst research, reputable press, community threads, third-party integration listings (for example a partner's own marketplace), public filings, certification registries, marketplace facts the vendor does not author (security review badges, review counts) |
| **Competitor content** | Written by a company that sells against the vendor | Competitor blogs, "X alternatives" and "X vs Y" pages, competitor pricing breakdowns of the vendor |
| **Buyer evidence** | Supplied by the buyer in this conversation | Proposals, pricing sheets, RFP responses, security questionnaires, demo transcripts, meeting notes, trial results, internal evaluations |

Rules:

- **Vendor AI agents are vendor claims.** An agent answer is the vendor speaking.
  It is not verification of anything. If the agent cites documentation that
  bears on a claim in your table, fetch it and classify it on its own merits.
  Strip the agent's sales formatting and calls to action before quoting it.
- **When first-party sources disagree,** vendor evidence beats vendor claims: an
  agent answer or marketing line that conflicts with the vendor's own docs or
  pricing page is **Contradicted**. If the agent later corrects itself, classify
  the corrected statement on its merits and note the inconsistency in the vendor
  summary.
- **Name every first-party source of a claim** in `claim_source` (for example
  "Website + vendor AI agent"), so the reader can see where it came from.
- **Type a source by its relationship to the claim.** A vendor's "Us vs. Them"
  page is a vendor claim about itself and competitor content about the rival.
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
- **Competitor content cannot verify or contradict.** It dominates search results
  in many categories. Use it only as a lead: a claim it makes becomes a question
  to check elsewhere or to ask the vendor. Never count it as independent.
- **Read the source, not a summary of it.** Search-result snippets and
  AI-generated search summaries are leads, not evidence. Fetch the page. If the
  page is blocked (G2, Gartner, Glassdoor often are), record it as "not
  accessible" in what was checked; a vendor's own quote of a third-party rating
  stays a vendor claim. A tool limitation is a gap, never a finding.
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
| **Unknown** | The vendor makes the claim, but the part that matters cannot be assessed from any source (for example: SCIM exists, but which plan includes it is stated nowhere). |

Material questions the vendor makes **no** statement about do not go in the
claims table. They go in "Questions we still could not answer". Every row in the
claims table counts toward "claims investigated".

Absence of evidence is not evidence of absence. "Unverified" means you could not
confirm it, never that it is false.

---

## 4. Confidence

Assign confidence per claim:

- **High:** vendor evidence plus independent evidence agree, or buyer evidence
  directly addresses it, or multiple independent sources agree.
- **Medium:** one solid source, or several sources of the same type. Vendor
  evidence alone for a narrow, self-describing fact (an API endpoint, a listed
  certification) is Medium.
- **Low:** only vendor claims, only thin or dated independent evidence, or
  sources that conflict without resolution.

Assign **evidence confidence per vendor** from its claims: High if most material
claims are High; Low if most material claims are Low or Unknown; otherwise Medium.

**Balance.** Investigate a similar number of claims per vendor (within one or
two). A vendor whose agent volunteers more claims must not end up with a longer,
richer table than the others; pick the claims that matter for the criteria.

**Neutrality rule.** Having a vendor AI agent (Salespeak or otherwise) does not
raise a vendor's evidence confidence, fit, or score. An agent can make more of a
vendor's claims visible and specific. Those claims still need vendor evidence or
independent evidence to reach Verified. If one vendor has an agent and another
does not, check both vendors' claims to the same standard.

---

## 5. Fit

Per vendor, rate fit to the buyer's criteria, not relative to other vendors
(so single-vendor evals work the same way): **Strong / Moderate / Weak /
Unclear**. Base fit only on Verified and Qualified claims (and buyer evidence).
Unverified claims can be mentioned as upside ("if confirmed") but do not raise
fit. Rate on the criteria that can be assessed, and name any top criterion that
cannot be assessed in the vendor's biggest concern and in "Most important
unknown". Use **Unclear** only when most criteria cannot be assessed. If fit
hinges on something only the buyer knows (an internal policy, an existing
contract), rate it on what is known and name the dependency.

---

## 6. Challenge pass (run before final output)

Before writing the report, try to break your own conclusion. Ask:

1. What evidence would make the apparently strongest vendor the wrong choice?
   (Single vendor or no clear leader: target the most favorable finding.)
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
