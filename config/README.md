# Playto Payout Engine

## Tech Stack
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- React
- Tailwind

## Setup

### Clone
git clone <repo_url>

cd payout_engine


### Create venv
python -m venv venv

venv\Scripts\activate


### Install dependencies
pip install -r requirements.txt


### Run migrations
python manage.py makemigrations

python manage.py migrate


### Start server
python manage.py runserver


### Start Celery worker
python -m celery -A config.celery:app worker --pool=solo --loglevel=info


## API Endpoint

POST /api/v1/payouts/

Headers:
Idempotency-Key

Body:
{
 "amount_paise":5000,
 "bank_account_id":"bank123"
}


## Features
- Merchant ledger
- Concurrency-safe payouts
- Idempotent API
- Retry logic
- Simulated settlement worker


## Test Concurrency
python concurrency_test.py