from dataclasses import dataclass, asdict

from backend.services.sanitizer import clean_text
from backend.services.scoring import normalize_severity


@dataclass
class NormalizedFinding:
    title: str
    severity: str
    description: str
    affected_host: str
    remediation: str
    references: str
    source: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["severity"] = normalize_severity(data["severity"])
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = clean_text(value)
        return data


def finding(
    title: str,
    severity: str,
    description: str,
    affected_host: str,
    remediation: str,
    references: str,
    source: str,
) -> dict:
    return NormalizedFinding(
        title=title,
        severity=severity,
        description=description,
        affected_host=affected_host,
        remediation=remediation,
        references=references,
        source=source,
    ).to_dict()


def coerce_finding(item: dict | None, source: str) -> dict:
    item = item or {}
    title = clean_text(item.get("title") or f"{source} finding", 500)
    affected_host = clean_text(item.get("affected_host") or item.get("host") or "unknown-host", 255)
    description = clean_text(item.get("description") or "Scanner reported a finding without additional detail.")
    return finding(
        title=title,
        severity=normalize_severity(item.get("severity")),
        description=description,
        affected_host=affected_host,
        remediation=item.get("remediation") or "Review the finding, validate exposure, and remediate according to vendor guidance.",
        references=item.get("references") or "",
        source=item.get("source") or source,
    )
