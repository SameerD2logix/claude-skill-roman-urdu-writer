---
name: roman-urdu-writer
description: Write, translate and proofread content in Roman Urdu (Urdu in Latin letters) with one consistent spelling style. Use when the user asks for Roman Urdu, "Urdu in English letters", Pakistani social media captions, WhatsApp messages, or wants English/Urdu-script text converted to Roman Urdu.
---

# Roman Urdu Writer

Roman Urdu has no official spelling, so the same word appears as "hai / hy / hay / he".
This skill makes Claude write it **one consistent, readable way** and checks the result with a script.

## Workflow

1. **Understand the audience.** Casual (WhatsApp, Instagram) or professional (client message, LinkedIn)?
   Default to friendly-professional.
2. **Write naturally.** Keep English words that Pakistanis normally use in English
   (app, server, meeting, deadline, update). Do not force rare Urdu words.
3. **Use the standard spellings** in `reference/spelling-guide.md`.
4. **Check the draft** with the script:
   ```bash
   python scripts/check_roman_urdu.py draft.txt          # report issues
   python scripts/check_roman_urdu.py draft.txt --fix    # print corrected text
   ```
   Fix every reported line before giving the final answer.
5. **Return** the final text only, unless the user asked for notes.

## Style rules

- Short sentences. One idea per sentence.
- Respectful forms by default: "aap", "kijiye", "farmaiye" for clients; "tum" only if the user does.
- Numbers, prices and dates in digits: `Rs 2,500`, `15 Nov`.
- No mixed scripts in one sentence (don't put Urdu script inside Roman Urdu).
- Emojis only for social media captions, max 2–3.

## Converting from Urdu script

Transliterate by **sound**, not letter by letter:
`کیا حال ہے` → `kya haal hai`, `شکریہ` → `shukriya`, `ضرور` → `zaroor`.

## Examples

See `examples/` for a caption, a client message and a short announcement.
