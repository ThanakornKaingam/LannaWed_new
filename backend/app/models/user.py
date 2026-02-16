from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # =========================
    # Primary Key
    # =========================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # =========================
    # Authentication
    # =========================
    email = Column(String, unique=True, nullable=False, index=True)

    # password hash (nullable for Google users)
    password = Column(String, nullable=True)

    # Google OAuth
    google_id = Column(String, nullable=True, unique=True)

    # =========================
    # Account Info
    # =========================
    full_name = Column(String, nullable=True)

    role = Column(String, default="user")

    # =========================
    # Account Status
    # =========================
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # =========================
    # Password Reset
    # =========================
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    # =========================
    # Timestamps
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
