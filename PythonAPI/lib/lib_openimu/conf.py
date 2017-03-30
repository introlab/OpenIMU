import simplejson
import os

ERROR_404_HELP = False      # Don't add extra suggestions to 404 error msg
RESTFUL_JSON = {'cls': simplejson.JSONEncoder}

MONGO_HOST = os.getenv('OPENIMU_DATABASE_SERVER', 'localhost')
MONHO_PORT = 27017
MONGO_DBNAME = "openimu"

VERSION_MAJOR = 0
VERSION_MINOR = 1
