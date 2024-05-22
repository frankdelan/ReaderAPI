import pytest

from api.books.schemas import BookAdd
from tests.conftest import USER_ID


@pytest.mark.usefixtures('setup_database')
class TestSuccessAPI:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_book_by_id(self, get_client, user_id, add_test_data):
        """Тест успешных запросов к  API на получение книги по id"""
        response = await get_client.get(f"/book/{add_test_data['data']['id']}?user_id={user_id}")
        assert response.status_code == 200
        assert response.json() == add_test_data

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_book_list(self, get_client, user_id, add_test_data):
        """Тест успешных запросов к  API на получение списка книг пользователя"""
        response = await get_client.get(f"/book/list?user_id={user_id}")
        assert response.status_code == 200
        assert response.json()['data'] == [add_test_data['data']]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("data, user_id", [
        (BookAdd(title="Dubrovskiy", author="Pushkin", volume=300), USER_ID)
    ])
    async def test_add_book(self, get_client, data, user_id, add_test_data):
        """Тест успешных запросов к API на добавление книги"""
        response_post = await get_client.post(f"/book/add?user_id={user_id}",
                                         json={"title": data.title,
                                               "author": data.author,
                                               "volume": data.volume})
        response_get = await get_client.get(f"/book/{response_post.json()['data']['id']}?user_id={user_id}")
        assert response_post.status_code == 200
        assert response_post.json() == response_get.json()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id, current_page", [
        (USER_ID, 150),
    ])
    async def test_change_progress(self, get_client, user_id, current_page, add_test_data):
        """Тест успешных запросов к  API на изменение прогресса чтения книги"""
        response_patch = await get_client.patch(f"/book/progress/{add_test_data['data']['id']}?user_id={user_id}&current_page={current_page}")
        response_get = await get_client.get(f"/book/{add_test_data['data']['id']}?user_id={user_id}")
        assert response_patch.status_code == 200
        assert response_patch.json()['data'] == response_get.json()['data']

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_delete_book(self, get_client, user_id, add_test_data):
        """Тест успешных запросов API на удаление книги по id"""
        await get_client.delete(f"/book/delete/{add_test_data['data']['id']}?user_id={user_id}")
        response_get = await get_client.get(f"/book/{add_test_data['data']['id']}?user_id={user_id}")
        assert response_get.status_code == 404


@pytest.mark.usefixtures('setup_database')
class TestErrorAPI:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("book_id, user_id", [
        (1, 2), (10, 1), ('5', '5'), (5, ''), ('', 5), ('', '')
    ])
    async def test_book_by_id(self, get_client, book_id, user_id, add_test_data):
        """
        Тест успешных запросов API на получение книги по id.
        Если не передан только один параметр user_id - 422, в других случаях 404.
        """
        response = await get_client.get(f"/book/{book_id}?user_id={user_id}")
        if not user_id and book_id:
            assert response.status_code == 422
        else:
            assert response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [5, '6', ''])
    async def test_book_list(self, get_client, user_id):
        """Тест ошибок в запросах к API на получение списка книг пользователя"""
        response = await get_client.get(f"/book/list?user_id={user_id}")
        if user_id:
            assert response.status_code == 404
        else:
            assert response.status_code == 422



