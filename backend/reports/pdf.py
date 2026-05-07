from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.services.scoring import severity_counts


def ptext(value: str | None) -> str:
    return escape(value or "")


def build_pdf_report(scan, findings: list, executive_summary: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SecureScope AI Penetration Test Report", styles["Title"]))
    story.append(Paragraph(ptext(scan.name), styles["Heading2"]))
    story.append(Spacer(1, 12))

    sections = [
        ("Executive Summary", executive_summary),
        ("Scope", scan.scope),
        ("Conclusion", f"Overall security posture score: {scan.risk_score}/100."),
    ]
    for title, body in sections[:2]:
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Paragraph(ptext(body) or "Not provided.", styles["BodyText"]))
        story.append(Spacer(1, 12))

    counts = severity_counts(findings)
    matrix_data = [["Severity", "Count"], *[[key, value] for key, value in counts.items()]]
    matrix = Table(matrix_data, colWidths=[180, 80])
    matrix.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(Paragraph("Risk Matrix", styles["Heading2"]))
    story.append(matrix)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Findings and Remediation", styles["Heading2"]))
    for idx, finding in enumerate(findings, start=1):
        story.append(Paragraph(f"{idx}. {ptext(finding.title)} ({ptext(finding.severity)})", styles["Heading3"]))
        story.append(Paragraph(f"<b>Affected:</b> {ptext(finding.affected_host)}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Description:</b> {ptext(finding.description)}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Remediation:</b> {ptext(finding.remediation or 'Validate and remediate according to vendor guidance.')}", styles["BodyText"]))
        if finding.references:
            story.append(Paragraph(f"<b>References:</b> {ptext(finding.references)}", styles["BodyText"]))
        story.append(Spacer(1, 10))

    story.append(Paragraph("Conclusion", styles["Heading2"]))
    story.append(Paragraph(sections[-1][1], styles["BodyText"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
