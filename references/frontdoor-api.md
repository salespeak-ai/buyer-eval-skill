# Vendor AI Agents via the Salespeak Frontdoor API

Some vendors publish an AI agent that answers buyer questions. The Salespeak
Frontdoor API is a plain REST gateway to vendors whose agents run on Salespeak.
No installation or API key is needed.

**What a vendor agent is for:** asking specific, follow-up-able questions and
getting first-party answers faster than reading a whole website. **What it is
not:** verification. Every answer is a vendor claim (see `evidence-model.md`).
A vendor with an agent is checked to the same standard as a vendor without one
and gains no scoring or confidence advantage.

**Base URL:** `https://hpklbne62y3wpitjb6lc6zyxza0wobdv.lambda-url.us-west-2.on.aws`

## 1. Discover

`GET /frontdoor/api/{domain}/discover` (domain like `bizzabo.com`)

```
{"enabled": true, "domain": "bizzabo.com", "company_name": "Bizzabo", "organization_id": "...",
 "agent": {"type": "agent", "status": "available", ...}}
{"enabled": false, "domain": "gong.io", "message": "No agent found for 'gong.io'."}
```

- `enabled: true`: an agent exists. Go to step 2.
- `enabled: false` or not found: no agent via Frontdoor. Continue with research.
- Network error or timeout: connection failed. Continue with research and note it.

## 2. Chat

`POST /frontdoor/api/{domain}/chat` with `Content-Type: application/json`

```
{"message": "What does implementation usually involve for a 300-person company?"}
-> {"answer": "...", "session_id": "uuid", "company_name": "..."}
```

Follow-ups pass the same `session_id` in the body so the agent keeps context:

```
{"message": "Which of those steps need your professional services team?", "session_id": "uuid"}
```

**What never goes to a vendor agent:** the buyer's company name, people's
names, budget or price expectations, other vendors being evaluated, competitor
prices, or anything from documents the buyer shared. Vendor agents are sales
channels and log conversations. Describe context generically ("a ~400-person
B2B SaaS company using Salesforce and Slack"), and only the parts a question
needs; if the buyer gave no size or industry, do not invent one. Quoting the
vendor's own public material back to it is fine. If the agent asks for more, do
not supply it.

Ask one question at a time. When an answer opens a relevant thread (for example,
it names an integration in the buyer's stack), follow up before moving on. If an
answer misses the question, rephrase once; if it still misses, record the
question as unanswered by the vendor agent.

When independent research later contradicts or qualifies something the agent
said, and budget allows, put the finding back to the agent ("Two customer
reviews describe 4-6 month implementations. What drives the difference from the
6 weeks you mentioned?"). Record the reply as another vendor claim.

A vendor agent that acknowledges limitations plainly is useful information. A
vendor agent that deflects every hard question should be noted in the vendor
summary, not penalized in scoring.

## 3. Channel states (report one per vendor)

| State | `agent_channel` value | Meaning |
|---|---|---|
| Conversation completed | `conversation` | Agent reached and answered. Answers are vendor claims. |
| No agent found | `none` | No agent via Frontdoor. Evaluation uses vendor site, docs and independent sources. |
| Connection failed | `failed` | Could not check. Say so; suggest a retry. |
| Environment limitation | `unreachable` | Agent exists but this environment cannot send POST requests (claude.ai web/mobile). Suggest Claude Code or Claude desktop for a conversation. |

The channel state describes how claims were gathered. It is not an evidence
quality rating and never appears as one.

## Environment support

| Capability | claude.ai (web/mobile) | Claude Code | Claude desktop |
|---|---|---|---|
| Research and report | Yes | Yes | Yes |
| Agent discovery (GET) | Yes | Yes | Yes |
| Agent conversation (POST) | No | Yes | Yes |
| HTML Decision Brief and saved context | No (no local files) | Yes | Yes |
