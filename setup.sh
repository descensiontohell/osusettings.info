#!/bin/bash
cd /osusettings/
sleep 2
alembic upgrade head
sleep 2
PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -h db -d $POSTGRES_DB -f ./data.sql
sleep 2
python3 main.py
