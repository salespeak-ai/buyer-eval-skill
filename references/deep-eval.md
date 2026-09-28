# Deep Eval

Full buying diligence. Run it when the buyer asks for deep, full, or
comprehensive diligence, or asks to go deeper after a Quick Eval.

Also load: `evidence-model.md`, `frontdoor-api.md`, `report-format.md`, `scoring.md`.

If a Quick Eval report JSON exists from this conversation (or the buyer points
to one in `~/buyer-eval-reports/`), start from it: keep its claims and sources,
and deepen rather than redo.

Deep Eval asks the buyer more questions than Quick Eval. Batch them: each step
below asks at most one consolidated message. Expect roughly 20-40 minutes.

No action beyond research is taken without explicit approval: no emails to
vendors, demo bookings, trials, or commitments.

---

## D1. Why now

Unless the buyer already explained it, ask one open question:

> "What's driving the search for this right now?"

The answer surfaces the core pain, whether this is a first purchase or a
replacement, failed prior tools, urgency, and implicit requirements. Use it to
calibrate criteria, weights, vendor-agent questions, and emphasis.

## D2. Buyer research

Research the buyer's company before the vendors (skip what the saved profile
already covers): industry, size, region, business model, likely stack (job
posts, integration pages, engineering content), maturity. Then ask only the gaps
you could not resolve, in one message. If there are none, ask nothing.

## D3. Hard constraints

If the saved profile has `hard_constraints`, state them in one line and ask for
changes or exceptions for this evaluation. If it has none, ask once:

> "Any hard requirements or automatic disqualifiers? For example budget ceiling,
> must-have integrations, compliance certifications, data residency, or
> implementation timeline."

Confirm the active constraint set in one message. Then do a light check of each
vendor against it (website, trust page, docs). If a vendor appears to fail a
hard constraint, say so with the evidence and let the buyer drop it or keep it.

Save new reusable constraints with `bin/profile.py save` at the end of the run
(see SKILL.md section 5).

## D4. Category calibration

Infer the category from the vendors' positioning and confirm it in one sentence.
Then reason about the category:

- Which dimensions matter most, and why
- What "good" looks like per dimension
- The most common post-purchase failure modes
- Category-specific differentiators (architectures built for different buyers)
- Dimension weights, adjusted for this buyer
- Pricing benchmarks for the buyer's size (typical ACV, pricing models, discounts)

## D5. Domain-expert discovery questions

Turn the calibration into 2-4 questions a domain expert would ask, questions
that change what gets evaluated and how it is weighted. Not gap-filling ("What
CRM do you use?"). Each question explains why it matters.

Present them in one message:

> "Before I evaluate vendors, a few questions that decide fit in [category]:"

Examples (illustrative; reason about each category dynamically):

**Examples by category (illustrative, not exhaustive, the agent reasons dynamically):**

*Customer Success platforms:*
> *"Is your CS team running high-touch (dedicated CSMs, <50 accounts each) or low-touch/digital-led (automated journeys, 1-to-many)? Most CS platforms are architecturally built for one model; choosing a tool built for the other is a common post-purchase regret in this category."*

*External Attack Surface Management (EASM):*
> *"How many acquisitions has your company completed in the last 3 years, and do you have a complete DNS inventory for each? The biggest differentiator between EASM tools is how they handle inherited infrastructure from M&A, some discover it automatically from a single seed domain, others require you to provide every domain manually."*

*FP&A / Financial Planning:*
> *"How many legal entities or subsidiaries do you consolidate across? FP&A tools that work well for single-entity reporting often break at multi-entity consolidation, it's a common failure point in this category."*

*Secrets Management:*
> *"How many of your microservices use short-lived vs. long-lived credentials today? And are teams generating secrets centrally or does each team manage their own? This determines whether you need a platform optimized for dynamic secret generation at scale or one optimized for centralized policy enforcement, they're architecturally different choices."*

*Breach and Attack Simulation (BAS):*
> *"Are you primarily looking to validate security controls continuously, or do you need to run red-team-style attack chains end to end? Some BAS tools excel at control validation (testing individual defenses) while others are built for full kill-chain simulation, the distinction matters more than most vendors will tell you."*

*Website Builder (agencies):*


**What the agent does with the answers:**

- Updates dimension weights if the answer shifts what matters most (e.g. multi-entity consolidation → increase Integration weight)
- Adds the answer as a specific evaluation criterion in the relevant dimension (e.g. "must support automated M&A asset discovery" added to Product Fit)
- Adjusts the due diligence question bank to probe the specific area in vendor conversations (e.g. ask the vendor AI agent specifically about multi-entity consolidation rather than generic reporting)
- Saves reusable answers to the buyer profile at the end of the run

**Rules:**

- Maximum 4 questions. The buyer's time is valuable. Ask only what genuinely changes the evaluation.
- Never ask questions that the "why now" answer already addressed. If the buyer already said "we've grown through acquisitions and have a poorly documented external footprint," do not ask about M&A, that's already captured.
- Every question must include the "why it matters" context. A question without context ("How many entities do you consolidate?") feels like a form. A question with context ("How many entities do you consolidate? This matters because...") feels like expert guidance.
- If the buyer's "why now" and profile are detailed enough that all major decision factors are already covered, the agent says so and proceeds: *"Your context is detailed enough that I don't have additional questions, let me start the evaluation."*


Answers become `discovered` criteria in the report.

## D6. Vendor AI agent conversations

Run Frontdoor discover for every vendor (`frontdoor-api.md`). Where a
conversation is possible, work through the question bank below one question at
a time, with follow-ups. Every answer is a vendor claim. Later, put material
contradictions from independent research back to the agent and record the reply.

### Question bank

Use these as the basis for vendor-agent questions and for passive research on
vendors without an agent. Tailor each to the buyer's criteria.

The agent works through these questions via the vendor AI agent where available, or passive research where not. Questions are organized by evaluation dimension.

**Product & Fit**
- What problem does [Vendor] primarily solve, and for what type of customer?
- What are the top capabilities that differentiate you from competitors in this category?
- How does the product handle [specific use case from buyer's "why now" answer]?
- What are the known limitations of the product today?
- What does the product roadmap look like over the next 6-12 months?
- Is the product better suited for [high-touch / low-touch / PLG / enterprise] -- based on category calibration?

**Integration & Technical**
- What native integrations exist for [tools identified in buyer's inferred stack]?
- What is the typical implementation timeline, and what internal resources does it require from the buyer?
- Is there a public API? What are its capabilities and constraints?
- What is the onboarding process, and is there a self-serve option?

**Pricing & Commercial**
- What is the pricing model (per seat, usage-based, flat fee, outcome-based)?
- What is the typical contract structure for a company of [buyer's size]?
- Are there minimum contract lengths, seat minimums, or auto-renewal terms?
- What typically drives price increases at renewal?

**Security & Compliance**
- What compliance certifications does the vendor currently hold?
- Where is customer data stored, and in which regions?
- What is the data retention and deletion policy?
- Has the company experienced any security incidents in the last 24 months?

**Company & Support**
- How long has the company been operating, and how many customers are on the platform?
- What does the support model look like, and what SLAs are offered?
- Are there reference customers in [buyer's industry] who could be contacted?

**Adversarial / Stress-Test Questions**

These questions are designed to surface information vendors are less likely to volunteer. The agent asks them through the vendor AI agent where available, and researches them through review sites and public sources where not:

- What are customers' most common complaints or frustrations with the product?
- What use cases or customer profiles are you NOT a good fit for?
- What is the typical reason customers leave or don't renew?
- Has the company had any significant leadership changes, layoffs, or restructuring in the last 12 months?
- What is the biggest feature gap your customers are asking for that you haven't shipped yet?

When a vendor AI agent declines to answer or deflects an adversarial question, note the deflection in the vendor summary and research the question independently. Do not adjust scores for agent behavior; score the evidence.

---

## D7. Evidence research

Research every vendor to the same standard, whether or not it has an AI agent. For vendors with an agent, this is where agent claims get checked.

For each source, the agent extracts evidence mapped to evaluation dimensions -- not general summaries.

**Vendor Website + Documentation**
Product pages, pricing page, integration docs, security/trust page, customer case studies, changelog. Extract: capabilities, pricing model, integration list, compliance certifications, customer references, product history.

**Review Sites (G2, Capterra, TrustRadius)**
Extract: overall rating, category ranking, most cited pros and cons, recency of reviews (last 12 months weighted more heavily), reviewer profile (company size, role, use case). Look for patterns, not outliers.

**Salesforce AgentExchange / AppExchange** (conditional: only when the buyer's stack is Salesforce-centric, as detected in D2 buyer research)
Salesforce's vendor-curated marketplace (AppExchange rebranded to AgentExchange in 2025 with the Agentforce launch). Treat this as an **ecosystem-fit signal**, not as an independent review source comparable to G2. Rules:
- **When to pull:** only if the buyer uses Salesforce (Sales Cloud, Service Cloud, Agentforce, Slack) as a system of record, OR if the category inherently runs on Salesforce (e.g. CPQ, field service, revenue intelligence). Otherwise skip, it will be noise.
- **What to extract:** Salesforce Partner tier (Base → Ridge → Crest → Summit), Security Review certification status, install count ranges (e.g. "10k+ orgs"), review count and average, Agentforce-specific certifications, reviewer community badges (MVP, Ranger, Top Reviewer).
- **Do not lump this rating with G2/Capterra in the score.** Record it under the Integration & Technical and Customer Evidence dimensions as Salesforce-ecosystem corroboration. Vendor-curated marketplaces have structural bias (vendors can solicit reviews from customers, Salesforce controls what gets listed).
- **Data-quality filters (mandatory before computing any average):**
  - Require **n ≥ 10 reviews** before taking the star average seriously. Below that, report the count but ignore the number.
  - Strip reviews whose body matches known injection payloads (`{{...constructor...}}`, `javascript:`, `<script`, `alert(`, `prompt(`). Fresh agent listings are being used as XSS probe targets, observed in the field as of 2026.
  - Discount reviews missing reviewer job title and company (common on newer Agentforce listings), they cannot be cross-referenced to a company-size or role pattern.
- **Strong trust signals to surface regardless of review count:** Passed Security Review (T1, Salesforce-audited), Crest/Summit Partner tier, and multi-year listing history. These carry more weight than the star rating on thin-review listings.
- **Tier:** Security Review status is **T1** (independently audited). Star ratings and install counts are **T2** (vendor-curated marketplace data).

**Analyst Reports (Gartner, Forrester, IDC, category-specific)**
Extract: placement in relevant evaluations if applicable, analyst commentary on vendor strengths and cautions, competitive context.

**News + Press Coverage**
Extract: funding history and recency, leadership changes, product launches, acquisitions, controversies, security incidents.

**LinkedIn + Social Signals**
Extract: headcount and growth trend, leadership credibility and tenure, employee sentiment signals, quality and recency of company content.

**Pricing Intelligence Sources (Vendr, G2 pricing pages, category benchmark reports)**
Extract: published pricing tiers, reported ACV ranges by company size, common discount structures, typical contract terms. When any vendor source (pricing page, AI agent, proposal) gives specific pricing, use these sources to check whether the quoted price is in line with category norms. When no pricing is available from any source, estimate a range based on category benchmarks for the buyer's company size and state it as an estimate.

### 7.1 Source Reliability Classification

Every specific number or factual claim from research must be tagged with its source reliability tier. This is critical -- the buyer needs to know which numbers are verified and which are directional.

| Tier | Label | Description | Examples |
|------|-------|-------------|----------|
| T1 | **Audited / filed** | Audited, officially filed, or independently confirmed by multiple authoritative sources | SEC filings, audited financials, SOC 2 reports confirmed on trust pages, G2 review counts, Salesforce AppExchange Security Review certification |
| T2 | **Vendor-published** | Stated by the vendor on their own properties but not independently audited | Vendor website claims, press releases, case study metrics, vendor blog posts |
| T3 | **Self-reported / unaudited** | Data submitted by the vendor (or founder) to a third-party aggregator with no independent verification | Latka (founder interviews), Crunchbase self-reported metrics, Tracxn estimates, PitchBook unconfirmed data, AngelList profiles |
| T4 | **Estimated / inferred** | Agent's own estimate based on indirect signals | Headcount inferred from LinkedIn, revenue estimated from category benchmarks, team size from job posting volume |

**Rules for using tiered sources:**

- **Always state the tier when presenting specific numbers.** Never write "Vendor X has $1.7M ARR and 11 employees." Instead write: "Latka reports $1.7M ARR and 11 employees as of 2024 (T3: self-reported, unaudited, treat as directional, not confirmed)."
- **T3 and T4 data must include an explicit caveat** in the report. The caveat should name the source, its limitation, and recommend verification: "Verify directly with vendor during due diligence."
- **Never let T3/T4 data be the sole basis for a score.** If the only data for a dimension comes from T3/T4 sources, mark the related claims Low confidence and say so in the score note.
- **When multiple sources agree**, note the corroboration but check whether they share a common upstream source. Tracxn, CB Insights, and Latka often pull from or echo the same self-reported data, corroboration across them is weaker than it appears.
- **Scoring impact:** T3/T4 data is used directionally (e.g., "early-stage company" is a valid inference from Latka-reported $1.7M ARR) but specific numbers are never presented as confirmed facts. The Vendor Stability dimension score should reflect the evidence tier available, not just the numbers themselves.

---

Record every claim and its evidence in the claims table as defined in
`evidence-model.md`. The source tiers above describe reliability inside a
type; the type (vendor, independent, buyer) decides what a claim can be
verified by.

## D8. Risk signals

Research for every vendor, regardless of agent availability, and report each
signal factually with its source:


- Leadership stability: any C-suite departures, layoffs, or
  restructuring in the last 12 months (source: LinkedIn, press)
- Funding runway and burn signals: last funding round recency, revenue
  trajectory if public, analyst commentary on financial health
- Employee sentiment: Glassdoor rating trend (improving or declining
  over last 12 months), common themes in recent employee reviews
- Customer retention signals: G2 review recency trend (are new reviews
  increasing or declining?), presence of "switching from [Vendor]"
  reviews on competitor pages
- Acquisition or strategic risk: any acquisition rumors, acquirer
  integration risk if recently acquired, dependency on a single
  platform or ecosystem that could shift
- Product velocity: changelog or release notes frequency, evidence of
  active development vs. maintenance mode

Each signal is reported factually with its source. The agent does not
editorialize -- it presents the data and lets the buyer assess materiality.
If no concerning signals are found, the agent states: "No hidden risk
signals detected in public sources."]

## D9. Buyer evidence

Invite the buyer, once, to share anything they already have: proposals, pricing,
RFP or security questionnaire answers, demo notes or transcripts, trial results.
Classify contents as buyer evidence. Never store them in the saved profile.

## D10. Score

Score each vendor per `scoring.md`.

## D11. Challenge pass

Run `evidence-model.md` section 6. In Deep Eval, spend at least four searches
trying to disprove the leading conclusion, and re-ask vendor agents about any
material contradiction if a conversation is available.

## D12. Output

Produce the chat brief and HTML Decision Brief per `report-format.md`, with
`mode: "deep"`, plus `risks` and `scores`. Continue with SKILL.md section 5.

When the buyer later returns with demo notes, a proposal, or new facts, update
the same report JSON (add buyer evidence, re-classify claims, re-render) rather
than starting over.
