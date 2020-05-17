from pydantic.error_wrappers import ValidationError
from pytest import raises

from app.api.schemas import RecordCreate, RecordRead, RecordUpdate

new_record = {
    "amount": 12.34,
    "title": "title",
    "description": "description",
    "happened_at": "2020-05-16T18:00:00",
}


def test_record_create_must_have_amount():
    new_record_without_amount = {**new_record}
    del new_record_without_amount["amount"]
    with raises(ValidationError):
        RecordCreate(**new_record_without_amount)


def test_record_update_has_no_required_args():
    record_update = RecordUpdate()
    assert record_update.dict(exclude_unset=True) == {}


def test_read_must_have_id():
    with raises(ValidationError):
        RecordRead(**new_record)


def test_record_title_must_be_shorter_than_51():
    long_title = 51 * "a"
    with raises(ValidationError):
        RecordUpdate(title=long_title)


def test_record_title_must_be_longer_than_2():
    short_title = 2 * "a"
    with raises(ValidationError):
        RecordUpdate(title=short_title)


def test_record_description_must_be_shorter_than_141():
    long_description = 141 * "a"
    with raises(ValidationError):
        RecordUpdate(description=long_description)


def test_record_amount_must_have_2_decimal_places():
    amount = 12.345
    with raises(ValidationError):
        RecordUpdate(amount=amount)


def test_record_happened_at_must_have_datetime_format():
    happened_at = "abc"
    with raises(ValidationError):
        RecordUpdate(happened_at=happened_at)
