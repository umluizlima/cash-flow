from datetime import datetime
from decimal import Decimal

from pytest import fixture, raises
from sqlalchemy.orm.exc import NoResultFound

from app.core.models import Record
from app.core.repositories import RecordsRepository


@fixture(scope="function")
def repository(db):
    return RecordsRepository(db)


new_record = {
    "title": "title",
    "description": "description",
    "amount": Decimal(12.34),
    "happened_at": datetime.now(),
}


def test_create_should_return_record_instance(repository):
    record = repository.create(new_record)
    assert isinstance(record, Record)


def test_create_record_should_have_id(repository):
    record = repository.create(new_record)
    assert record.id


def test_create_record_should_have_given_attributes(repository):
    record = repository.create(new_record)
    assert record.title == new_record["title"]
    assert record.description == new_record["description"]
    assert record.amount == new_record["amount"]
    assert record.happened_at == new_record["happened_at"]


def test_create_records_should_be_persisted(repository):
    repository.create(new_record)
    repository.create(new_record)
    assert len(repository.find_all()) == 2


def test_find_all_should_return_list(repository):
    assert isinstance(repository.find_all(), list)


def test_find_all_should_return_existing_records(repository):
    record = repository.create(new_record)
    result = repository.find_all()
    assert result[0] == record


def test_find_by_id_should_return_record(repository):
    record = repository.create(new_record)
    result = repository.find_by_id(record.id)
    assert result.id == record.id


def test_find_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.find_by_id(123)


def test_update_by_id_should_update_record(repository):
    record = repository.create(new_record)
    updated_record = repository.update_by_id(record.id, {"title": "new title"})
    assert updated_record.title == "new title"


def test_update_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.update_by_id(123, {})


def test_delete_by_id_should_remove_record(repository):
    record = repository.create(new_record)
    repository.delete_by_id(record.id)
    assert record not in repository.find_all()


def test_delete_by_id_should_raise_exception_if_not_found(repository):
    with raises(NoResultFound):
        repository.delete_by_id(123)
