# Image: introlab3it/openimu:xenial
FROM ubuntu:16.04

MAINTAINER Dominic Letourneau <doumdi@docker.com>

# Install build dependencies
RUN apt-get update && apt-get install -y \
	git \
	python \
	python-setuptools \
	python-dev \
	build-essential \
	python-pip
	
# Get OpenIMU/Python dependencies  
RUN pip install --upgrade pip 
RUN pip install numpy
RUN pip install flask
RUN pip install flask_restful
RUN pip install flask_marshmallow
RUN pip install flask_pymongo
RUN pip install simplejson
RUN pip install marshmallow==2.10.0
RUN pip install tornado    
    
   
# Clone source code
WORKDIR /root/
RUN git clone -b macosx https://github.com/introlab/OpenIMU.git

# Expose OpenIMU backend default port
EXPOSE 5000

# The name of the database server (container)
ENV OPENIMU_DATABASE_SERVER=mongo

WORKDIR /root/OpenIMU/PythonAPI/src/
CMD ["python", "tornado_wsgi.py"]


