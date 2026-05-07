from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.ai.openrouter import OpenRouterClient, executive_summary_prompt
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.reports.pdf import build_pdf_report


router = APIRouter()


@router.get("/{scan_id}/pdf")
async def report_pdf(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    findings = db.query(Finding).filter(Finding.scan_id == scan.id).order_by(Finding.priority.desc()).all()
    system, user = executive_summary_prompt(findings)
    summary = await OpenRouterClient().complete(system, user)
    pdf = build_pdf_report(scan, findings, summary)
    filename = f"securescope-report-{scan.id}.pdf"
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
