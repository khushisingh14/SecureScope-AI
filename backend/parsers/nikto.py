import re

from .common import finding


TARGET_RE = re.compile(r"^\+\s*Target\s+(?:IP|Hostname):\s*(?P<host>.+)$", re.I)
PORT_RE = re.compile(r"^\+\s*Target\s+Port:\s*(?P<port>\d+)", re.I)


def parse_nikto(content: bytes) -> list[dict]:
    text = content.decode("utf-8", errors="ignore")
    host = "web-server"
    port = ""
    findings: list[dict] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("+"):
            continue
        target = TARGET_RE.match(line)
        if target:
            host = target.group("host").strip()
            continue
        port_match = PORT_RE.match(line)
        if port_match:
            port = port_match.group("port")
            continue
        if line.startswith("+ OSVDB") or ": " in line:
            lowered = line.lower()
            severity = "High" if any(term in lowered for term in ["xss", "sql", "default", "outdated", "cve"]) else "Medium"
            affected = f"{host}:{port}" if port else host
            findings.append(
                finding(
                    title="Nikto web server finding",
                    severity=severity,
                    description=line.lstrip("+ ").strip(),
                    affected_host=affected,
                    remediation="Confirm the finding manually, remove insecure defaults, patch the web server, and harden response headers.",
                    references="https://cirt.net/Nikto2",
                    source="Nikto",
                )
            )

    return findings
