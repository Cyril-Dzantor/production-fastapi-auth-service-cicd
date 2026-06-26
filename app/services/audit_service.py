from sqlalchemy.orm import Session
from app.models.audit import AuditLog
import json

def log_event(db: Session, event_type: str, user_id: int | None = None, details: dict | None = None):
    """
    Log an authentication-related event to the database.
    """
    details_str = json.dumps(details) if details else None
    audit_log = AuditLog(
        event_type=event_type,
        user_id=user_id,
        details=details_str
    )
    db.add(audit_log)
    db.commit()
