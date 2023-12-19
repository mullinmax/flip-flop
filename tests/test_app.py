from unittest.mock import patch, MagicMock
import pytest
from src.app import app


@pytest.fixture(scope="function")
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_environment_config(client):
    assert app.config["TESTING"] is True


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<head>" in str(response.data)
    assert "stylesheet" in str(response.data)
    assert "<script src=" in str(response.data)


def test_static_files(client):
    css_response = client.get("/static/css/index.css")
    assert css_response.status_code == 200
    js_response = client.get("/static/js/index.js")
    assert js_response.status_code == 200


@pytest.fixture
def mock_docker():
    with patch("docker.from_env") as mock:
        yield mock


@patch("src.app.is_docker_socket_available", return_value=True)
@patch("docker.from_env")
def test_docker_label_parsing(mock_docker_env, mock_socket_avail, client):
    mock_container = MagicMock()
    mock_container.name = "mock_container"
    mock_container.labels = {
        "flip-flop.instances": "a,b,c,default",
        "flip-flop.name": "example",
        "flip-flop.url": "http://example.com",
        "flip-flop.icon": "🔥",
        "flip-flop.priority": 5,
    }
    mock_docker_env.return_value.containers.list.return_value = [mock_container]

    labels_response = client.get("/docker-labels")
    assert labels_response.status_code == 200
    data = labels_response.json
    assert data == [
        {"name": "example", "url": "http://example.com", "icon": "🔥", "priority": 5}
    ]
