import pytest
from fastapi.testclient import TestClient

from taskmanager.api.v1.tasks.task_router import task_manager_router, get_manager
from taskmanager.crud.tasks.task_manager_crud import TaskManager
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

def test_delete_task_success(override_get_manager):
    """
    Test deleting a task successfully.
    """
    # Mock TaskManager response
    override_get_manager.delete_task.return_value = True

    # Perform DELETE request
    response = client.delete("/tasks/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}
    override_get_manager.delete_task.assert_called_once_with("1")

def test_delete_task_not_found(override_get_manager):
    """
    Test deleting a task that does not exist.
    """
    # Mock TaskManager to return False for a nonexistent task
    override_get_manager.delete_task.return_value = False

    # Perform DELETE request
    response = client.delete("/tasks/999")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    override_get_manager.delete_task.assert_called_once_with("999")
