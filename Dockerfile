FROM python:3.9

## ODBC drivers
ARG DRIVER_MAJOR_VERSION="2.6.29"
ARG DRIVER_MINOR_VERSION=1049
ARG BUCKET_URI="https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc"

ENV DRIVER_FULL_VERSION=${DRIVER_MAJOR_VERSION}.${DRIVER_MINOR_VERSION}
ENV FOLDER_NAME=SimbaSparkODBC-${DRIVER_FULL_VERSION}-Debian-64bit
ENV ZIP_FILE_NAME=${FOLDER_NAME}.zip

WORKDIR /opt/drivers


RUN apt-get update -y && \
    apt-get install -y unzip unixodbc-dev unixodbc build-essential cmake make procps && \
    wget ${BUCKET_URI}/${DRIVER_MAJOR_VERSION}/${ZIP_FILE_NAME} && \
    unzip ${ZIP_FILE_NAME} && rm -f ${ZIP_FILE_NAME} && \
    apt-get install -y ./*.deb

## NodeJS for pynecone

ENV NODE_VERSION=16.13.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

ENV POETRY_HOME /opt/poetry
ENV PATH ${POETRY_HOME}/bin:${PATH}
RUN apt-get update && apt-get install build-essential -y
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false 

RUN mkdir /app
WORKDIR /app