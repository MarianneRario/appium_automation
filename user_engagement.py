# SSL CERTIFICATE
import certifi
from pymongo import MongoClient
import ssl

# SSL CERTIFICATE
ca = certifi.where()
# DATABASE CLOUD CONNECTION
cluster = MongoClient(
    "mongodb+srv://pass:name@cluster0.20txl.mongodb.net/users?retryWrites=true&w=majority",
    ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
# FETCHING DATABASE
db = cluster["facebook"]
# COLLECTION NAME (OR TABLE NAME FOR SQL)
user_engagement_collection = db["user_engagement"]


def add_user_engagement(filename, url, email, password):
    post = {
        "filename": filename + ".png",
        "url": url,
        "accounts": [{
            "email": email,
            "password": password}
        ]
    }
    # INSERT DATA IN DATABASE
    user_engagement_collection.insert_one(post)
