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
