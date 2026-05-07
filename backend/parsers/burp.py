import xml.etree.ElementTree as ET

from .common import finding


def _text(issue: ET.Element, tag: str, default: str = "") -> str:
    node = issue.find(tag)
    return node.text.strip() if node is not None and node.text else default


def parse_burp(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    findings: list[dict] = []

    for issue in root.findall(".//issue"):
        title = _text(issue, "name", "Burp Suite finding")
        severity = _text(issue, "severity", "Informational")
        host = _text(issue, "host", "web-application")
        path = _text(issue, "path", "")
        detail = _text(issue, "issueDetail", _text(issue, "background", "Burp Suite reported a web application security issue."))
        remediation = _text(issue, "remediationBackground", "Review the affected endpoint and apply vendor or framework-specific remediation.")
        refs = _text(issue, "references", "https://portswigger.net/web-security")

        findings.append(
            finding(
                title=title,
                severity=severity,
                description=detail,
                affected_host=f"{host}{path}",
                remediation=remediation,
                references=refs,
                source="Burp Suite",
            )
        )

    return findings
