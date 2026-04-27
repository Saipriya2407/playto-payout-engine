# Playto Payout Engine

## Overview
A payout engine built using Django, DRF, PostgreSQL, Celery and React.

Supports:
- Merchant ledger in paise
- Idempotent payout requests
- Concurrency-safe withdrawals
- Async payout processing
- Retry and failure handling
- React merchant dashboard


## Tech Stack
Backend:
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis/Memurai

Frontend:
- React


## Setup

### Clone
```bash
git clone <repo-url>
cd payout_engine
```
### Install dependencies

```bash
pip install -r requirements.txt
```

### Backend setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run backend
```bash
python manage.py runserver
```

### Start worker
```bash
python -m celery -A config worker --pool=solo --loglevel=info
```


## Frontend
```bash
cd frontend
npm install
npm start
```


## API

POST:

```http
/api/v1/payout-request/
```

Headers:

```text
Idempotency-Key
```

Body:

```json
{
 "amount_paise":5000,
 "bank_account_id":"bank123"
}
```


## Concurrency Test

Run:

```bash
python concurrency_test.py
```

Expected:
Two simultaneous payouts against insufficient balance:
only one succeeds.


## Features Implemented

- Ledger based balance model
- select_for_update locking
- Idempotency key store
- State machine:
pending → processing → completed/failed

- Retry logic
- Refund on failure
- React dashboard
- Withdraw form