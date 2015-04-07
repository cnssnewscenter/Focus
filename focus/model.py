import pymongo
from focus import app
mc = pymongo.MongoClient(app.config['MONGO_URL'])