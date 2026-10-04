"""pillar_guard: PII masking and prompt-injection sanitization. Stdlib only, free.
mask(text) -> text with emails, phones, card numbers (Luhn), IBAN-like, API-key-like tokens and SSN-like ids replaced.
mask_obj(obj) -> same for nested dict/list/str.
sanitize(text) -> (clean_text, flags): strips control chars and zero-width chars, neutralizes common injection phrases, flags them.
Heuristic, not a guarantee: treat as a layer, not the only control."""
import re

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_KEY = re.compile(r"\b(?:sk|pk|gsk|ghp|gho|xox[abp]|tskey-auth|AKIA)[-_A-Za-z0-9]{12,}\b|\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")
_CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
_PHONE = re.compile(r"(?<!\w)\+?\d[\d ()-]{8,14}\d(?!\w)")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")

def _luhn(s):
    d = [int(c) for c in re.sub(r"\D", "", s)]
    if not 13 <= len(d) <= 19: return False
    t = 0
    for i, n in enumerate(reversed(d)):
        if i % 2: n = n * 2 - 9 if n * 2 > 9 else n * 2
        t += n
    return t % 10 == 0

def mask(text):
    if not isinstance(text, str): return text
    text = _KEY.sub("[KEY]", text)
    text = _EMAIL.sub("[EMAIL]", text)
    text = _SSN.sub("[ID]", text)
    text = _IBAN.sub("[IBAN]", text)
    text = _CARD.sub(lambda m: "[CARD]" if _luhn(m.group(0)) else m.group(0), text)
    return _PHONE.sub("[PHONE]", text)

def mask_obj(o):
    if isinstance(o, str): return mask(o)
    if isinstance(o, dict): return {k: mask_obj(v) for k, v in o.items()}
    if isinstance(o, list): return [mask_obj(v) for v in o]
    return o

_ZW = re.compile("[\u200b-\u200f\u202a-\u202e\u2060\ufeff\x00-\x08\x0b\x0c\x0e-\x1f]")
_INJ = [re.compile(p, re.I) for p in (
    r"ignore (all |any )?(previous|prior|above) (instructions|prompts?)",
    r"disregard (the |all )?(system|previous) (prompt|instructions)",
    r"you are now\b", r"reveal (your )?(system prompt|instructions)",
    r"send (this|the|all) .{0,40}\bto\b .{0,40}@", r"do not tell the user")]

def sanitize(text):
    flags = []
    t = _ZW.sub("", text or "")
    if t != (text or ""): flags.append("hidden_chars")
    for p in _INJ:
        if p.search(t):
            flags.append("injection:" + p.pattern[:24]); t = p.sub("[removed instruction-like text]", t)
    return t, flags
