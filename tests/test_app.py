import pytest
from src.app import app  # , get_docker_labels

# from src.config import config


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


# passes locally but not on github actions
# def test_docker_label_parsing(client):
#     config.set("FLIP_FLOP_DEV_MODE", True)
#     data = get_docker_labels()
#     assert data == [
#         {
#             "name": "App 1",
#             "url": "https://example.com/app1",
#             "icon": "7dadd3de8c5a3e18dbc9867aeb8292d4.png",
#             "priority": 9999,
#         },
#     ]
