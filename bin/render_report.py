#!/usr/bin/env python3
"""
buyer-eval: render a report JSON into a single-file HTML Decision Brief.

Usage:
  render_report.py REPORT.json [--out PATH]

Prints the path of the written HTML file. No third-party libraries, no external
assets: the output opens offline, prints cleanly, and can be forwarded as-is.
The JSON schema is documented in references/report-format.md.
"""

import argparse
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

STATUSES = ["Verified", "Qualified", "Contradicted", "Unverified", "Unknown"]
STATUS_NOTE = {
    "Verified": "enough supporting evidence",
    "Qualified": "true with material limits",
    "Contradicted": "credible evidence conflicts",
    "Unverified": "vendor says so; not corroborated",
    "Unknown": "no source answers it",
}
CHANNEL_LABEL = {
    "conversation": "Vendor AI agent consulted (answers treated as vendor claims)",
    "none": "No vendor AI agent found",
    "failed": "Vendor AI agent check failed",
    "unreachable": "Vendor AI agent exists; not reachable from this environment",
}
BASIS_LABEL = {
    "vendor_claim": "Vendor claim only",
    "vendor_docs": "Vendor documentation",
    "vendor_and_independent": "Vendor + independent evidence",
    "independent": "Independent evidence",
    "buyer": "Buyer-provided evidence",
    "mixed": "Mixed evidence",
}
# v4.0 reports used evidence_type; map it so old JSON still renders.
LEGACY_BASIS = {"vendor": "vendor_docs", "independent": "independent", "buyer": "buyer", "none": "vendor_claim"}
PRIORITY_ORDER = ["critical", "important", "useful"]
PRIORITY_LABEL = {"critical": "Critical", "important": "Important", "useful": "Useful"}
ORIGIN_LABEL = {"stated": "Stated by you", "inferred": "Inferred", "discovered": "Discovered"}
SOURCE_TYPE_LABEL = {"vendor": "Vendor", "independent": "Independent", "competitor": "Competitor", "buyer": "Your team"}

CSS = """
:root{--ink:#1b1d21;--muted:#5d6470;--line:#e3e5e9;--bg:#ffffff;--soft:#f6f7f9;
--ok:#1f7a4d;--okbg:#e7f4ed;--warn:#8a5a00;--warnbg:#fbf1dc;--bad:#a8322d;--badbg:#fbe9e7;
--info:#34598a;--infobg:#e9eff8;--none:#5d6470;--nonebg:#eef0f3}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
main{max-width:960px;margin:0 auto;padding:40px 20px 64px}
header.top{border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:28px}
.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
h1{font-size:28px;line-height:1.2;margin:0 0 8px}
.meta{color:var(--muted);font-size:14px;margin:0}
h2{font-size:19px;margin:36px 0 12px;padding-top:4px}
h3{font-size:16px;margin:20px 0 8px}
p{margin:0 0 10px}
.counts{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin:12px 0 18px}
.count{background:var(--soft);border-radius:6px;padding:10px 12px}
.count b{display:block;font-size:22px;line-height:1.1}
.count span{font-size:12px;color:var(--muted)}
.keylines{border-left:3px solid var(--ink);padding:2px 0 2px 14px;margin:0}
.keylines p{margin:0 0 8px}
.keylines strong{display:inline-block;min-width:0}
table{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0 10px}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600;background:var(--soft)}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.s-Verified{color:var(--ok);background:var(--okbg)}
.s-Qualified{color:var(--warn);background:var(--warnbg)}
.s-Contradicted{color:var(--bad);background:var(--badbg)}
.s-Unverified{color:var(--info);background:var(--infobg)}
.s-Unknown{color:var(--none);background:var(--nonebg)}
.conf{font-size:12px;color:var(--muted)}
sup a{color:var(--muted);text-decoration:none;font-size:11px}
.vendors{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.vcard{border:1px solid var(--line);border-radius:8px;padding:14px 16px}
.vcard h3{margin:0 0 8px}
.vcard dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0 0 10px;font-size:14px}
.vcard dt{color:var(--muted)}
.vnote{font-size:14px;margin:0 0 8px}
.vlabel{display:block;font-size:12px;color:var(--muted)}
.vcard dd{margin:0}
.channel{font-size:12px;color:var(--muted);margin-top:8px}
ul.clean{padding-left:18px;margin:0 0 10px}
ul.clean li{margin-bottom:6px}
.crit-origin{font-size:12px;color:var(--muted);margin-left:6px}
.q{border-top:1px solid var(--line);padding:10px 0}
.q:first-child{border-top:0}
.q .label{font-size:12px;color:var(--muted)}
.prio{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
padding:2px 8px;border-radius:4px;margin-right:8px;vertical-align:2px}
.p-critical{color:#fff;background:var(--bad)}
.p-important{color:var(--warn);background:var(--warnbg)}
.p-useful{color:var(--none);background:var(--nonebg)}
.basis{font-size:13px}
.claimsrc{display:block;font-size:12px;color:var(--muted);margin-top:3px}
ol.sources{padding-left:22px;font-size:13px;color:var(--muted)}
ol.sources a{color:var(--info);word-break:break-all}
.method{margin-top:40px;padding:16px;background:var(--soft);border-radius:8px;font-size:13px;color:var(--muted)}
.method strong{color:var(--ink)}
footer{margin-top:28px;font-size:12px;color:var(--muted)}
.tablewrap{overflow-x:auto}
@media (max-width:640px){.counts{grid-template-columns:repeat(3,minmax(0,1fr))}h1{font-size:23px}
main{padding:24px 16px 48px}
table.stack thead{display:none}
table.stack tr{display:block;border-bottom:1px solid var(--line);padding:8px 0}
table.stack td{display:block;border:0;padding:3px 0;width:auto!important}
table.stack td[data-label]::before{content:attr(data-label);display:block;font-size:11px;
text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
table.stack td:first-child{font-weight:600}}
@media print{main{padding:0;max-width:none}body{font-size:12px}h2,h3{break-after:avoid}
tr,.q{break-inside:avoid}.vcard{break-inside:auto}a{color:inherit}
.tablewrap{overflow:visible;display:block}table{break-inside:auto}thead{display:table-header-group}
.vendors{display:block}.vcard{margin-bottom:12px}}
"""


def esc(v) -> str:
    return html.escape("" if v is None else str(v))


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "buyer-eval").lower()).strip("-")
    return s[:80] or "buyer-eval"


def safe_url(url) -> bool:
    return isinstance(url, str) and re.match(r"^https?://", url.strip(), re.I) is not None


def pill(status: str) -> str:
    st = status if status in STATUSES else "Unknown"
    return f'<span class="pill s-{st}">{esc(st)}</span>'


def cite(ids, known_ids) -> str:
    if not ids:
        return ""
    if not isinstance(ids, list):
        ids = [ids]
    parts = []
    for i in ids:
        if i in known_ids:
            parts.append(f'<a href="#src-{esc(i)}">[{esc(i)}]</a>')
        else:
            parts.append(f"[{esc(i)}]")
    return "<sup>" + "".join(parts) + "</sup>"


_WARNED: set = set()


def claim_basis(c: dict) -> str:
    b = c.get("basis")
    if b in BASIS_LABEL:
        return b
    return LEGACY_BASIS.get(c.get("evidence_type"), "mixed")


def effective_status(c: dict) -> str:
    """A vendor claim alone can never render as Verified."""
    st = c.get("status") if c.get("status") in STATUSES else "Unknown"
    if st == "Verified" and claim_basis(c) == "vendor_claim":
        key = id(c)
        if key not in _WARNED:
            _WARNED.add(key)
            print(f"WARNING: '{c.get('claim')}' is Verified on a vendor claim only; shown as Unverified.",
                  file=sys.stderr)
        return "Unverified"
    return st


def unanswered_priority(q: dict) -> str:
    p = q.get("priority")
    if p in PRIORITY_ORDER:
        return p
    return "important" if q.get("material") else "useful"


def count_statuses(claims):
    counts = {s: 0 for s in STATUSES}
    for c in claims:
        counts[effective_status(c)] += 1
    return counts


def section(title: str, body: str, anchor: str) -> str:
    if not body.strip():
        return ""
    return f'<section id="{anchor}"><h2>{esc(title)}</h2>{body}</section>'


def render(data: dict) -> str:
    claims = data.get("claims") or []
    vendors = data.get("vendors") or []
    sources = data.get("sources") or []
    known_ids = {s.get("id") for s in sources}
    counts = count_statuses(claims)
    mode = "Deep Eval" if data.get("mode") == "deep" else "Quick Eval"
    title = data.get("title") or " vs ".join(v.get("name", "") for v in vendors) + " Buyer Evaluation"

    meta_bits = []
    if data.get("buyer"):
        meta_bits.append(f"Evaluated for {esc(data['buyer'])}")
    meta_bits.append(esc(data.get("date") or date.today().isoformat()))
    if data.get("category"):
        meta_bits.append(esc(data["category"]))
    meta_bits.append(mode)

    out = []
    out.append(f"""<header class="top"><p class="eyebrow">Buyer Evaluation</p>
<h1>{esc(title)}</h1><p class="meta">{' &middot; '.join(meta_bits)}</p></header>""")

    # 1. What we found
    f = data.get("findings") or {}
    cells = [f'<div class="count"><b>{len(claims)}</b><span>claims investigated</span></div>']
    for st in STATUSES:
        cells.append(f'<div class="count"><b>{counts[st]}</b><span>{esc(st.lower())}</span></div>')
    lines = []
    for key, label in (("key_finding", "Most important finding"),
                       ("key_unknown", "Most important unknown"),
                       ("next_question", "Ask next")):
        if f.get(key):
            lines.append(f"<p><strong>{label}:</strong> {esc(f[key])}</p>")
    body = f'<div class="counts">{"".join(cells)}</div>'
    if lines:
        body += f'<div class="keylines">{"".join(lines)}</div>'
    out.append(section("What we found", body, "found"))

    # 2. Criteria
    crit = data.get("criteria") or []
    if crit:
        items = "".join(
            f'<li>{esc(c.get("text"))}<span class="crit-origin">{esc(ORIGIN_LABEL.get(c.get("origin"), c.get("origin") or ""))}</span></li>'
            for c in crit)
        out.append(section("Evaluation criteria", f'<ul class="clean">{items}</ul>', "criteria"))

    # 3. Claims vs Evidence
    if claims:
        vendor_order = [v.get("name") for v in vendors] or []
        for c in claims:
            if c.get("vendor") not in vendor_order:
                vendor_order.append(c.get("vendor"))
        multi = len([v for v in vendor_order if v]) > 1
        parts = []
        for vn in vendor_order:
            rows = [c for c in claims if c.get("vendor") == vn]
            if not rows:
                continue
            trs = "".join(
                "<tr>"
                f"<td>{esc(c.get('claim'))}"
                + (f"<span class=\"claimsrc\">Claimed in: {esc(c.get('claim_source'))}</span>" if c.get('claim_source') else "")
                + "</td>"
                f"<td>{pill(effective_status(c))}"
                + (f"<br><span class=\"conf\">{esc(c.get('confidence'))} confidence</span>" if c.get('confidence') else "")
                + "</td>"
                f"<td data-label=\"Evidence basis\" class=\"basis\">{esc(BASIS_LABEL[claim_basis(c)])}</td>"
                f"<td data-label=\"What the evidence says\">{esc(c.get('evidence'))}{cite(c.get('sources'), known_ids)}</td>"
                "</tr>" for c in rows)
            head = f"<h3>{esc(vn)}</h3>" if multi else ""
            parts.append(f"""{head}<div class="tablewrap"><table class="stack"><thead><tr><th style="width:28%">Claim</th>
<th style="width:14%">Status</th><th style="width:16%">Evidence basis</th><th>What the evidence says</th></tr></thead><tbody>{trs}</tbody></table></div>""")
        out.append(section("Claims vs. evidence", "".join(parts), "claims"))

    # 4. Vendor assessment
    single = len(vendors) == 1
    if vendors:
        cards = []
        for v in vendors:
            vc = [c for c in claims if c.get("vendor") == v.get("name")]
            vcounts = count_statuses(vc)
            applies = [q for q in (data.get("unanswered") or []) if (
                q.get("vendor") == v.get("name")
                or str(q.get("vendor") or "").strip().lower() in {"both", "all", "all vendors", "each vendor"})]
            applies = [q for q in applies if unanswered_priority(q) in ("critical", "important")]
            unknowns = len(applies)
            dl = [
                ("Fit to criteria", v.get("fit")),
                ("Evidence confidence", v.get("confidence")),
                ("Verified claims", f'{vcounts["Verified"]} of {len(vc)}' if vc else None),
                ("Contradicted / qualified", f'{vcounts["Contradicted"]} / {vcounts["Qualified"]}' if vc else None),
                ("Unknown claims", vcounts["Unknown"] if vc else None),
                ("Open critical or important questions", unknowns),
            ]
            dls = "".join(f"<dt>{esc(k)}</dt><dd>{esc(val)}</dd>" for k, val in dl if val not in (None, ""))
            notes = "".join(
                f'<p class="vnote"><span class="vlabel">{esc(k)}</span>{esc(val)}</p>'
                for k, val in (("Key strength" if single else "Strongest fit", v.get("strongest")),
                               ("Key concern" if single else "Biggest concern", v.get("concern")))
                if val)
            ch = CHANNEL_LABEL.get(v.get("agent_channel"), "")
            cards.append(f"""<div class="vcard"><h3>{esc(v.get('name'))}</h3><dl>{dls}</dl>{notes}
<p>{esc(v.get('summary'))}</p>{f'<p class="channel">{esc(ch)}</p>' if ch else ''}</div>""")
        out.append(section("Vendor assessment" if single else "Where each vendor appears strongest",
                           f'<div class="vendors">{"".join(cards)}</div>', "vendors"))

    # 5. What could change
    cc = data.get("could_change") or []
    if cc:
        out.append(section("What could change the evaluation",
                           '<ul class="clean">' + "".join(f"<li>{esc(x)}</li>" for x in cc) + "</ul>", "change"))

    # 6. Unanswered
    ua = data.get("unanswered") or []
    if ua:
        qs = []
        ua = sorted(ua, key=lambda q: PRIORITY_ORDER.index(unanswered_priority(q)))
        for q in ua:
            p = unanswered_priority(q)
            chip = f'<span class="prio p-{p}">{PRIORITY_LABEL[p]}</span>'
            qs.append(f"""<div class="q"><p>{chip}<strong>{esc(q.get('question'))}</strong></p>
<p><span class="label">Why it matters:</span> {esc(q.get('why'))}</p>
<p><span class="label">Checked:</span> {esc(q.get('checked'))} &middot; <span class="label">Who should answer:</span> {esc(q.get('vendor'))}</p></div>""")
        legend = ('<p class="conf">Ordered by decision impact. Critical: could decide whether the vendor is viable. '
                  'Important: could change cost, implementation, risk, or fit. Useful: worth clarifying.</p>')
        out.append(section("What you need to get answered before you buy", legend + "".join(qs), "unanswered"))

    # 7. Demo questions
    dq = data.get("demo_questions") or []
    if dq:
        by_v = {}
        for q in dq:
            by_v.setdefault(q.get("vendor") or "", []).append(q)
        parts = []
        for vn, qs in by_v.items():
            items = "".join(
                f"<li>{esc(q.get('question'))}"
                + (f"<br><span class=\"conf\">Listen for: {esc(q.get('listen_for'))}</span>" if q.get("listen_for") else "")
                + "</li>" for q in qs)
            parts.append((f"<h3>{esc(vn)}</h3>" if len(by_v) > 1 and vn else "") + f'<ol class="clean">{items}</ol>')
        out.append(section("Questions for the next demo", "".join(parts), "demo"))

    # 8. Review changes
    rc = data.get("review_changes") or []
    if rc:
        out.append(section("What changed during review",
                           '<ul class="clean">' + "".join(f"<li>{esc(x)}</li>" for x in rc) + "</ul>", "review"))

    # 9. Deep: risks + scores
    risks = data.get("risks") or []
    if data.get("mode") != "deep":
        note = ('<p class="conf">Quick Eval does not run the full company-risk scan (leadership, funding, '
                'employee sentiment, retention). Signals below were found in passing.</p>' if risks else
                '<p class="conf">Not researched in Quick Eval. A Deep Eval covers leadership, funding, '
                'employee sentiment, and retention signals.</p>')
    else:
        note = ""
    if risks:
        trs = "".join(f"<tr><td>{esc(r.get('vendor'))}</td><td>{esc(r.get('signal'))}{cite(r.get('source'), known_ids)}</td></tr>" for r in risks)
        out.append(section("Risk signals",
                           note + f'<div class="tablewrap"><table class="stack"><thead><tr><th style="width:22%">Vendor</th><th>Signal</th></tr></thead><tbody>{trs}</tbody></table></div>',
                           "risks"))
    elif note:
        out.append(section("Risk signals", note, "risks"))
    scores = data.get("scores") or []
    if scores:
        vnames = []
        dims = []
        grid = {}
        for s in scores:
            if s.get("vendor") not in vnames:
                vnames.append(s.get("vendor"))
            key = s.get("dimension")
            if key not in dims:
                dims.append(key)
            grid[(key, s.get("vendor"))] = s
        weights = {s.get("dimension"): s.get("weight") for s in scores if s.get("weight") is not None}
        head = "".join(f"<th>{esc(v)}</th>" for v in vnames)
        rows = []
        for d in dims:
            w = weights.get(d)
            cells = []
            for v in vnames:
                s = grid.get((d, v)) or {}
                val = s.get("score")
                shown = "GAP" if val is None else f"{val}/5"
                note = f'<br><span class="conf">{esc(s.get("note"))}</span>' if s.get("note") else ""
                cells.append(f"<td>{esc(shown)}{note}</td>")
            rows.append(f"<tr><td>{esc(d)}{f' <span class=conf>({esc(w)}%)</span>' if w is not None else ''}</td>{''.join(cells)}</tr>")
        body = (f'<p class="conf">Scores are 1-5 per dimension and rate only verified or qualified evidence. '
                f'GAP means not enough evidence to score. Read them after the claims above, not instead of them.</p>'
                f'<div class="tablewrap"><table><thead><tr><th>Dimension</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
        out.append(section("Dimension scores", body, "scores"))

    # 10. Sources
    if sources:
        items = "".join(
            f'<li id="src-{esc(s.get("id"))}" value="{esc(s.get("id"))}">'
            f'<strong>{esc(SOURCE_TYPE_LABEL.get(s.get("type"), s.get("type") or ""))}</strong> &middot; '
            f'{esc(s.get("title"))}'
            + (f' &middot; <a href="{esc(s.get("url"))}" rel="noopener noreferrer">{esc(s.get("url"))}</a>'
               if safe_url(s.get("url")) else (f' &middot; {esc(s.get("url"))}' if s.get("url") else ""))
            + "</li>" for s in sources)
        out.append(section("Sources", f'<ol class="sources">{items}</ol>', "sources"))

    # 11. Method
    out.append(f"""<div class="method"><p><strong>How to read this.</strong> Each row in Claims vs. evidence is a specific
statement a vendor makes. Claims come from the vendor's website, documentation, or AI agent, and are first-party.
They are checked against vendor documentation, independent sources (customer reviews and accounts, analyst and press
coverage, community discussions, third-party documentation) and anything your team provided. Content written by
the vendor's competitors is treated as a lead, never as independent evidence.</p>
<p><strong>Statuses.</strong> Verified: enough supporting evidence. Qualified: true with material limits. Contradicted:
credible evidence conflicts. Unverified: the vendor says so and it was not corroborated, which is not the same as false.
Unknown: the part that matters cannot be assessed from any source.</p>
<p><strong>Evidence basis.</strong> What each status rests on. "Vendor documentation" means the vendor's own docs,
trust, or pricing pages: specific and first-party, not independent confirmation. "Vendor + independent evidence" and
"Independent evidence" mean at least one source the vendor does not control. "Vendor claim only" can never be
Verified.</p>
<p><strong>Neutrality.</strong> Answers from a vendor's AI agent are treated as vendor claims. Having an AI agent does not
improve a vendor's fit, confidence, or score. {"The vendor's claims were checked to the same standard any vendor's would be." if single else "Every vendor's claims are checked to the same standard."}</p>
<p>This brief was produced by an AI research agent and has not been reviewed by {"the vendor" if single else "the vendors"}. Verify material points
before contracting.</p></div>""")
    out.append('<footer>Generated with Buyer Eval, an open-source buyer research skill: '
               'github.com/salespeak-ai/buyer-eval-skill</footer>')

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{esc(title)}</title>
<style>{CSS}</style></head>
<body><main>{''.join(out)}</main></body></html>
"""


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render a Buyer Eval report JSON to HTML.")
    p.add_argument("report")
    p.add_argument("--out", help="Output HTML path (default ~/buyer-eval-reports/<slug>-<date>.html)")
    args = p.parse_args(argv)

    src = Path(args.report).expanduser()
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"ERROR: could not read report JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("ERROR: report JSON must be an object", file=sys.stderr)
        return 1

    if args.out:
        out = Path(args.out).expanduser()
    else:
        stem = f"{slugify(data.get('title') or 'buyer-eval')}-{data.get('date') or date.today().isoformat()}"
        out = Path.home() / "buyer-eval-reports" / f"{stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")

    json_copy = out.with_suffix(".json")
    if json_copy.resolve() != src.resolve():
        try:
            shutil.copyfile(src, json_copy)
        except OSError:
            pass
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
