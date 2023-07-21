#!/bin/sh
alembic upgrade head && python3 app.py
