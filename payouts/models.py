from django.db import models

class Merchant(models.Model):
    name=models.CharField(max_length=100)
    available_balance=models.BigIntegerField(default=0)

class LedgerEntry(models.Model):

    ENTRY_TYPES=(
      ('credit','Credit'),
      ('debit','Debit'),
      ('hold','Hold')
    )

    merchant=models.ForeignKey(
       Merchant,
       on_delete=models.CASCADE
    )

    amount_paise=models.BigIntegerField()

    entry_type=models.CharField(
       max_length=20,
       choices=ENTRY_TYPES
    )

    created_at=models.DateTimeField(
       auto_now_add=True
    )

class Payout(models.Model):

    STATUS=(
      ('pending','Pending'),
      ('processing','Processing'),
      ('completed','Completed'),
      ('failed','Failed')
    )

    merchant=models.ForeignKey(
       Merchant,
       on_delete=models.CASCADE
    )

    amount_paise=models.BigIntegerField()

    status=models.CharField(
      max_length=20,
      choices=STATUS,
      default='pending'
    )

    bank_account_id=models.CharField(
      max_length=100
    )

    retry_count=models.IntegerField(
      default=0
    )

    created_at=models.DateTimeField(
      auto_now_add=True
    )

class IdempotencyKey(models.Model):
    merchant=models.ForeignKey(
       Merchant,
       on_delete=models.CASCADE
    )

    key=models.CharField(
       max_length=255
    )

    payout=models.ForeignKey(
      Payout,
      on_delete=models.CASCADE
    )

    created_at=models.DateTimeField(
      auto_now_add=True
    )
from django.db.models import Sum
def get_balance(merchant):

    credits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='credit'
    ).aggregate(
        Sum('amount_paise')
    )

    debits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='debit'
    ).aggregate(
        Sum('amount_paise')
    )

    total_credit = credits['amount_paise__sum'] or 0
    total_debit = debits['amount_paise__sum'] or 0

    return total_credit - total_debit

