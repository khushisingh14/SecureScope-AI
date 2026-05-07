from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.ai.openrouter import OpenRouterClient, executive_summary_prompt, vulnerability_prompt
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import Finding, Scan, User
from backend.schemas import AIRequest


router = APIRouter()


@router.post("/analyze")
async def analyze(payload: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.finding_id:
        finding = db.query(Finding).join(Scan).filter(Finding.id == payload.finding_id, Scan.user_id == current_user.id).first()
        if not finding:
            raise HTTPException(status_code=404, detail="Finding not found")
        system, user = vulnerability_prompt(finding)
        result = await OpenRouterClient().complete(system, user)
        finding.ai_analysis = result
        db.commit()
        return {"analysis": result}

    if payload.prompt:
        result = await OpenRouterClient().complete("You are a cybersecurity assessment assistant.", payload.prompt[:4000])
        return {"analysis": result}

    raise HTTPException(status_code=400, detail="finding_id or prompt is required")


@router.post("/executive-summary/{scan_id}")
async def executive_summary(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    findings = db.query(Finding).filter(Finding.scan_id == scan.id).order_by(Finding.priority.desc()).all()
    system, user = executive_summary_prompt(findings)
    return {"summary": await OpenRouterClient().complete(system, user)}
