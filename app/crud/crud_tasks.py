from sqlmodel import Session, select
from app.models.model_tasks import Task

def get_tasks(session: Session, offset: int = 0, limit: int = 100) -> list[Task]:
    """Retorna lista de tarefas com paginação."""
    return session.exec(select(Task).offset(offset).limit(limit)).all()


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    """Retorna uma tarefa pelo ID ou None se não existir."""
    return session.get(Task, task_id)


def get_task_by_title(session: Session, title: str) -> Task | None:
    """Retorna uma tarefa pelo título ou None se não existir."""
    return session.exec(select(Task).where(Task.title == title)).first()


def create_task(session: Session, title: str, description: str) -> Task:
    """Cria uma nova tarefa no banco de dados."""
    db_task = Task(title=title, description=description)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def update_task(session: Session, task_id: int, title: str, description: str) -> Task | None:
    """Atualiza uma tarefa existente. Retorna None se não encontrar."""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    db_task.title = title
    db_task.description = description
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    """Deleta uma tarefa. Retorna True se deletou, False se não encontrou."""
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True