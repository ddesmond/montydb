
import pytest

from montydb import MontyCollection
from montydb.errors import OperationFailure


def test_database_name(monty_database):
    assert monty_database.name == "test_db"


def test_database_client(monty_database, monty_client):
    assert monty_database.client == monty_client


def test_database_getitem(monty_database):
    col = monty_database["test_col_get_item"]
    assert isinstance(col, MontyCollection)
    assert col.name == "test_col_get_item"


def test_database_get_collection(monty_database):
    col = monty_database.get_collection("test_col_get")
    assert isinstance(col, MontyCollection)
    assert col.name == "test_col_get"

    with pytest.raises(OperationFailure):
        monty_database.get_collection("$test")

    with pytest.raises(OperationFailure):
        monty_database.get_collection("system.")


def test_database_collection_names(monty_database, mongo_database):
    col_names = ["test1", "test2"]

    for col in col_names:
        monty_database.create_collection(col)
        mongo_database.create_collection(col)

    monty_col_names = monty_database.collection_names()
    mongo_col_names = mongo_database.collection_names()
    assert monty_col_names == mongo_col_names


def test_database_create_colllection(monty_database):
    col = monty_database.create_collection("create_collection_test")
    assert isinstance(col, MontyCollection)
    assert col.name == "create_collection_test"


def test_database_drop_colllection(monty_database):
    monty_database.create_collection("drop_me")
    assert "drop_me" in monty_database.collection_names()
    monty_database.drop_collection("drop_me")
    assert "drop_me" not in monty_database.collection_names()

    db_inst = monty_database.create_collection("drop_col_inst")
    assert "drop_col_inst" in monty_database.collection_names()
    monty_database.drop_collection(db_inst)
    assert "drop_col_inst" not in monty_database.collection_names()

    with pytest.raises(TypeError):
        monty_database.drop_collection(0)
