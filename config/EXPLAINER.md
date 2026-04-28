# 💡 Payout System - Explainer

## 📌 Overview

This project is a payout system where a merchant can request withdrawals.  
The system ensures correctness, avoids duplicate processing, and handles failures using retries.

---

## 🔑 Key Concepts

### 1. Idempotency

Each payout request includes an `Idempotency-Key`.

- If the same key is used again → no new payout is created
- Existing payout is returned

👉 This prevents duplicate transactions.

---

### 2. Concurrency Handling

To avoid double spending, I used:

- `select_for_update()` (row locking)
- Database transactions

👉 Ensures only one request modifies balance at a time.

---

### 3. Ledger System

Instead of directly updating balance, I used a ledger:

- **HOLD** → when payout is initiated
- **DEBIT** → when payout succeeds
- **CREDIT** → when payout fails

👉 This provides traceability and consistency.

---

### 4. Async Processing (Celery)

Payout processing is handled in the background:

1. API creates payout (status = pending)
2. Celery worker processes it
3. Updates status to completed/failed

👉 Improves performance and scalability.

---

### 5. Retry Mechanism

- If payout fails → retry automatically
- Retry count is tracked
- Max retries = 3
- After that → mark as FAILED and refund

👉 Ensures reliability.

---

### 6. Failure Simulation

To test retry logic:

- Random failures are introduced
- Mimics real-world payment failures

---

## 🔄 System Flow

1. User sends payout request
2. Idempotency key is checked
3. Merchant row is locked
4. Balance is validated
5. HOLD entry is created
6. Payout is created (pending)
7. Celery processes payout
8. On success → DEBIT
9. On failure → retry → eventually CREDIT

---

## ⚠️ Edge Cases Handled

- Duplicate requests → idempotency
- Concurrent requests → row locking
- Insufficient balance → rejected
- Failures → retries
- Max retries → refund

---

## 🖥️ Frontend

The React UI allows:

- Creating payouts (withdraw)
- Viewing payout history
- Tracking retry count and status
- Auto-refresh updates

---

## 🚀 Conclusion

This system is:

- **Safe** → idempotency + locking
- **Reliable** → retry mechanism
- **Scalable** → async processing
- **Transparent** → ledger system

👉 It simulates a real-world payout system used in fintech applications.