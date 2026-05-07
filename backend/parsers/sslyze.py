import json

from .common import finding


def parse_sslyze(content: bytes) -> list[dict]:
    data = json.loads(content.decode("utf-8", errors="ignore"))
    findings: list[dict] = []
    results = data.get("server_scan_results") or data.get("accepted_targets") or []

    for item in results:
        target = item.get("server_location", {})
        host = target.get("hostname") or item.get("hostname") or "tls-service"
        port = target.get("port") or item.get("port", 443)
        affected = f"{host}:{port}"
        scan_result = item.get("scan_result", item)

        cert_info = scan_result.get("certificate_info", {})
        deployments = cert_info.get("result", {}).get("certificate_deployments", [])
        for deployment in deployments:
            leaf = deployment.get("received_certificate_chain", [{}])[0]
            not_trusted = deployment.get("path_validation_results", [{}])[0].get("was_validation_successful") is False
            if not_trusted:
                findings.append(
                    finding(
                        title="Untrusted TLS certificate chain",
                        severity="High",
                        description="SSLyze reported that the certificate chain could not be validated by the trust store.",
                        affected_host=affected,
                        remediation="Install a publicly trusted certificate chain and include required intermediate certificates.",
                        references="https://nabla-c0d3.github.io/sslyze/documentation/",
                        source="SSLyze",
                    )
                )
            if leaf.get("not_valid_after"):
                findings.append(
                    finding(
                        title="TLS certificate inventory item",
                        severity="Informational",
                        description=f"Leaf certificate expires at {leaf.get('not_valid_after')}.",
                        affected_host=affected,
                        remediation="Track certificate expiration and rotate certificates before expiry.",
                        references="https://nabla-c0d3.github.io/sslyze/documentation/",
                        source="SSLyze",
                    )
                )

        for plugin_key, label in [
            ("ssl_2_0_cipher_suites", "SSL 2.0 supported"),
            ("ssl_3_0_cipher_suites", "SSL 3.0 supported"),
            ("tls_1_0_cipher_suites", "TLS 1.0 supported"),
            ("tls_1_1_cipher_suites", "TLS 1.1 supported"),
        ]:
            plugin = scan_result.get(plugin_key, {})
            accepted = plugin.get("result", {}).get("accepted_cipher_suites", [])
            if accepted:
                severity = "Critical" if "ssl" in plugin_key else "High"
                findings.append(
                    finding(
                        title=label,
                        severity=severity,
                        description=f"SSLyze identified {len(accepted)} accepted cipher suite(s) for a deprecated protocol.",
                        affected_host=affected,
                        remediation="Disable deprecated TLS/SSL protocols and allow only TLS 1.2 or TLS 1.3 with strong ciphers.",
                        references="https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html",
                        source="SSLyze",
                    )
                )

    return findings
