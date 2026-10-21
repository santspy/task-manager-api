from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.task import TaskModel
from app.models.user import UserModel
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/tasks", tags=["Tarefas"])


@router.post("/", status_code=201)
def create_task(
    task: TaskCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
  db_task = TaskModel(
      title=task.title, description=task.description, user_id=current_user.id
  )
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return {
      "message": "Tarefa criada com sucesso!",
      "task_id": db_task.id,
      "title": db_task.title,
  }


@router.get("/")
def list_tasks(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
  tasks = db.query(TaskModel).filter(TaskModel.user_id == current_user.id).all()
  return tasks