from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from sqlalchemy.sql import func

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True, nullable=False)
    user_id = Column(Integer, nullable=True) # Optional, as failed logins might not have a valid user_id
    details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
