import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from taskmanager.api.v1.tasks.task_router import task_manager_router, get_manager
from taskmanager.crud.tasks.task_manager_crud import TaskManager
from taskmanager.schema.tasks.task_schema import TaskCreate, TaskRead
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
def task_create_request():
    """Fixture to provide valid task creation input."""
    return TaskCreate(title="Sample Task", description="This is a sample task.")


def test_create_task_success(override_get_manager, task_create_request):
    """
    Test the successful creation of a task.
    """
    # Mock TaskManager response
    override_get_manager.create_task.return_value = TaskRead(
        id="1",
        title=task_create_request.title,
        description=task_create_request.description,
        completed=False
    )

    # Perform POST request
    response = client.post(
        "/tasks/",
        json={"title": task_create_request.title,
              "description": task_create_request.description},
    )

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": task_create_request.title,
        "description": task_create_request.description,
        "completed": False,
    }
    override_get_manager.create_task.assert_called_once_with(task_create_request)


def test_create_task_validation_error():
    """
    Test creating a task with invalid input.
    """
    # Perform POST request with invalid input
    response = client.post("/tasks/", json={"title": ""})  # Missing required fields

    # Assertions
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_task_manager_failure(override_get_manager, task_create_request):
    """
    Test the behavior when the TaskManager fails to create a task.
    """
    # Mock TaskManager to raise HTTPException
    override_get_manager.create_task.side_effect = HTTPException(
        status_code=400, detail="Task creation failed"
    )

    # Perform POST request
    response = client.post(
        "/tasks/",
        json={"title": task_create_request.title,
              "description": task_create_request.description},
    )

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Task creation failed"}
    override_get_manager.create_task.assert_called_once_with(task_create_request)
