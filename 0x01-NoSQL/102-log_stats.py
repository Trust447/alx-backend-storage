#!/usr/bin/env python3
""" Log stats - new version """
from pymongo import MongoClient
from pymongo.errors import ConnectionError


def nginx_stats_check():
    """ Provides some stats about Nginx logs stored in MongoDB """
    try:
        client = MongoClient()  # Connect to the MongoDB server
        collection = client.logs.nginx  # Access the nginx logs collection

        num_of_docs = collection.count_documents({})
        print("{} logs".format(num_of_docs))
        print("Methods:")
        
        methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods_list:
            method_count = collection.count_documents({"method": method})
            print("\tmethod {}: {}".format(method, method_count))
        
        status = collection.count_documents({"method": "GET", "path": "/status"})
        print("{} status check".format(status))

        print("IPs:")
        top_IPs = collection.aggregate([
            {"$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10},
            {"$project": {
                "_id": 0,
                "ip": "$_id",
                "count": 1
            }}
        ])

        for top_ip in top_IPs:
            count = top_ip.get("count")
            ip_address = top_ip.get("ip")
            print("\t{}: {}".format(ip_address, count))

    except ConnectionError:
        print("Failed to connect to MongoDB. Please ensure it is running.")
    except Exception as e:
        print("An error occurred: {}".format(e))


if __name__ == "__main__":
    nginx_stats_check()
