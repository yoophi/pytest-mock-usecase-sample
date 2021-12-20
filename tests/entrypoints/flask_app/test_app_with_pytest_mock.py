import pytest

from app.entrypoints.flask_app import create_app
from app.request_objects import InvalidRequestObject
from app.response_objects import ResponseSuccess, ResponseFailure
from app.use_cases.hello import HelloUseCase


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


def test(client):
    resp = client.get("/")
    assert resp.status_code == 404


def test_hello(client, mocker):
    mocker.patch("app.use_cases.hello")
    mock_func = mocker.patch.object(
        HelloUseCase, "execute", return_value=ResponseSuccess(value="Tom")
    )
    resp = client.get("/api/hello")
    mock_func.assert_called()
    assert resp.status_code == 200


def test_hello_resource_error(client, mocker):
    mocker.patch("app.use_cases.hello")
    mock_func = mocker.patch.object(
        HelloUseCase,
        "execute",
        return_value=ResponseFailure.build_resource_error("not found"),
    )
    resp = client.get("/api/hello")
    mock_func.assert_called()
    assert resp.status_code == 404


def test_hello_invalid_request(client, mocker):
    mocker.patch("app.use_cases.hello")
    invalid_ro = InvalidRequestObject()
    invalid_ro.add_error("invalid", "data is not valid")

    mock_func = mocker.patch.object(
        HelloUseCase,
        "execute",
        return_value=ResponseFailure.build_from_invalid_request_object(invalid_ro),
    )
    resp = client.get("/api/hello")
    mock_func.assert_called()
    assert resp.status_code == 400
