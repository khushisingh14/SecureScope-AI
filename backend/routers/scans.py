import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from backend.config import get_settings
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.parsers import PARSERS
from backend.parsers.common import coerce_finding
from backend.schemas import ScanRead
from backend.services.sanitizer import safe_filename
from backend.services.scoring import finding_priority, posture_score


router = APIRouter()
logger = logging.getLogger("securescope.scans")
ALLOWED_EXTENSIONS = {
    "nmap": {".xml"},
    "burp": {".xml"},
    "nikto": {".txt", ".log"},
    "sslyze": {".json"},
}
SCANNER_ALIASES = {
    "burp suite": "burp",
    "burpsuite": "burp",
    "nmap xml": "nmap",
    "nikto txt": "nikto",
    "sslyze json": "sslyze",
}


def _extension(filename: str) -> str:
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def _scanner(value: str) -> str:
    normalized = (value or "").strip().lower()
    return SCANNER_ALIASES.get(normalized, normalized)


@router.get("", response_model=list[ScanRead])
def list_scans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Scan)
        .options(selectinload(Scan.findings))
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.created_at.desc())
        .all()
    )


@router.post("/upload", response_model=ScanRead, status_code=201)
async def upload_scan(
    file: UploadFile = File(...),
    scanner_type: str = Form(...),
    name: str = Form(...),
    scope: str = Form("External security assessment"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    scanner = _scanner(scanner_type)
    if scanner not in PARSERS:
        raise HTTPException(status_code=400, detail="Unsupported scanner type")
    if _extension(file.filename or "") not in ALLOWED_EXTENSIONS[scanner]:
        raise HTTPException(status_code=400, detail="File extension does not match scanner type")
    clean_name = (name or "").strip()[:255] or f"{scanner.upper()} scan"

    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Upload exceeds size limit")
    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        parsed = [coerce_finding(item, scanner) for item in PARSERS[scanner](content)]
    except Exception as exc:
        logger.info("Parser failed for scanner=%s filename=%s: %s", scanner, file.filename, exc)
        raise HTTPException(status_code=400, detail=f"Could not parse scan file: {exc}") from exc

    scan = Scan(
        name=clean_name,
        scanner_type=scanner,
        filename=safe_filename(file.filename or "scan"),
        scope=scope.strip()[:4000],
        user_id=current_user.id,
    )
    try:
        db.add(scan)
        db.flush()

        findings = []
        for item in parsed:
            finding = Finding(
                scan_id=scan.id,
                title=item["title"],
                severity=item["severity"],
                description=item["description"],
                affected_host=item["affected_host"],
                remediation=item["remediation"],
                references=item["references"],
                source=item["source"],
                priority=finding_priority(item["severity"]),
            )
            findings.append(finding)
            db.add(finding)

        scan.risk_score = posture_score(findings)
        db.commit()
        db.refresh(scan)
        scan.findings = findings
    except SQLAlchemyError:
        db.rollback()
        raise

    logger.info("Imported scan id=%s scanner=%s findings=%s", scan.id, scanner, len(parsed))
    return scan


@router.get("/{scan_id}", response_model=ScanRead)
def get_scan(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = (
        db.query(Scan)
        .options(selectinload(Scan.findings))
        .filter(Scan.id == scan_id, Scan.user_id == current_user.id)
        .first()
    )
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
