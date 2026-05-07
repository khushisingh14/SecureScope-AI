from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.schemas import DashboardStats
from backend.services.scoring import posture_score, severity_counts, source_counts


router = APIRouter()


@router.get("", response_model=DashboardStats)
def stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = (
        db.query(Scan)
        .options(selectinload(Scan.findings))
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.created_at.desc())
        .all()
    )
    findings = db.query(Finding).join(Scan).filter(Scan.user_id == current_user.id).all()
    return {
        "scan_count": len(scans),
        "finding_count": len(findings),
        "posture_score": posture_score(findings),
        "severity_counts": severity_counts(findings),
        "source_counts": source_counts(findings),
        "recent_scans": scans[:6],
    }
