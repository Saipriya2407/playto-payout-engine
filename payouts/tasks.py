import random
from celery import shared_task
from django.db import transaction
from .models import Payout, LedgerEntry


@shared_task(bind=True, max_retries=3)
def process_payout(self, payout_id):
    try:
        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)

            # ✅ If already completed, skip
            if payout.status == 'completed':
                return

            # ✅ Mark as processing
            payout.status = 'processing'
            payout.save()

            print(f"Processing payout {payout.id}, retry {payout.retry_count}")

            # ❌ Simulate failure (70% chance)
            if random.random() < 0.7:
                payout.retry_count =self.request.retries+1
                payout.save()
                raise Exception("force retry")

            # ✅ SUCCESS
            payout.status = 'completed'
            payout.save()

            # ✅ Convert HOLD → DEBIT
            LedgerEntry.objects.create(
                merchant=payout.merchant,
                payout=payout,
                amount_paise=payout.amount_paise,
                entry_type='debit'
            )

    except Exception as e:

        # ❌ MAX RETRY REACHED
        if self.request.retries >= self.max_retries:
            with transaction.atomic():
                payout = Payout.objects.select_for_update().get(id=payout_id)

                payout.status = 'failed'
                payout.save()

                print(f"Payout {payout.id} FAILED after retries")

                # ✅ Refund HOLD → CREDIT
                LedgerEntry.objects.create(
                    merchant=payout.merchant,
                    payout=payout,
                    amount_paise=payout.amount_paise,
                    entry_type='credit'
                )
            return

        print(f"Retrying payout {payout_id}...")

        # 🔁 Retry after 3 seconds
        raise self.retry(exc=e, countdown=3)