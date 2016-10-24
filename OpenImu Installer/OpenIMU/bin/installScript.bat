if not exist "C:\data" mkdir C:\data
if not exist "C:\data\db" mkdir C:\data\db
CD C:/Program Files/MongoDB/Server/3.2/bin
mongod --logpath=C:/data/db/log.txt --install
net start MongoDB
CD C:/Python27/Scripts
pip install numpy
pip install flask
pip install flask_restful
pip install flask_marshmallow
pip install flask_pymongo
pip install simplejson
pip install marshmallow==2.10.0