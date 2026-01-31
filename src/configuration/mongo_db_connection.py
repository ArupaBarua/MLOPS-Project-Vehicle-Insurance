import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY
#Loading the certificate authority file to avoid timeout errors while connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    client = None # shared MongoClient instance across all MongoDBClient instances

    def __init__(self, database_name : str = DATABASE_NAME) -> None:

        try:
            if MongoDBClient.client is None:
                mongodb_url = os.getenv(MONGODB_URL_KEY)
                if mongodb_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set")
                MongoDBClient.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful.")

        except Exception as e:
            raise MyException(e, sys) from e