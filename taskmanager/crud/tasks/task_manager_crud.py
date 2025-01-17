from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from typing import List, Optional

from taskmanager.models.tasks.task_models import Task
from taskmanager.schema.tasks.task_schema import TaskCreate, TaskUpdate, TaskPartialUpdate


class TaskManager:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        new_task = Task(**task_data.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_all_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Retrieve a list of tasks, with optional filtering by completed status."""
        query = self.db.query(Task)
        if completed is not None:
            query = query.filter(Task.completed == completed)
        return query.all()

    def get_task_by_id(self, task_id: str) -> Task:
        """Retrieve a task by its ID."""
        try:
            return self.db.query(Task).filter(Task.id == task_id).one()
        except NoResultFound:
            return None

    def update_task(self, task_id: str, updated_data: TaskUpdate) -> Task:
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def partially_update_task(self, task_id: str, partial_data: TaskPartialUpdate) -> Task:
        """Partially update a task."""
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        for key, value in partial_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True
