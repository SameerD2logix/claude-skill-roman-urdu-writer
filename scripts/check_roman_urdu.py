#!/usr/bin/env python3
"""Check Roman Urdu text for inconsistent spellings and print fixes.

Usage:
    python check_roman_urdu.py FILE [--fix] [--json]
    echo "ap kia ker rhe hen" | python check_roman_urdu.py -

Exit code 0 = clean, 1 = issues found (handy in CI or a Claude Code hook).
No dependencies beyond the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

# variant -> standard. Only unambiguous variants are listed, so --fix is safe to apply.
VARIANTS: dict[str, str] = {
    "hy": "hai", "hay": "hai", "hae": "hai",
    "hen": "hain", "hein": "hain", "hayn": "hain",
    "nhi": "nahi", "nai": "nahi", "nahin": "nahi", "nhn": "nahi",
    "kia": "kya", "kyaa": "kya",
    "kyon": "kyun", "kiun": "kyun",
    "mien": "mein",
    "ap": "aap", "aapp": "aap",
    "abi": "abhi", "abhe": "abhi",
    "thik": "theek", "theak": "theek", "thk": "theek",
    "zarur": "zaroor", "zror": "zaroor",
    "shukria": "shukriya", "shukrya": "shukriya", "sukriya": "shukriya",
    "bht": "bohat", "bahut": "bohat", "bhot": "bohat",
    "ker": "kar", "kr": "kar",
    "rha": "raha", "rahaa": "raha", "rhi": "rahi", "rhe": "rahe",
    "skta": "sakta", "sakhta": "sakta", "skti": "sakti",
    "chahye": "chahiye", "chaiye": "chahiye", "chahie": "chahiye",
    "liay": "liye", "liyea": "liye",
    "sath": "saath",
    "phle": "pehle", "pehly": "pehle", "pehlay": "pehle",
    "jldi": "jaldi", "jaldy": "jaldi",
    "ziada": "zyada", "ziyada": "zyada",
    "thoda": "thora",
    "mjhe": "mujhe", "mujhy": "mujhe", "mhuje": "mujhe",
    "hamein": "humein", "hume": "humein",
    "unhe": "unhein", "unhen": "unhein",
}

WORD = re.compile(r"[A-Za-z']+")


@dataclass
class Issue:
    line: int
    column: int
    found: str
    suggestion: str


def _match_case(original: str, replacement: str) -> str:
    if original.isupper() and len(original) > 1:
        return replacement.upper()
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def check(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in WORD.finditer(line):
            standard = VARIANTS.get(m.group().lower())
            if standard:
                issues.append(Issue(line_no, m.start() + 1, m.group(), _match_case(m.group(), standard)))
    return issues


def fix(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        standard = VARIANTS.get(m.group().lower())
        return _match_case(m.group(), standard) if standard else m.group()

    return WORD.sub(repl, text)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--fix", action="store_true", help="print the corrected text")
    ap.add_argument("--json", action="store_true", help="print issues as JSON")
    args = ap.parse_args(argv)

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    if args.fix:
        sys.stdout.write(fix(text))
        return 0

    issues = check(text)
    if args.json:
        print(json.dumps([asdict(i) for i in issues], ensure_ascii=False, indent=2))
    else:
        for i in issues:
            print(f"{i.line}:{i.column}  '{i.found}' -> '{i.suggestion}'")
        print(f"{len(issues)} issue(s)" if issues else "No issues. Spelling is consistent.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
