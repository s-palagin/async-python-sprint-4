import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from .mocks import TEST_LINKS, TEST_LINKS_ID, TESTS_COUNT


@pytest.mark.asyncio
async def test_create_item(
    client: AsyncClient, async_session: AsyncSession
) -> None:
    response = await client.post(
        app.url_path_for('create_links'),
        json=[{"long_link": TEST_LINKS[i]} for i in range(TESTS_COUNT)]
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), list)
    for item in response.json():
        assert 'id' in item, 'No "id" in answer'
        assert 'long_link' in item, 'No "long_link" in answer'
        TEST_LINKS_ID.update({item['id']: item['long_link']})
        assert 'short_link' in item, 'No "short_link" in answer'


@pytest.mark.asyncio
async def test_get_item(
    client: AsyncClient,
    async_session: AsyncSession
) -> None:
    for id in TEST_LINKS_ID:
        response = await client.get(
            app.url_path_for('get_link', id=id))
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT, (
            'Not redirect status')
        assert response.headers.get('location') == TEST_LINKS_ID.get(id), (
            'Uncorrect location in header')


@pytest.mark.asyncio
async def test_status_item(
    client: AsyncClient,
    async_session: AsyncSession
) -> None:
    for id in TEST_LINKS_ID:
        response = await client.get(app.url_path_for('get_acivity', id=id))
        assert response.status_code == status.HTTP_200_OK
        assert 'id' in response.json(), 'No "id" in answer'
        assert id == response.json().get('id'), f'Uncorrect id{id} in answer'
        assert 'amount' in response.json(), 'No "ammount" in answer'
        assert response.json().get('amount') == 1, 'Uncorrect ammount'
        assert 'activity' not in response.json(), (
            '"activity" in non-full answer')


@pytest.mark.asyncio
async def test_full_status(
    client: AsyncClient,
    async_session: AsyncSession
) -> None:
    for id in TEST_LINKS_ID:
        response = await client.get(
            app.url_path_for('get_acivity', id=id), params='full-info=yes')
        assert response.status_code == status.HTTP_200_OK
        assert 'activity' in response.json(), (
            'Not "activity" in full status answer')
        assert isinstance(response.json().get('activity'), list), (
            'Activity in answer must be list'
        )
        assert response.json().get('activity')[0].get('client'), (
            'Not "client" in activity list'
        )
        assert response.json().get('activity')[0].get('date'), (
            'Not "data" in activity list'
        )


@pytest.mark.asyncio
async def test_delete_item(
    client: AsyncClient,
    async_session: AsyncSession
) -> None:
    for id in TEST_LINKS_ID:
        response = await client.delete(app.url_path_for('delete_link', id=id))
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Uncorrect status after delete. Need 204'
        )


@pytest.mark.asyncio
async def test_get_after_delete(
    client: AsyncClient,
    async_session: AsyncSession
) -> None:
    for id in TEST_LINKS_ID:
        response = await client.get(
            app.url_path_for('get_link', id=id))
        assert response.status_code == status.HTTP_410_GONE, (
            'Uncorrect status for get deleted record. Need 410(GONE)'
        )
