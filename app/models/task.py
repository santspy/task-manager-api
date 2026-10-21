from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class TaskModel(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  description = Column(String, nullable=True)
  status = Column(String, default="Pendente")
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer, ForeignKey("users.id"))

  owner = relationship("UserModel", back_populates="tasks")