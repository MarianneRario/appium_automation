import certifi
from pymongo import MongoClient
import ssl
import datetime

ca = certifi.where()
# DATABASE CLOUD CONNECTION
cluster = MongoClient(
    "mongodb+srv://rariom:marianne07@cluster0.20txl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
# FETCHING DATABASE
db = cluster["facebook"]
# COLLECTION NAME (OR TABLE NAME FOR SQL)
collection = db["user_accounts"]
# COLLECTION FOR LOCKED ACCOUNTS
locked_collection = db["locked_accounts"]
# COLLECTION FOR TIMESTAMP (FOR RESTARTING APPIUM AND ADB)
col_time = db["time"]
# LENGTH OF DOCUMENTS
acc_len = collection.count_documents({})
# time_now = datetime.datetime.now() - datetime.timedelta(minutes=10)
#
# for x in range(len(list(collection.find({})))):
#     collection.update_one({}, {"$set": {"timestamp": time_now}})
