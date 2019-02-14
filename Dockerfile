
##################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Wanderlust
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##################################################

FROM jupyter/base-notebook
USER root

#-----------------------------------------------------
#  Basic Packages
#-----------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git  \
    netcat \
    software-properties-common \
    unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


#-------------------------------------------------
#  JAVA 
#-------------------------------------------------

ENV JAVA_VERSION=8
ENV JAVA_HOME=/usr/lib/jvm/java-${JAVA_VERSION}-oracle

RUN echo oracle-java${JAVA_VERSION}-installer shared/accepted-oracle-license-v1-1 select true \
  | /usr/bin/debconf-set-selections \
 && add-apt-repository -y ppa:webupd8team/java \
 &&	apt-get update && apt-get install -y --no-install-recommends oracle-java${JAVA_VERSION}-installer \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /var/cache/oracle-jdk${JAVA_VERSION}-installer
 
 
#-------------------------------------------------
#  SPARK
#-------------------------------------------------

ENV SPARK_VERSION=2.4.0 \
    PY4J_VERSION=0.10.4
    
ENV SPARK_PACKAGE=spark-${SPARK_VERSION}-bin-hadoop2.7 \
    SPARK_HOME=/usr/spark-${SPARK_VERSION}
    
ENV PATH=${PATH}:${SPARK_HOME}/bin \
    PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-${PY4J_VERSION}-src.zip

RUN curl -sL --retry 3 \
  "http://apache.rediris.es/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /usr/ \
 && mv /usr/${SPARK_PACKAGE} ${SPARK_HOME} \
 && chown -R root:root ${SPARK_HOME}


#-------------------------------------------------
# Node
#-------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm    \
#&& ln -s `which nodejs` /usr/bin/node  \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*  

WORKDIR /root

RUN npm install express socket.io


#-------------------------------------------------
#  Python Dependencies
#-------------------------------------------------

RUN pip install \
  confluent-kafka \
  kafka-python
  

