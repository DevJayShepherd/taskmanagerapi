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
def sample_tasks():
    """Fixture to provide a sample list of tasks."""
    return [
        TaskRead(id="1", title="Task 1", description="First task", completed=True),
        TaskRead(id="2", title="Task 2", description="Second task", completed=False),
        TaskRead(id="3", title="Task 3", description="Third task", completed=True),
    ]


def test_get_all_tasks(override_get_manager, sample_tasks):
    """
    Test retrieving all tasks without filters.
    """
    # Mock TaskManager response
    override_get_manager.get_all_tasks.return_value = sample_tasks

    # Perform GET request
    response = client.get("/tasks/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "title": "Task 1",
         "description": "First task", "completed": True},
        {"id": "2", "title": "Task 2",
         "description": "Second task", "completed": False},
        {"id": "3", "title": "Task 3",
         "description": "Third task", "completed": True},
    ]
    override_get_manager.get_all_tasks.assert_called_once_with(None)


def test_get_completed_tasks(override_get_manager, sample_tasks):
    """
    Test retrieving only completed tasks.
    """
    # Mock TaskManager response
    override_get_manager.get_all_tasks.return_value = [
        task for task in sample_tasks if task.completed
    ]

    # Perform GET request with filter
    response = client.get("/tasks/", params={"completed": True})

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "title": "Task 1", "description": "First task", "completed": True},
        {"id": "3", "title": "Task 3", "description": "Third task", "completed": True},
    ]
    override_get_manager.get_all_tasks.assert_called_once_with(True)


def test_get_incomplete_tasks(override_get_manager, sample_tasks):
    """
    Test retrieving only incomplete tasks.
    """
    # Mock TaskManager response
    override_get_manager.get_all_tasks.return_value = [
        task for task in sample_tasks if not task.completed
    ]

    # Perform GET request with filter
    response = client.get("/tasks/", params={"completed": False})

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"id": "2", "title": "Task 2",
         "description": "Second task", "completed": False},
    ]
    override_get_manager.get_all_tasks.assert_called_once_with(False)


def test_get_tasks_empty_list(override_get_manager):
    """
    Test retrieving tasks when no tasks are present.
    """
    # Mock TaskManager response
    override_get_manager.get_all_tasks.return_value = []

    # Perform GET request
    response = client.get("/tasks/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == []
    override_get_manager.get_all_tasks.assert_called_once_with(None)
