from warnings import warn

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture

from .utils import find_link
from .warnings import StatSpecWarning


@fixture
def data(stat_client: TestClient):
    res = stat_client.get("/")

    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == "application/json"

    yield res.json()


def test_root(stat_client: TestClient, url_for):
    res = stat_client.get("/")

    assert res.status_code == status.HTTP_200_OK
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()

    link = find_link(data["links"], "self")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=self] should exist"))
    else:
        assert link["type"] == "application/json"
        assert link["href"] == url_for("/")

    link = find_link(data["links"], "service-description")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-description] should exist"))

    else:
        assert link["type"] == "application/json"
        assert str(link["href"]) == url_for("/openapi.json")

    link = find_link(data["links"], "service-docs")
    if link is None:
        warn(StatSpecWarning("GET / Link[rel=service-docs] should exist"))
    else:
        assert link["type"] == "text/html"
        assert str(link["href"]) == url_for("/docs")
