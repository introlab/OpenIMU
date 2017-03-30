from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
import os

ma = Marshmallow()

mongo = PyMongo(os.getenv('OPENIMU_DATABASE_SERVER', 'localhost'),27017)
