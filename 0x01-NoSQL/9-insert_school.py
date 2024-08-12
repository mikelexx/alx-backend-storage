#!/usr/bin/env python3
"""
Write a Python function that inserts a new document in
a collection based on kwargs:

    Prototype: def insert_school(mongo_collection, **kwargs):
    mongo_collection will be the pymongo collection object
    Returns the new _id
"""
from typing import Any
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs: dict) -> Any:
    """
    inserts a new document in a collection based on kwargs
    """
    return mongo_collection.insert_one(kwargs).inserted_id
