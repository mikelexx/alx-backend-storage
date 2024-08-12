#!/usr/bin/env python3
"""
Write a Python script that provides some stats about
Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
"""
from pymongo import MongoClient

client = MongoClient()
db = client.logs
collection = db.nginx
rows = collection.find()
print("{} logs".format(rows.count()))
print("Methods:")
for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
    print("\tmethod {}: {}".format(method,
                                   collection.find({
                                       "method": method
                                   }).count()))
print("{} status check".format(
    collection.find({
        "method": 'GET',
        'path': '/status'
    }).count()))
