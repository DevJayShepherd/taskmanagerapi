from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from taskmanager.core.depends import get_db_session
from taskmanager.crud.tasks.task_manager_crud import TaskManager
from taskmanager.schema.tasks.task_schema import TaskCreate, TaskRead, TaskUpdate, TaskPartialUpdate

task_manager_router = APIRouter()


def get_manager(db: Session = Depends(get_db_session)) -> TaskManager:
    """Helper function to initialize the TaskManager."""
    return TaskManager(db)


@task_manager_router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, manager: TaskManager = Depends(get_manager)):
    """
    Create a new task.

    This endpoint allows users to create a task by providing task details.
    The task is stored in the system and returned as a response.

    Parameters:
    - task (TaskCreate): The data for creating a new task.
    - manager (TaskManager): The task manager instance for handling task operations.

    Returns:
    - TaskRead: The details of the newly created task.
    """
    # Validate task title to ensure it is not empty
    if len(task.title) == 0:
        raise HTTPException(status_code=422, detail="Must provide a title for the task")

    return manager.create_task(task)


@task_manager_router.get("/", response_model=List[TaskRead])
def get_tasks(completed: Optional[bool] = Query(None), manager: TaskManager = Depends(get_manager)):
    """
    Retrieve a list of tasks.

    This endpoint retrieves all tasks from the system. An optional filter
    can be applied to return tasks based on their completion status.

    Parameters:
    - completed (Optional[bool]): Filter to retrieve completed (`True`),
      incomplete (`False`), or all (`None`) tasks.
    - manager (TaskManager): The task manager instance for retrieving tasks.

    Returns:
    - List[TaskRead]: A list of tasks matching the filter criteria.
    """
    return manager.get_all_tasks(completed)


@task_manager_router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, manager: TaskManager = Depends(get_manager)):
    """
    Retrieve a specific task by its ID.

    This endpoint fetches details of a specific task using its unique identifier.
    If the task is not found, a 404 error is returned.

    Parameters:
    - task_id (str): The unique identifier of the task.
    - manager (TaskManager): The task manager instance for handling task retrieval.

    Returns:
    - TaskRead: The details of the requested task.
    Raises:
    - HTTPException: If the task with the given ID is not found (404).
    """
    task = manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_manager_router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_data: TaskUpdate, manager: TaskManager = Depends(get_manager)):
    """
    Update an existing task.

    This endpoint allows users to update all fields of a task identified
    by its ID. If the task does not exist, a 404 error is returned.

    Parameters:
    - task_id (str): The unique identifier of the task.
    - task_data (TaskUpdate): The updated task details.
    - manager (TaskManager): The task manager instance for handling updates.

    Returns:
    - TaskRead: The details of the updated task.
    Raises:
    - HTTPException: If the task with the given ID is not found (404).
    """
    task = manager.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_manager_router.patch("/{task_id}", response_model=TaskRead)
def partially_update_task(task_id: str, partial_data: TaskPartialUpdate, manager: TaskManager = Depends(get_manager)):
    """
    Partially update a task.

    This endpoint allows users to update specific fields of a task identified
    by its ID. If the task does not exist, a 404 error is returned.

    Parameters:
    - task_id (str): The unique identifier of the task.
    - partial_data (TaskPartialUpdate): The partial data for updating the task.
    - manager (TaskManager): The task manager instance for handling updates.

    Returns:
    - TaskRead: The details of the partially updated task.
    Raises:
    - HTTPException: If the task with the given ID is not found (404).
    """
    task = manager.partially_update_task(task_id, partial_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_manager_router.delete("/{task_id}")
def delete_task(task_id: str, manager: TaskManager = Depends(get_manager)):
    """
    Delete a task by its ID.

    This endpoint removes a task from the system based on its unique identifier.
    If the task does not exist, a 404 error is returned.

    Parameters:
    - task_id (str): The unique identifier of the task to delete.
    - manager (TaskManager): The task manager instance for handling deletions.

    Returns:
    - dict: A message indicating the task was successfully deleted.
    Raises:
    - HTTPException: If the task with the given ID is not found (404).
    """
    success = manager.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
