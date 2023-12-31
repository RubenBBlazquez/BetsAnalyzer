import os
import subprocess

import pytest
from common.db_client.mongo_db_client import MongoDBConnection

DOCKER_COMPOSE_FILE = os.path.join(os.path.dirname(__file__), "docker-compose.yaml")


@pytest.fixture
def mongo_db_conn():
    return MongoDBConnection().db_conn


def pytest_sessionstart(session):
    os.environ.update(
        {
            "MONGO_HOST": "localhost",
            "MONGO_PORT": "27019",
            "MONGO_USER": "root",
            "MONGO_PASSWORD": "root",
            "MONGO_AUTH_DATABASE": "admin",
            "PROJECT_DATABASE": "sport_monks_prueba",
        }
    )
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--build"], check=True)


def pytest_sessionfinish(session, exitstatus):
    MongoDBConnection().db_conn.drop_database("sport_monks_prueba")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "down", "-v"], check=True)
