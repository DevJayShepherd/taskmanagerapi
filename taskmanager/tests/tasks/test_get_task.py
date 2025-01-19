import pytest
from fastapi.testclient import TestClient

from taskmanager.api.v1.tasks.task_router import task_manager_router, get_manager
from taskmanager.crud.tasks.task_manager_crud import TaskManager
from taskmanager.schema.tasks.task_schema import TaskRead
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
        title="Sample Task",
        description="This is a sample task.",
        completed=False
    )

def test_get_task_success(override_get_manager, sample_task):
    """
    Test retrieving a specific task by ID successfully.
    """
    # Mock TaskManager response
    override_get_manager.get_task_by_id.return_value = sample_task

    # Perform GET request
    response = client.get("/tasks/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "Sample Task",
        "description": "This is a sample task.",
        "completed": False,
    }
    override_get_manager.get_task_by_id.assert_called_once_with("1")

def test_get_task_not_found(override_get_manager):
    """
    Test retrieving a task that does not exist.
    """
    # Mock TaskManager to return None for a nonexistent task
    override_get_manager.get_task_by_id.return_value = None

    # Perform GET request
    response = client.get("/tasks/999")  # Use a nonexistent task ID

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    override_get_manager.get_task_by_id.assert_called_once_with("999")
