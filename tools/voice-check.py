#!/usr/bin/env python3
"""Voice firewall check for marsmike.com drafts.

Runs the manual checks that gate every post before lift:
  1. Banned words (anti-slop)
  2. Banned transitions (anti-slop)
  3. Em-dash count (≤3)
  4. EN: contraction density (≥1 per 100 words)
  5. DE: LanguageTool grammar check (anglicism-filtered)

Usage:
    python tools/voice-check.py <draft.md>

Exits 0 on PASS, 1 on FAIL. Use stdin path "-" to pipe content.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Frontmatter banned-word lists are sourced from
# 00_Memory/voice/mike-voice-banned-patterns in the vault. Update both places
# when the canonical list changes.
BANNED_WORDS = re.compile(
    r"\b(leverage|delve|robust|holistic|tapestry|seamless|landscape|navigate"
    r"|synergy|foster|underscore|resonate|nuanced|comprehensive|streamline"
    r"|empower)\b",
    re.IGNORECASE,
)
BANNED_TRANSITION_LINE = re.compile(
    r"^\s*(Furthermore|Moreover|Additionally|That being said)\b"
)
CONTRACTION = re.compile(r"[A-Za-z]+'[a-z]+")
EM_DASH = "—"

# Engineering anglicisms LanguageTool's de-DE dictionary doesn't know.
# Suppressed only when LT flags them as a possible spelling error.
KNOWN_DE_ANGLICISMS: set[str] = {
    "Plugin-Marketplaces", "Plugin-Marketplace", "Marketplace", "Marketplaces",
    "DCO-Sign-off", "DCO", "Sign-off",
    "Homelab", "Homelab-Steuerung",
    "Big-Bang-Launches", "Big-Bang-Launch", "Big-Bang",
    "Tradeoffs", "Trade-offs", "Trade-off",
    "OSS", "Repos", "Repo",
    "Social-Cards", "Social-Card", "Social", "Cards",
    "Pop-ups", "Popups", "Pop-up", "Popup",
    "Roadmap", "GitHub", "GitHub-Sterne",
    "MacBook",
    "Claude-Code-Plugins", "Claude-Code-Plugin", "Claude-Design-HTML",
    "Video-Pipelines", "Video-Pipeline", "Video-Frames", "Video-Frame",
    "PowerPoint", "PowerPoint-Decks", "PowerPoint-Deck",
    "Deck-Produktion", "Decks",
    "Coming Soon",
    "Newsletter",
    "agentic-toolkit", "marsmike",
    # Recurring concept names from the vault (Resources/Concepts/) — likely to
    # appear in many future DE posts. Add new terms here as they show up.
    "Harness", "Harness-as-Product", "Harness-Loop-Pattern", "Harness-Moves",
    "Context", "Context-Engineering", "Context Engineering", "Context-Files",
    "Intent", "Intent-Engineering",
    "Agent-Memory", "Agent Memory", "Agent-Knowledge-Layer",
    "Scaffolding", "Spreading-Activation", "Chain-of-Thought",
    "Background-Agenten", "Background-Agent",
    "Skills", "Skill",
    "Slow-Cooking", "Slow-Plugins", "Slow-Plugin",
    # Feinschliff post — plugin-specific terminology
    "präsentationsreif",
    "Verify", "Verify-Lauf",
    "elf-klassigen", "elf-klassige", "elf-klassiger",
    "Defekt-Klassen", "Defekt-Klasse",
    "Ingest",
    "Overflow", "Empty", "Placeholder", "Empty Placeholder",
    "Layout-Mismatch", "Brand-Violation",
    "Spacing", "Density", "One-Idea", "Bullet-Dump", "Bullets",
    "Audience-Mismatch", "Red-Line-Break",
    "Curse-of-Knowledge", "Curse-of-Knowledge-Stelle", "Claim-Title",
    "DTCG", "DTCG-Draft", "DTCG-Draft-2-Design-Tokens",
    "Renderer", "Renderer-Adaptern", "Renderer-Adapter",
    "Baukasten",
    "cp", "brands", "meinco", "myco",
    "Noto", "Sans", "Noto Sans",
    "bash",
    "ARR", "MRR", "EBITDA",
    "awesome-design-md",
    "Vercel", "Linear", "Notion", "Stripe", "Spotify",
    "Slow", "Polish",
    "extend", "compile", "deck",
    # Feinschliff catalog — layout names that appear outside italic markers in prose.
    "KPI-Grid", "KPI", "Waterfall", "Stacked-Bar", "Stacked-Bar-Chart",
    "Scorecard", "Pyramid", "Bar Chart", "Line Chart", "Process Flow",
    "Action Title", "Executive Summary", "Key Takeaways",
    "Column", "2-Column", "3-Column", "4-Column",
    "Vertical", "Horizontal",
    "Heading", "Counter", "Slot", "Slots", "Slot-Schema",
    # German compounds coined for the post / Feinschliff domain.
    "Exec-Publikum", "Exec-Zielgruppe",
    "SCQA", "SCQA-Narrativ",
    "Sektions-Eröffner", "Sektions-Öffner", "End-Folie",
    "Vier-Slot-Layout", "Sieben-Bullets",
    "Anker-Totalen", "Finanz-Brücken",
    "Matching-Engine", "Token-System",
    "brand-pluggable", "Brand-Pluggable",
    # Casual-register verbs Mike's voice accepts (mirroring EN colloquialisms).
    # LT flags these as "Umgangssprache"; Mike's voice spec tolerates the casual form
    # when the EN sibling is also casual ("drop one in, get X out" → "reinwerfen, X rauskriegen").
    "reinwerfen", "rauskriegen", "rausbekommen", "reinkommen", "rausziehen",
}

LT_API = "https://api.languagetool.org/v2/check"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)\Z", text, re.DOTALL)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, m.group(2)


def check_banned_words(body: str) -> list[str]:
    return [m.group() for m in BANNED_WORDS.finditer(body)]


def check_banned_transitions(body: str) -> list[str]:
    return [
        line.strip()[:80]
        for line in body.splitlines()
        if BANNED_TRANSITION_LINE.match(line)
    ]


def is_de_false_positive(match: dict, body: str, flagged: str) -> bool:
    """Suppress LT matches Mike has manually triaged as false positives.

    Each branch is a documented exception to LT's de-DE rules. Add to the list
    only after verifying the flagged construction is grammatically correct in
    Mike's voice register.
    """
    if flagged in KNOWN_DE_ANGLICISMS:
        return True

    # Brand form: "Nacht Schafft Wissen" — official capitalization of the BSH event.
    offset, length = match["offset"], match["length"]
    context = body[max(0, offset - 25) : offset + length + 25]
    if "Nacht Schafft Wissen" in context:
        return True

    # `was` in a list of indirect questions after a colon — not a Hauptsatz, no
    # capitalization needed. Detect by colon within 60 chars before, no period
    # in between (i.e. still inside the colon-introduced span).
    if flagged.lower() == "was":
        before = body[max(0, offset - 60) : offset]
        last_colon = before.rfind(":")
        last_period = before.rfind(".")
        if last_colon > last_period >= 0 or (last_colon >= 0 and last_period < 0):
            return True

    # Partizipialgruppe comma is optional in modern German (Duden K 109).
    if flagged.strip(", ").lower().startswith("geschrieben"):
        return True

    # LT comma rule misfires on "Feinschliff erscheint heute." — simple Hauptsatz,
    # no comma needed. Suppress this exact false-positive shape.
    if flagged == "Feinschliff erscheint":
        return True

    # Markdown italic spans (*…*) wrap technical names — engineering jargon,
    # plugin commands, defect classes, layout names, vault concepts. Anything
    # whose offset falls inside an italic span is intentionally a term-of-art.
    if any(s < offset < e for s, e in _md_italic_spans(body)):
        return True

    # Code spans (`…`) wrap CLI commands, JSON keys, file paths. LT can't see
    # the formatting; suppress noise inside them.
    if any(s < offset < e for s, e in _md_code_spans(body)):
        return True

    # LT misfires on capitalisation of words that follow a markdown bold-with-period
    # sentence header like `**Section.** Word ...` — `Word` IS a sentence start, but
    # LT can't parse the markdown boundary. Detect by `**.` within 8 chars before.
    if match.get("rule", {}).get("category", {}).get("id") == "CASING":
        before = body[max(0, offset - 8) : offset]
        if "**" in before and "." in before:
            return True

    return False


def _md_italic_spans(body: str) -> list[tuple[int, int]]:
    """Return list of (start, end) offsets covering markdown italic spans `*…*`.
    Skips `**` (bold) by requiring single asterisk runs."""
    spans = []
    for m in re.finditer(r'(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)', body):
        spans.append((m.start(), m.end()))
    return spans


def _md_code_spans(body: str) -> list[tuple[int, int]]:
    """Return list of (start, end) offsets covering markdown inline code `\`…\``."""
    return [(m.start(), m.end()) for m in re.finditer(r'`[^`\n]+`', body)]


def lt_check_de(body: str) -> tuple[list[dict], str | None]:
    """Call LanguageTool, return (filtered_matches, error_or_None)."""
    data = urllib.parse.urlencode({"language": "de-DE", "text": body}).encode()
    req = urllib.request.Request(LT_API, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read())
    except Exception as exc:  # noqa: BLE001 — surfaced to caller
        return [], f"LT API call failed: {exc}"

    real: list[dict] = []
    for m in payload.get("matches", []):
        offset, length = m["offset"], m["length"]
        flagged = body[offset : offset + length]
        if is_de_false_positive(m, body, flagged):
            continue
        real.append({"flagged": flagged, "match": m})
    return real, None


def main(path_arg: str) -> int:
    if path_arg == "-":
        text = sys.stdin.read()
        label = "<stdin>"
    else:
        path = Path(path_arg).expanduser()
        text = path.read_text(encoding="utf-8")
        label = str(path)

    fm, body = parse_frontmatter(text)
    lang = fm.get("lang", "")
    word_count = len(body.split())

    print(f"voice-check: {label}")
    print(f"  lang={lang!r}  body_words={word_count}")
    print()

    ok = True

    # 1. Banned words
    bw = check_banned_words(body)
    if bw:
        print(f"[1] banned words: FAIL — {bw}")
        ok = False
    else:
        print("[1] banned words: PASS")

    # 2. Banned transitions
    bt = check_banned_transitions(body)
    if bt:
        print(f"[2] banned transitions: FAIL — {bt}")
        ok = False
    else:
        print("[2] banned transitions: PASS")

    # 3. Em-dash count
    em_count = body.count(EM_DASH)
    em_status = "PASS" if em_count <= 3 else "FAIL"
    print(f"[3] em-dashes: {em_count} (limit ≤3) — {em_status}")
    if em_count > 3:
        ok = False
    if lang == "de" and em_count > 0:
        print("    note: DE rider prefers hyphens-with-spaces over em-dashes")

    # 4. EN contraction density
    if lang == "en":
        c = len(CONTRACTION.findall(body))
        ratio = (c / word_count * 100) if word_count else 0.0
        en_status = "PASS" if ratio >= 1.0 else "FAIL"
        print(f"[4] EN contractions: {c}/{word_count} = {ratio:.2f}/100 — {en_status}")
        if ratio < 1.0:
            ok = False

    # 5. DE LanguageTool grammar
    if lang == "de":
        print("[5] DE grammar (LanguageTool, anglicism-filtered):")
        matches, err = lt_check_de(body)
        if err:
            print(f"    WARN — {err}")
        elif not matches:
            print("    PASS")
        else:
            print(f"    FAIL — {len(matches)} unsuppressed match(es):")
            for entry in matches:
                m = entry["match"]
                cat = m.get("rule", {}).get("category", {}).get("name", "")
                msg = m["message"]
                sugg = ", ".join(r["value"] for r in m.get("replacements", [])[:3])
                offset = m["offset"]
                ctx = body[max(0, offset - 25) : offset + m["length"] + 25].replace("\n", " ")
                print(f"      ({cat}) [{entry['flagged']}]")
                print(f"         {msg}")
                print(f"         …{ctx}…")
                if sugg:
                    print(f"         suggest: {sugg}")
            ok = False

    print()
    print("OVERALL:", "PASS ✅" if ok else "FAIL ❌")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
