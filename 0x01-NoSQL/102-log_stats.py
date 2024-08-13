#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the
most present IPs in the collection nginx of the database
logs:

The IPs top must be sorted (like the example below)
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
print("IPs:")
for row in collection.aggregate([{
        '$group': {
            '_id': '$ip',
            'count': {
                '$sum': 1
            }
        }
}, {
        "$project": {
            "ip": '$_id',
            'date': 1,
            'count': 1
        }
}, {
        "$sort": {
            "count": -1
        }
}, {
        '$limit': 10
}]):
    print(row.get('ip'))
if __name__ == '__main__':
    exit()
