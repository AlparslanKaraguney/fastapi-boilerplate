#!/bin/bash
# get ENV variable from env. If local,use this else do not use --reload

if [ "$ENV" = "dev" ] || [ "$ENV" = "prod" ];
then
    alembic upgrade head
    uvicorn app.main:app --host 0.0.0.0 --port 8000
else
    alembic upgrade head
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
