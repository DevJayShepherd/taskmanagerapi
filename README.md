# Task Manager API
This is a FastAPI-based project for managing tasks.

## Getting Started

Follow the steps below to set up the project on your local machine.

---

### Prerequisites
Ensure you have the following installed:
- [Python 3.12+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

---

### Installation

#### Clone the Repository
Clone the repository and navigate to the project directory.
```bash
git clone https://github.com/DevJayShepherd/taskmanagerapi.git
cd taskmanager
```

#### Create Your `.env` File
Copy the provided `env-example` file to a `.env` file and update it with your local configuration.
```bash
cp .env-example .env
```

#### Install Dependencies
Install project dependencies using Poetry.
```bash
make install
```

#### Apply Database Migrations
Run Alembic migrations to set up the database schema.
```bash
make migrate
```
---

### Running the Application

Start the FastAPI application locally with hot-reloading.
```bash
make run
```

### Code Quality and Testing
Run the following command to run tests and check code quality.
```bash
make lint
```

Run the following command to run tests only.
```bash
make test
```

The API will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`
