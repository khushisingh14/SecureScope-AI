import re


CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean_text(value: str | None, max_length: int = 4000) -> str:
    if value is None:
        return ""
    cleaned = CONTROL_CHARS.sub("", value)
    cleaned = cleaned.strip()
    return cleaned[:max_length]


def safe_filename(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return cleaned[:180] or "scan_upload"
