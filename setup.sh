#!/bin/bash
cd /osusettings/
alembic upgrade head
sleep 1
PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -h db -d $POSTGRES_DB -f ./data.sql
python3 main.py
