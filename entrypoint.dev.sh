#!/bin/sh

#while ! </dev/tcp/db/5432; do
#  sleep 1
#done

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload