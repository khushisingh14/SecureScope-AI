from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.schemas import FindingRead


router = APIRouter()


@router.get("", response_model=list[FindingRead])
def list_findings(
    severity: str | None = None,
    source: str | None = None,
    search: str | None = None,
    sort: str = Query("severity", pattern="^(severity|created_at|title)$"),
    direction: str = Query("desc", pattern="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Finding).join(Scan).filter(Scan.user_id == current_user.id)
    if severity:
        query = query.filter(Finding.severity == severity)
    if source:
        query = query.filter(Finding.source == source)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Finding.title.ilike(like), Finding.description.ilike(like), Finding.affected_host.ilike(like)))

    sort_column = {"severity": Finding.priority, "created_at": Finding.created_at, "title": Finding.title}[sort]
    query = query.order_by(desc(sort_column) if direction == "desc" else asc(sort_column))
    return query.all()
