from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.api import api
from app.api.schemas import RecordCreate, RecordRead, RecordUpdate
from app.core.database import get_db
from app.core.models import Record
from app.core.repositories import RecordsRepository


def mock_get_db():
    return MagicMock()


api.dependency_overrides[get_db] = mock_get_db

record_dict_1 = {
    "title": "Title 1",
    "description": "Description 1",
    "amount": 10,
    "happened_at": "2020-05-02T12:00:00",
}
record_1 = Record(id=1, **record_dict_1)
record_dict_2 = {
    "title": "Title 2",
    "description": "Description 2",
    "amount": 25.12,
    "happened_at": "2020-05-03T12:00:00",
}
record_2 = Record(id=2, **record_dict_2)


@fixture(scope="function")
def list_response(client):
    RecordsRepository.find_all = MagicMock(return_value=[record_1, record_2])
    yield client.get("/records")
    RecordsRepository.find_all.assert_called_once()


def test_list_should_return_status_200(list_response):
    assert list_response.status_code == HTTP_200_OK


def test_list_should_return_json(list_response):
    assert list_response.headers["Content-Type"] == "application/json"


def test_list_should_return_list(list_response):
    assert isinstance(list_response.json(), list)


def test_listed_record_should_have_id(list_response):
    assert "id" in list_response.json().pop()


def test_listed_record_should_have_title(list_response):
    assert "title" in list_response.json().pop()


def test_listed_record_should_have_description(list_response):
    assert "description" in list_response.json().pop()


def test_listed_record_should_have_happened_at(list_response):
    assert "happened_at" in list_response.json().pop()


def test_listed_record_should_have_amount(list_response):
    assert "amount" in list_response.json().pop()


def test_listed_records_should_be_ordered_by_happened_at(list_response):
    assert list_response.json()[0]["happened_at"] == record_dict_2["happened_at"]


@fixture(scope="function")
def read_response(client):
    RecordsRepository.find_by_id = MagicMock(return_value=record_1)
    yield client.get(f"/records/{record_1.id}")
    RecordsRepository.find_by_id.assert_called_once_with(record_1.id)


def test_read_endpoint_should_accept_get(read_response):
    assert read_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_read_should_return_status_200_if_record_found(read_response):
    assert read_response.status_code == HTTP_200_OK


def test_read_record_should_return_record_if_found(read_response):
    response_record = Record(**read_response.json())
    assert response_record.id == record_1.id
    assert response_record.title == record_1.title
    assert response_record.description == record_1.description
    assert response_record.amount == record_1.amount
    assert response_record.happened_at == record_1.happened_at


def test_read_should_return_status_404_if_record_not_found(client):
    RecordsRepository.find_by_id = MagicMock(side_effect=Exception)
    response = client.get(f"/records/{record_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    RecordsRepository.find_by_id.assert_called_once_with(record_1.id)


@fixture(scope="function")
def create_response(client):
    RecordsRepository.create = MagicMock(return_value=record_1)
    yield client.post("/records", json=record_dict_1)
    RecordsRepository.create.assert_called_once_with(
        RecordCreate(**record_dict_1).dict()
    )


def test_create_record_endpoint_should_accept_post(create_response):
    assert create_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_create_record_should_have_amount(client):
    response = client.post("/records", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_create_record_should_return_record(create_response):
    assert create_response.json()["id"] == record_1.id


def test_created_record_should_return_status_201(create_response):
    assert create_response.status_code == HTTP_201_CREATED


@fixture(scope="function")
def delete_response(client):
    RecordsRepository.delete_by_id = MagicMock()
    yield client.delete(f"/records/{record_1.id}")
    RecordsRepository.delete_by_id.assert_called_once_with(record_1.id)


def test_delete_record_endpoint_should_accept_delete(delete_response):
    assert delete_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_delete_record_should_return_status_204(delete_response):
    assert delete_response.status_code == HTTP_204_NO_CONTENT


def test_delete_record_should_return_status_404_if_record_not_found(client):
    RecordsRepository.delete_by_id = MagicMock(side_effect=Exception)
    response = client.delete(f"/records/{record_1.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    RecordsRepository.delete_by_id.assert_called_once_with(record_1.id)


@fixture(scope="function")
def update_response(client):
    RecordsRepository.update_by_id = MagicMock(return_value=record_1)
    yield client.put(f"/records/{record_1.id}", json=record_dict_1)
    RecordsRepository.update_by_id.assert_called_once_with(
        record_1.id, RecordUpdate(**record_dict_1).dict()
    )


def test_update_record_endpoint_should_accept_put(update_response):
    assert update_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_update_record_should_return_status_404_if_record_not_found(client):
    RecordsRepository.update_by_id = MagicMock(side_effect=Exception)
    response = client.put(f"/records/{record_1.id}", json=record_dict_1)
    assert response.status_code == HTTP_404_NOT_FOUND
    RecordsRepository.update_by_id.assert_called_once_with(
        record_1.id, RecordUpdate(**record_dict_1).dict()
    )


def test_update_record_should_not_have_required_fields(client):
    response = client.put(f"/records/{record_1.id}", json={})
    assert response.status_code != HTTP_422_UNPROCESSABLE_ENTITY


def test_update_record_should_return_updated_record(update_response):
    assert update_response.json()["title"] == record_dict_1["title"]


def test_update_record_should_ignore_unknown_fields(client):
    update_data = {"key": "value", **record_dict_1}
    RecordsRepository.update_by_id = MagicMock(return_value=record_1)
    client.put(f"/records/{record_1.id}", json=update_data)
    RecordsRepository.update_by_id.assert_called_once_with(
        record_1.id, RecordUpdate(**record_dict_1).dict()
    )


def test_update_record_should_return_status_200_if_successful(update_response):
    assert update_response.status_code == HTTP_200_OK
