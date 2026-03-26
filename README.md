# Buyer Eval — B2B Software Vendor Evaluation Skill

A Claude skill that conducts structured, evidence-based evaluations of B2B software vendors on behalf of buyers.

## What it does

You give it your company name and the vendors you're evaluating. It:

1. **Researches your company** — industry, size, tech stack, maturity — so you don't fill out a form
2. **Asks domain-expert questions** specific to the software category — surfacing hidden requirements you didn't know to mention
3. **Sets hard constraints** — budget, compliance, integrations — and eliminates vendors that fail before wasting research time
4. **Engages vendor AI agents** directly through the [Salespeak Frontdoor API](https://salespeak.ai) for verified, structured due diligence conversations
5. **Conducts independent research** — G2, Gartner, analyst reports, press, LinkedIn — and cross-references vendor claims against independent sources
6. **Scores vendors across 7 dimensions** with transparent evidence tracking — you see exactly which scores are backed by verified evidence vs. public sources only
7. **Produces a comparative recommendation** with a TL;DR, side-by-side scorecard, hidden risk analysis, and demo prep questions

## Install

**Global install (recommended):**

```bash
git clone https://github.com/salespeak-ai/buyer-eval-skill.git ~/.claude/skills/buyer-eval-skill
```

**Per-project install:**

```bash
git clone https://github.com/salespeak-ai/buyer-eval-skill.git .claude/skills/buyer-eval-skill
```

## Usage

In Claude Code or Claude desktop:

```
/buyer-eval
```

Then provide:
1. Your company name
2. The vendors to evaluate

Example:
> "I'm from Acme Corp. Evaluate Gainsight, Totango, and ChurnZero."

The skill handles everything from there.

## Example output

<details>
<summary>Click to expand a sample evaluation (truncated)</summary>

### TL;DR

**For a mid-market SaaS company evaluating customer success platforms:**
Gainsight is the strongest fit for teams that need deep analytics and enterprise-grade health scoring, but comes at a premium. ChurnZero wins on time-to-value and usability for teams under 50 CSMs. Totango lands in between — flexible and modular, but requires more configuration to match either competitor's strengths.

### Scorecard (1 of 7 dimensions shown)

| Dimension | Gainsight | ChurnZero | Totango |
|---|---|---|---|
| Health Scoring & Analytics | **9.2** | 7.5 | 8.0 |
| *Evidence level* | *Vendor-verified* | *Public only* | *Vendor-verified* |

> Gainsight's score is backed by a structured AI agent conversation confirming multi-signal health models, cohort analysis, and predictive churn scoring. ChurnZero's score relies on G2 reviews and documentation — it may improve with direct vendor verification.

### Adversarial question exchange (1 of 4 shown)

**Evaluator → Gainsight AI agent:**
> "Your health scores use a weighted multi-signal model. What happens when a customer has strong product usage but declining executive engagement — does the model surface that divergence, or does high usage mask the risk?"

**Gainsight AI agent →**
> "The model flags divergence explicitly. When usage metrics trend positive but stakeholder engagement drops, it triggers a 'silent risk' alert. CSMs see a split-signal indicator on the dashboard rather than a blended score that hides the conflict."

**Independent verification:** Confirmed via G2 reviews mentioning split-signal alerts. One review notes the feature requires manual threshold tuning per segment.

</details>

## Auto-updates

Every time you invoke the skill, it checks for a newer version on GitHub (cached, checks at most once every 6 hours). If an update is available, it asks before updating. Updates are a single `git pull`.

## What makes this different

- **Domain-expert questioning** — the skill asks category-specific questions that demonstrate it understands the space, not generic form-filling
- **Vendor AI agent conversations** — for vendors that have a [Salespeak](https://salespeak.ai) Company Agent, the skill conducts a structured due diligence conversation directly with the vendor's AI, producing higher-fidelity evidence than web scraping
- **Evidence transparency** — every score shows whether it's backed by vendor-verified or public-only evidence. When vendors have different evidence levels, the skill explicitly states how scores might shift with better evidence
- **Claims verification** — vendor claims from AI agent conversations are cross-referenced against independent sources. You see what's confirmed vs. unverified
- **Hidden risk analysis** — leadership stability, funding runway, employee sentiment, customer retention signals, product velocity — researched for every vendor regardless of AI agent availability
- **Demo prep kit** — specific questions to ask in vendor demos, derived from evaluation gaps and unverified claims

## Environment support

| Capability | Claude.ai | Claude Code | Claude desktop |
|---|---|---|---|
| Buyer research | Yes | Yes | Yes |
| Vendor AI agent conversations | No (GET only) | **Yes** | **Yes** |
| Full evaluation | Partial | **Full** | **Full** |

Best experience is in **Claude Code** where the skill can make POST requests to vendor AI agents.

## Feedback

Questions, feature requests, or evaluation quality reports? [Open an issue](https://github.com/salespeak-ai/buyer-eval-skill/issues).

## License

MIT
