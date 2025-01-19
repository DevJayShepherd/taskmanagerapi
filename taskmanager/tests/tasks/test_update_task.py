import pytest
from fastapi.testclient import TestClient

from taskmanager.api.v1.tasks.task_router import task_manager_router, get_manager
from taskmanager.crud.tasks.task_manager_crud import TaskManager
from taskmanager.schema.tasks.task_schema import TaskUpdate, TaskRead
from unittest.mock import MagicMock
from fastapi import FastAPI

# Setup FastAPI application
app = FastAPI()
app.include_router(task_manager_router, prefix="/tasks")

client = TestClient(app)

@pytest.fixture
def mocked_task_manager():
    """Fixture to mock the TaskManager."""
    return MagicMock(spec=TaskManager)

@pytest.fixture
def override_get_manager(mocked_task_manager):
    """Fixture to override the TaskManager dependency."""
    app.dependency_overrides[get_manager] = lambda: mocked_task_manager
    yield mocked_task_manager
    app.dependency_overrides.clear()

@pytest.fixture
def sample_task():
    """Fixture to provide a sample task."""
    return TaskRead(
        id="1",
        title="Updated Task",
        description="This is the updated task description.",
        completed=True,
    )

@pytest.fixture
def task_update_request():
    """Fixture to provide valid task update input."""
    return TaskUpdate(
        title="Updated Task",
        description="This is the updated task description.",
        completed=True,
    )

def test_update_task_success(override_get_manager, sample_task, task_update_request):
    """
    Test updating a task successfully.
    """
    # Mock TaskManager response
    override_get_manager.update_task.return_value = sample_task

    # Perform PUT request
    response = client.put(
        "/tasks/1",
        json={
            "title": task_update_request.title,
            "description": task_update_request.description,
            "completed": task_update_request.completed,
        },
    )

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "Updated Task",
        "description": "This is the updated task description.",
        "completed": True,
    }
    override_get_manager.update_task.assert_called_once_with("1", task_update_request)

def test_update_task_not_found(override_get_manager, task_update_request):
    """
    Test updating a task that does not exist.
    """
    # Mock TaskManager to return None for a nonexistent task
    override_get_manager.update_task.return_value = None

    # Perform PUT request
    response = client.put(
        "/tasks/999",
        json={
            "title": task_update_request.title,
            "description": task_update_request.description,
            "completed": task_update_request.completed,
        },
    )

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    override_get_manager.update_task.assert_called_once_with("999", task_update_request)
