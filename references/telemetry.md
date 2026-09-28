# Telemetry (opt-in, off by default)

Load this file only when `TELEMETRY_STATE` is `consented` or `unasked`.

Telemetry never delays or gates the evaluation. The buyer always gets the full
brief and HTML regardless of their answer. The consent question is asked once,
ever, after the evaluation is delivered.

Never send: the buyer's name, company, email, anything the buyer typed about
themselves, answers to discovery questions, vendor responses, claim text,
evidence text, or documents.

## Events

These are the only events. Do not invent others.

| Event | When | Fields |
|---|---|---|
| `skill_started` | Right after the preamble | `skill_version`, `mode` (`quick`/`deep`), `returning_user` (true if `PROFILE` was a saved profile) |
| `eval_context` | After Frontdoor discover calls | `category` (slug), `vendor_count`, `vendors` (array of domains), `company_agents_found` (int), `evaluation_path` (`company_agent_engaged` / `passive_research_only` / `mixed`) |
| `discovery_question_asked` | Deep Eval only, after the buyer answers the why-now question or a domain-expert question | `step` (`why_now` / `domain_expert`), `category` (slug or null), `topic` (short slug), `question_text` (the question you asked, never the answer) |
| `vendor_question` | For each question formulated for a vendor, whether or not an agent answered | `vendor` (domain), `category`, `dimension`, `question_text`, `delivery_method` (`asked_via_company_agent` / `would_have_asked` / `connection_failed`) |
| `deep_eval_requested` | The buyer asks for Deep Eval | `after_quick` (bool) |
| `vendor_scored` | Deep Eval only, per numeric dimension score | `vendor`, `dimension`, `score` (1-5; skip GAP) |
| `eval_completed` | After the brief is delivered | `mode`, `vendor_count`, `claims_total`, `verified`, `qualified`, `contradicted`, `unverified`, `unknown`, `unanswered_count`, `report_created` (bool: HTML rendered), `leading_vendor` (domain or null) |
| `eval_aborted` | The buyer abandons before the brief | `at_step` |

## Sending

**`consented`:** send each event as it happens:

```bash
python3 "$_BEVAL_DIR/bin/track.py" event eval_completed --session-id "$SESSION_ID" \
  --json '{"mode":"quick","vendor_count":2,"claims_total":14,"verified":6,"qualified":3,"contradicted":1,"unverified":3,"unknown":1,"unanswered_count":4,"report_created":true,"leading_vendor":null}'
```

The script no-ops silently on any error.

**`unasked`:** do not send. Keep the event objects in working memory. After the
brief and HTML are delivered, show this once:

```
─────────────────────────────────────────────────────────────
One optional question, asked only this once.

Salespeak maintains Buyer Eval. To improve it, we'd like to learn which
questions buyers want vendors to answer. With your permission we'd send
anonymized data from this and future runs:

  • The questions generated for vendors, and vendor domains
  • Counts of verified / unverified / contradicted claims, and scores
  • A random ID to group your runs (not linked to you)

Never sent: your name, email, or company; anything you told me about
yourself; vendor answers; claim or evidence text; your documents.

Verify: bin/track.py (plain Python) and the local log ~/.salespeak/buyer-eval.log
Change your mind: python3 bin/track.py revoke
Delete your data: email privacy@salespeak.ai with your ID (python3 bin/track.py show)
─────────────────────────────────────────────────────────────
```

Then AskUserQuestion: "Share anonymized usage data from Buyer Eval runs?"
Options: "Yes, share anonymized data" / "No thanks".

- Yes: `python3 "$_BEVAL_DIR/bin/track.py" grant --session-id "$SESSION_ID" --events '<JSON array>'`
  (build the array with `json.dumps` if question text contains quotes), then say
  "Sharing enabled. `python3 bin/track.py revoke` turns it off."
- No: `python3 "$_BEVAL_DIR/bin/track.py" decline`, then say "No data shared. We won't ask again."

**`declined` / `locked_off`:** nothing.

Administrators can disable telemetry for everyone with `BUYER_EVAL_NO_TELEMETRY=1`
or `/etc/salespeak/buyer-eval.json` containing `{"locked": true, "consent": false}`.
