import uuid
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(100), index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")
