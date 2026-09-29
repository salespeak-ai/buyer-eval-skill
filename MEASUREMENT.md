# Measuring Buyer Eval

For maintainers. What can and cannot be measured, and how.

## Signals

| Signal | What it measures | Reliable? |
|---|---|---|
| GitHub clones | Git fetches of the repo | **No.** Mostly automated (mirrors, indexers, CI). Sept 2026 sample: 419 unique cloners vs. 46 unique page viewers in 14 days. Do not report as usage. |
| GitHub views and referrers | Humans reading the repo page | Yes, for awareness only |
| `bin/update-check` | Fetches `VERSION` from raw.githubusercontent.com | Not observable by us |
| Frontdoor `discover` requests | Every run with network access calls discover once per vendor, consented or not | **Best consent-independent run count, if request logs are retained.** Status: not yet verified. Needs a check of the Frontdoor Lambda's CloudWatch logs (path, domain, timestamp, source IP). Group by source IP and hour to approximate runs; exclude Salespeak IPs. |
| Frontdoor `chat` requests | Vendor-agent conversations | Same caveat; also shows which vendor agents buyers reach |
| Telemetry events | Funnel for users who consented | Reliable but biased toward people who finish and opt in |

## Funnel (telemetry, consented users only)

| Stage | Event / field |
|---|---|
| Evaluation started | `skill_started` |
| Returning user | `skill_started.returning_user` |
| Vendors evaluated | `eval_context.vendor_count` |
| Quick Eval completed | `eval_completed` with `mode=quick` |
| Deep Eval requested | `deep_eval_requested` |
| Shareable report created | `eval_completed.report_created` |
| Repeat evaluation | more than one `eval_completed` per `user_id` |
| Consent | first event per `user_id` |

Events land in the analytics database as `event_type='buyer_eval'`.

## Cannot be measured

- Completion or repeat use for people who decline or are never asked (they quit
  before the end).
- Whether an HTML brief was forwarded or read. Reports are local files; there
  is no hosted link.
- Anything in environments that block outbound requests.

## Known history

- Before v4.0.0, `bin/track.py` crashed on import under Python 3.9 (the default
  `python3` on macOS), so telemetry failed silently for those users even after
  consent. Fixed in v4.0.0. Undercounts before that release are expected.
- The telemetry server drops events whose User-Agent it does not accept (HTTP
  200 instead of 201, logged as `dropped_by_server`). `buyer-eval-skill/4.0.0`
  was confirmed accepted (HTTP 201) on 2026-09-28. The User-Agent format is
  unchanged in later versions; spot-check the audit log after each release.
