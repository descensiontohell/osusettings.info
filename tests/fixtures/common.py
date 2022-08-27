from pytest import fixture

from tests.client import Client


@fixture(scope="session", autouse=True)
def client():
    yield Client()
