from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Mapping(Base):
    __tablename__ = "mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String, unique=True, index=True, nullable=False)
    target = Column(Text, nullable=False)
    action_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint(action_type.in_(['app', 'url', 'system_cmd'])),
    )

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False, server_default=func.now())
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class CommandLog(Base):
    __tablename__ = "command_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    intent = Column(String, nullable=False)
    action = Column(String, nullable=False)
    status = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(status.in_(['SUCCESS', 'FAILED', 'CANCELLED'])),
    )

class AuthKey(Base):
    __tablename__ = "auth_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key_value = Column(String, unique=True, index=True, nullable=False)
    label = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_used = Column(DateTime, nullable=True)
