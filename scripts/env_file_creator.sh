#!/bin/bash

CREDENTIAL_FILE="credentials.json"

cd ..

# Remove old .env file
if [ -f ".env" ]; then
  rm .env
fi

# Create new .env file
touch .env

# Insert data into file
echo "SERVER_PORT=$(jq .server.port $CREDENTIAL_FILE)" >> .env

DB_NAME=$(jq .db.db_name $CREDENTIAL_FILE)
echo "MYSQL_DATABASE=${DB_NAME//\"}" >> .env

DB_ROOT_PASSWORD=$(jq .db.root_password $CREDENTIAL_FILE)
echo "MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD//\"}" >> .env

DB_USER=$(jq .db.user $CREDENTIAL_FILE)
echo "MYSQL_USER=${DB_USER//\"}" >> .env

DB_USER_PASSWORD=$(jq .db.user_password $CREDENTIAL_FILE)
echo "MYSQL_PASSWORD=${DB_USER_PASSWORD//\"}" >> .env

echo "MYSQL_PORT=$(jq .db.port $CREDENTIAL_FILE)" >> .env

echo "PMA_PORT=$(jq .phpmyadmin.port $CREDENTIAL_FILE)" >> .env