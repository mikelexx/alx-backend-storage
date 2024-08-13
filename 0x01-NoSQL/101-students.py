#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted
by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns
with key = averageScore
"""


def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """

    pipeline = [{
        "$unwind": "$topics"
    }, {
        "$group": {
            "_id": "$name",
            "firstId": {
                "$first": "$_id"
            },
            "averageScore": {
                "$avg": "$topics.score"
            }
        }
    }, {
        "$project": {
            "_id": "$firstId",
            "name": "$_id",
            "averageScore": 1
        }
    }, {
        "$sort": {
            "averageScore": -1
        }
    }]
    return mongo_collection.aggregate(pipeline)
