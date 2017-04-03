from datetime import datetime

import pytest
import pytz
from dateutil.tz import tzlocal

from todoman.model import Todo, VtodoWritter


def test_serialize_created_at(todo_factory):
    now = datetime.now(tz=pytz.UTC)
    todo = todo_factory(created_at=now)
    vtodo = VtodoWritter(todo).serialize()

    assert vtodo.get('created') is not None


def test_serialize_dtstart(todo_factory):
    now = datetime.now(tz=pytz.UTC)
    todo = todo_factory(start=now)
    vtodo = VtodoWritter(todo).serialize()

    assert vtodo.get('dtstart') is not None


def test_serializer_raises(todo_factory):
    todo = todo_factory()
    writter = VtodoWritter(todo)

    with pytest.raises(Exception):
        writter.serialize_field('nonexistant', 7)


def test_supported_fields_are_serializeable():
    supported_fields = set(Todo.ALL_SUPPORTED_FIELDS)
    serialized_fields = set(VtodoWritter.FIELD_MAP.keys())

    assert supported_fields == serialized_fields


def test_vtodo_serialization(todo_factory):
    """Test VTODO serialization: one field of each type."""
    description = 'A tea would be nice, thanks.'
    todo = todo_factory(
        categories=['tea', 'drinking', 'hot'],
        description=description,
        due=datetime(3000, 3, 21),
        priority=7,
        status='IN-PROCESS',
        summary='Some tea',
    )
    writer = VtodoWritter(todo)
    vtodo = writer.serialize()

    assert str(vtodo.get('categories')) == 'tea,drinking,hot'
    assert str(vtodo.get('description')) == description
    assert vtodo.get('priority') == 7
    assert vtodo.decoded('due') == datetime(3000, 3, 21, tzinfo=tzlocal())
    assert str(vtodo.get('status')) == 'IN-PROCESS'