from backend.database import Base, SessionLocal, engine
from backend.models import Finding, Scan, User
from backend.security import get_password_hash
from backend.services.scoring import finding_priority, posture_score


DEMO_FINDINGS = [
    {
        "title": "SQL injection in reporting endpoint",
        "severity": "High",
        "description": "The reports endpoint responds with database errors when quote-based payloads are supplied to the id parameter.",
        "affected_host": "https://portal.example.com/reports?id=42",
        "remediation": "Replace dynamic SQL with parameterized queries and add input validation for identifier fields.",
        "references": "https://portswigger.net/web-security/sql-injection",
        "source": "Burp Suite",
    },
    {
        "title": "SMB service likely vulnerable to MS17-010",
        "severity": "Critical",
        "description": "Nmap scripting indicated exposure consistent with MS17-010 on an internal Windows file server.",
        "affected_host": "10.10.10.25:445",
        "remediation": "Apply Microsoft security updates, restrict SMB exposure, and verify exploitability with authenticated patch checks.",
        "references": "https://nvd.nist.gov/vuln/detail/CVE-2017-0144",
        "source": "Nmap",
    },
    {
        "title": "Deprecated TLS 1.0 protocol supported",
        "severity": "High",
        "description": "SSLyze identified accepted TLS 1.0 cipher suites on the VPN gateway.",
        "affected_host": "vpn.example.com:443",
        "remediation": "Disable TLS 1.0 and TLS 1.1. Prefer TLS 1.2 or TLS 1.3 with modern cipher suites.",
        "references": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html",
        "source": "SSLyze",
    },
    {
        "title": "Administrative interface exposed",
        "severity": "Medium",
        "description": "Nikto identified an exposed administrative path on the legacy web server.",
        "affected_host": "legacy.example.com:80",
        "remediation": "Restrict administrative interfaces to trusted networks and enforce strong authentication.",
        "references": "https://cirt.net/Nikto2",
        "source": "Nikto",
    },
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "analyst@securescope.ai").first()
        if not user:
            user = User(
                email="analyst@securescope.ai",
                full_name="Security Analyst",
                hashed_password=get_password_hash("SecureScope123!"),
            )
            db.add(user)
            db.flush()

        scan = Scan(
            name="Demo External Penetration Test",
            scanner_type="demo",
            filename="demo-assessment",
            scope="External web application, VPN endpoint, and selected internal infrastructure.",
            user_id=user.id,
        )
        db.add(scan)
        db.flush()

        finding_models = []
        for item in DEMO_FINDINGS:
            model = Finding(scan_id=scan.id, priority=finding_priority(item["severity"]), **item)
            finding_models.append(model)
            db.add(model)
        scan.risk_score = posture_score(finding_models)
        db.commit()
        print("Seeded demo account analyst@securescope.ai / SecureScope123!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
