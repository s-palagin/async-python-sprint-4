import pytest
from fastapi import status
from fastapi.testclient import TestClient

from .main import app


@pytest.fixture(scope='module')
def client() -> TestClient:
    with TestClient(app) as client:
        yield client


TESTS_COUNT = 3
TEST_LINKS = [
    f'http://test_{i}_test.py' for i in range(TESTS_COUNT)
]
TEST_LINKS_ID = {}


def test_create_item(client: TestClient) -> None:
    response = client.post(
        'api/v1/',
        json=[{"long_link": TEST_LINKS[i]} for i in range(TESTS_COUNT)]
    )

    assert response.status_code == 201
    assert isinstance(response.json(), list)
    for item in response.json():
        assert 'id' in item, 'No "id" in answer'
        assert 'long_link' in item, 'No "long_link" in answer'
        TEST_LINKS_ID.update({item['id']: item['long_link']})
        assert 'short_link' in item, 'No "short_link" in answer'


def test_get_item(client: TestClient) -> None:
    for id in TEST_LINKS_ID:
        response = client.get(f'api/v1/{id}', allow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT, (
            'Not redirect status')
        assert response.headers.get('location') == TEST_LINKS_ID.get(id), (
            'Uncorrect location in header')


def test_status_item(client: TestClient) -> None:
    for id in TEST_LINKS_ID:
        response = client.get(f'api/v1/{id}/status')
        assert response.status_code == status.HTTP_200_OK
        assert 'id' in response.json(), 'No "id" in answer'
        assert id == response.json().get('id'), f'Uncorrect id{id} in answer'
        assert 'amount' in response.json(), 'No "ammount" in answer'
        assert response.json().get('amount') == 1, 'Uncorrect ammount'
        assert 'activity' not in response.json(), (
            '"activity" in non-full answer')


def test_full_status(client: TestClient) -> None:
    for id in TEST_LINKS_ID:
        response = client.get(f'api/v1/{id}/status', params='full-info=yes')
        assert response.status_code == status.HTTP_200_OK
        assert 'activity' in response.json(), (
            'Not "activity" in full status answer')
        assert isinstance(response.json().get('activity'), list)
        assert 'testclient' in response.json().get('activity')[0].get('client')


def test_delete_item(client: TestClient) -> None:
    for id in TEST_LINKS_ID:
        response = client.delete(f'api/v1/{id}')
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Uncorrect status after delete. Need 204'
        )


def test_get_after_delete(client: TestClient) -> None:
    for id in TEST_LINKS_ID:
        response = client.get(f'api/v1/{id}', allow_redirects=False)
        assert response.status_code == status.HTTP_410_GONE, (
            'Uncorrect status for get deleted record. Need 410(GONE)'
        )
