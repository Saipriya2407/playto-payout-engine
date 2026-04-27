from celery import shared_task
import random
from .models import (Payout,LedgerEntry)
@shared_task
def process_payout(
payout_id
):

    payout=Payout.objects.get(
      id=payout_id
    )

    payout.status='processing'
    payout.save()

    x=random.randint(1,100)
    # x=80

    if x<=70:

        payout.status='completed'
        payout.save()


    elif x<=90:

        payout.status='failed'
        payout.save()

        LedgerEntry.objects.create(
            merchant=payout.merchant,
            amount_paise=
            payout.amount_paise,
            entry_type='credit'
        )


    else:

        if payout.retry_count <3:

            payout.retry_count+=1
            payout.save()

            process_payout.delay(
              payout.id
            )

        else:

            payout.status='failed'
            payout.save()

            LedgerEntry.objects.create(
              merchant=payout.merchant,
              amount_paise=
              payout.amount_paise,
              entry_type='credit'
            )