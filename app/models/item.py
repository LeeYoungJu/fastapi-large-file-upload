from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(1000), index=True)
    owner_id = Column(String(120), ForeignKey("user.id"))

    owner = relationship("User", back_populates="items")
