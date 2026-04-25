# 1 Ledger

Balance is stored in paise.

Credits and debits are tracked in ledger entries.

Balance invariant:
credits - debits = merchant balance


# 2 Lock

Used:

select_for_update()

inside:

transaction.atomic()

Merchant row is locked during payout creation.

Available balance is deducted atomically,
preventing simultaneous overdrafts.


# 3 Idempotency

Idempotency keys stored per merchant.

Repeated requests with same key return
same payout response.

No duplicate payouts created.


# 4 State Machine

Allowed:

pending -> processing -> completed

pending -> processing -> failed

Illegal backward transitions blocked in task logic.


# 5 AI Audit

Initial implementation used balance aggregation
during payout requests.

It allowed race conditions under simultaneous requests.

Fixed by moving to locked merchant balance
with atomic decrement using select_for_update.