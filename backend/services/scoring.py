from collections import Counter


SEVERITY_WEIGHTS = {
    "Critical": 10,
    "High": 7,
    "Medium": 5,
    "Low": 2,
    "Informational": 1,
}


def normalize_severity(value: str | None) -> str:
    if not value:
        return "Informational"
    cleaned = value.strip().lower()
    mapping = {
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "moderate": "Medium",
        "low": "Low",
        "info": "Informational",
        "informational": "Informational",
        "none": "Informational",
    }
    return mapping.get(cleaned, "Informational")


def finding_priority(severity: str) -> int:
    return SEVERITY_WEIGHTS.get(normalize_severity(severity), 1)


def _value(item, key: str, default=None):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def posture_score(findings: list) -> float:
    if not findings:
        return 100.0
    total_weight = sum(finding_priority(_value(finding, "severity")) for finding in findings)
    max_reasonable = max(len(findings) * SEVERITY_WEIGHTS["Critical"], 10)
    score = 100 - (total_weight / max_reasonable) * 100
    return round(max(0, min(100, score)), 1)


def severity_counts(findings: list) -> dict[str, int]:
    counts = Counter(normalize_severity(_value(f, "severity")) for f in findings)
    return {severity: counts.get(severity, 0) for severity in SEVERITY_WEIGHTS}


def source_counts(findings: list) -> dict[str, int]:
    counts = Counter(_value(f, "source", "Unknown") for f in findings)
    return dict(counts)
