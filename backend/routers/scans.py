from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session, selectinload

from backend.config import get_settings
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.parsers import PARSERS
from backend.schemas import ScanRead
from backend.services.sanitizer import safe_filename
from backend.services.scoring import finding_priority, posture_score


router = APIRouter()
ALLOWED_EXTENSIONS = {
    "nmap": {".xml"},
    "burp": {".xml"},
    "nikto": {".txt", ".log"},
    "sslyze": {".json"},
}


def _extension(filename: str) -> str:
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


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
    scanner = scanner_type.lower()
    print(f"DEBUG: Received upload - scanner_type={scanner_type}, scanner={scanner}, filename={file.filename}")
    if scanner not in PARSERS:
        raise HTTPException(status_code=400, detail="Unsupported scanner type")
    if _extension(file.filename or "") not in ALLOWED_EXTENSIONS[scanner]:
        raise HTTPException(status_code=400, detail="File extension does not match scanner type")

    content = await file.read()
    print(f"DEBUG: File size={len(content)} bytes")
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Upload exceeds size limit")
    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        parsed = PARSERS[scanner](content)
        print(f"DEBUG: Parser returned {len(parsed)} findings")
    except Exception as exc:
        print(f"DEBUG: Parser error - {exc}")
        raise HTTPException(status_code=400, detail=f"Could not parse scan file: {exc}") from exc

    scan = Scan(
        name=name.strip()[:255],
        scanner_type=scanner,
        filename=safe_filename(file.filename or "scan"),
        scope=scope.strip()[:4000],
        user_id=current_user.id,
    )
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
