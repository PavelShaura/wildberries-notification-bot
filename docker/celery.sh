#!/bin/bash

celery -A worker.tasks beat --loglevel=info &
celery -A worker.tasks worker --loglevel=info