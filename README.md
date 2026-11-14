# Roman Urdu Writer: a Claude Agent Skill

> Make Claude write **consistent, natural Roman Urdu** (Urdu in English letters) for captions, client messages and announcements, and check the spelling automatically.

![skill](https://img.shields.io/badge/Claude-Agent%20Skill-D97757) ![python](https://img.shields.io/badge/python-3.10%2B-3776AB) ![license](https://img.shields.io/badge/license-MIT-green)

## Why

Millions of Pakistanis write Urdu in Latin letters, but nobody agrees on the spelling (`hai / hy / hay / he`).
AI output in Roman Urdu often looks random. This skill gives Claude:

- a **style guide**: tone, respectful forms, when to keep English words
- a **standard spelling table** (`reference/spelling-guide.md`)
- a **zero-dependency checker** (`scripts/check_roman_urdu.py`) Claude runs on its own draft before answering

## Install

**Claude Code:** copy the folder into your skills directory:
```bash
git clone https://github.com/SameerD2logix/claude-skill-roman-urdu-writer ~/.claude/skills/roman-urdu-writer
```
**Claude.ai / API:** zip the folder and upload it as a custom skill.

Then just ask: *"Write a WhatsApp message in Roman Urdu telling the client the invoice is attached."*

## The checker

```bash
$ echo "Ap kia ker rhe hen?" | python scripts/check_roman_urdu.py -
1:1  'Ap' -> 'Aap'
1:4  'kia' -> 'kya'
1:8  'ker' -> 'kar'
1:12  'rhe' -> 'rahe'
1:16  'hen' -> 'hain'
5 issue(s)

$ echo "Ap kia ker rhe hen?" | python scripts/check_roman_urdu.py - --fix
Aap kya kar rahe hain?
```

- Exit code `1` when issues exist, so it also works as a **CI check** or a **Claude Code hook**.
- `--json` output for tools.
- Keeps capitalisation and punctuation.

## Project layout

```
SKILL.md                     instructions Claude follows
reference/spelling-guide.md  standard spellings
scripts/check_roman_urdu.py  checker + fixer (stdlib only)
examples/                    sample prompts and outputs
tests/                       pytest suite
```

## Tests

```bash
pip install pytest && pytest -q
```

## Author

**Sameer Hussain** · [LinkedIn](https://www.linkedin.com/in/sameer-hussain-87368a164) · [D2Logix](https://d2logix.com). AI automation for Pakistani businesses.
