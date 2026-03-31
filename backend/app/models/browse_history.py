from sqlalchemy import Column, BigInteger, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class BrowseHistory(Base):
    __tablename__ = "browse_histories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    browse_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="browse_histories")
    product = relationship("Product", backref="browse_histories")
