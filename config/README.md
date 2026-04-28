# 💸 Payout Engine

A full-stack payout system built using Django, Celery, and React.

---

## 🚀 Features

- Create payout API
- Idempotency handling (no duplicate payouts)
- Balance validation
- Ledger system (hold → debit / credit)
- Async processing using Celery
- Retry mechanism with failure handling
- React frontend dashboard

---

## 🛠️ Tech Stack

### Backend
- Django
- Django REST Framework
- PostgreSQL
- Celery (for async tasks)
- Redis (broker)

### Frontend
- React.js

---

## ⚙️ How It Works

1. User sends payout request
2. System checks balance
3. Amount is put on HOLD
4. Celery processes payout asynchronously
5. On success → DEBIT
6. On failure → retry (max 3 times)
7. If failed → amount refunded (CREDIT)

---

## 🔑 Idempotency

- Each request uses `Idempotency-Key`
- Prevents duplicate payouts

---

## 🔄 Retry Logic

- Failed payouts are retried automatically
- Retry count tracked
- Max retries → mark as FAILED

---

## 📊 APIs

### Create Payout
POST `/api/v1/payout-request/`

### Get Payouts
GET `/api/v1/payouts/`

### Get Balance
GET `/api/v1/balance/`

---

## 🖥️ Frontend

- Withdraw money
- View payout history
- See retry count & status
- Auto-refresh updates

---

## ▶️ Run Locally

### Backend

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver