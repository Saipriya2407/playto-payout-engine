# 1 The Ledger

Credits and debits are modeled in LedgerEntry.

Balance invariant:

balance = credits - debits

Debits created when payout requested.
Credits returned on payout failure.

This preserves money integrity.



# 2 The Lock

Concurrency protection:

```python
with transaction.atomic():

 merchant = Merchant.objects.select_for_update().get(id=1)

 if merchant.available_balance < amount:
     reject

 merchant.available_balance -= amount
 merchant.save()
```

Database primitive:
Row-level locking via SELECT FOR UPDATE.

Prevents simultaneous overdrafts.



# 3 Idempotency

Idempotency keys stored in IdempotencyKey model.

On repeated request:

- lookup merchant + key
- if found return existing payout response
- no duplicate payout created

If second request arrives while first in-flight,
row lock prevents double processing.



# 4 State Machine

Legal:

pending -> processing -> completed

pending -> processing -> failed

Illegal backward transitions are blocked in task logic.

Failed payouts atomically return held funds.



# 5 AI Audit

Initial AI-generated version calculated balance
from aggregated ledger rows during payout creation.

This caused race-condition risk.

Caught issue during concurrency test where two
simultaneous payouts both succeeded.

Replaced with:

- merchant available_balance field
- select_for_update row lock
- atomic balance decrement

This fixed overdraft race condition.