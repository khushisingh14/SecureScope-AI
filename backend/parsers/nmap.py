import xml.etree.ElementTree as ET

from .common import finding


def _host_address(host: ET.Element) -> str:
    address = host.find("address")
    return address.attrib.get("addr", "unknown-host") if address is not None else "unknown-host"


def parse_nmap(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    findings: list[dict] = []

    for host in root.findall("host"):
        host_addr = _host_address(host)
        for port in host.findall("./ports/port"):
            state = port.find("state")
            if state is None or state.attrib.get("state") != "open":
                continue

            service = port.find("service")
            service_name = service.attrib.get("name", "unknown") if service is not None else "unknown"
            port_id = port.attrib.get("portid", "unknown")
            protocol = port.attrib.get("protocol", "tcp")
            severity = "Medium" if service_name in {"ftp", "telnet", "smb", "rdp"} else "Low"

            findings.append(
                finding(
                    title=f"Open {service_name.upper()} service on {port_id}/{protocol}",
                    severity=severity,
                    description=f"Nmap detected an exposed {service_name} service on port {port_id}/{protocol}. Exposed services increase attack surface and should be reviewed for business need and hardening.",
                    affected_host=host_addr,
                    remediation="Restrict access with firewall policy, disable unused services, and verify secure service configuration.",
                    references="https://nmap.org/book/man-port-scanning-basics.html",
                    source="Nmap",
                )
            )

            for script in port.findall("script"):
                output = script.attrib.get("output", "")
                script_id = script.attrib.get("id", "nmap-script")
                script_severity = "High" if "vulnerable" in output.lower() or "cve" in output.lower() else "Medium"
                findings.append(
                    finding(
                        title=f"Nmap script finding: {script_id}",
                        severity=script_severity,
                        description=output or f"Nmap script {script_id} returned a notable result.",
                        affected_host=f"{host_addr}:{port_id}",
                        remediation="Validate the script result, patch affected software, and apply compensating controls where patching is delayed.",
                        references="https://nmap.org/nsedoc/",
                        source="Nmap",
                    )
                )

    return findings
