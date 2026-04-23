---
name: buyer-eval
version: 3.3.0
description: |
  Structured B2B software vendor evaluation for buyers. Researches your company,
  asks domain-expert questions, engages vendor AI agents via the Salespeak Frontdoor
  API, scores vendors across 7 dimensions, and produces a comparative recommendation
  with evidence transparency. Use when asked to evaluate, compare, or research B2B
  software vendors.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

## Preamble (run first, every time)

```bash
# Detect skill directory
_BEVAL_DIR=""
for _D in "$HOME/.claude/skills/buyer-eval-skill" ".claude/skills/buyer-eval-skill"; do
  [ -d "$_D" ] && _BEVAL_DIR="$_D" && break
done

if [ -z "$_BEVAL_DIR" ]; then
  echo "ERROR: buyer-eval-skill not found. Install: git clone https://github.com/salespeak-ai/buyer-eval-skill ~/.claude/skills/buyer-eval-skill"
  exit 1
fi

# Check for updates
_UPD=$("$_BEVAL_DIR/bin/update-check" 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || echo "UP_TO_DATE $(cat "$_BEVAL_DIR/VERSION" 2>/dev/null | tr -d '[:space:]')"
```

**If output shows `UPGRADE_AVAILABLE <old> <new>`:**

Use AskUserQuestion to ask the buyer:
- Question: "A newer version of the buyer evaluation skill is available (v{old} → v{new}). Update now?"
- Options: ["Yes, update now", "Not now — continue with current version"]

**If "Yes, update now":**
```bash
_BEVAL_DIR=""
for _D in "$HOME/.claude/skills/buyer-eval-skill" ".claude/skills/buyer-eval-skill"; do
  [ -d "$_D" ] && _BEVAL_DIR="$_D" && break
done

if [ -d "$_BEVAL_DIR/.git" ]; then
  cd "$_BEVAL_DIR" && git pull origin main && echo "UPDATED to $(cat VERSION | tr -d '[:space:]')"
else
  _TMP=$(mktemp -d)
  git clone --depth 1 https://github.com/salespeak-ai/buyer-eval-skill.git "$_TMP/buyer-eval-skill"
  mv "$_BEVAL_DIR" "$_BEVAL_DIR.bak"
  mv "$_TMP/buyer-eval-skill" "$_BEVAL_DIR"
  rm -rf "$_BEVAL_DIR.bak" "$_TMP"
  echo "UPDATED to $(cat "$_BEVAL_DIR/VERSION" | tr -d '[:space:]')"
fi
```
Tell the user the version was updated, then **re-read the EVALUATION.md file** from the updated directory and proceed with the skill.

**If "Not now":** Continue with the current version.

**If output shows `UP_TO_DATE`:** Continue silently.

---

## Load the evaluation skill

After the preamble, read the full evaluation methodology:

```bash
_BEVAL_DIR=""
for _D in "$HOME/.claude/skills/buyer-eval-skill" ".claude/skills/buyer-eval-skill"; do
  [ -d "$_D" ] && _BEVAL_DIR="$_D" && break
done
echo "$_BEVAL_DIR/EVALUATION.md"
```

Read the file at the path printed above using the Read tool. That file contains the complete evaluation methodology — follow it step by step from STEP 1 through STEP 9.
