from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.db import transaction

from payouts.tasks import process_payout

from .serializers import PayoutSerializer

from .models import (
Merchant,
Payout,
LedgerEntry,
IdempotencyKey,
get_balance
)



@api_view(['GET'])
def payout_list(request):

    payouts=Payout.objects.all()

    s=PayoutSerializer(
      payouts,
      many=True
    )

    return Response(
      s.data
    )



@csrf_exempt
@api_view(['POST'])
def create_payout(request):

    with transaction.atomic():

        merchant=Merchant.objects.select_for_update().get(
        id=1
        )


        key=request.headers.get(
          'Idempotency-Key'
        )


        if not key:

            return Response({
            "error":
            "Idempotency-Key required"
            },status=400)



        existing = IdempotencyKey.objects.filter(
          merchant=merchant,
          key=key
        ).first()


        if existing:

            return Response({

            "message":
            "Already processed",

            "payout_id":
            existing.payout.id

            })



        amount=int(
        request.data[
        'amount_paise'
        ]
        )



        if merchant.available_balance < amount:

            return Response({
            "error":
            "Insufficient balance"
            },status=400)



        merchant.available_balance-=amount
        merchant.save()



        payout=Payout.objects.create(
           merchant=merchant,
           amount_paise=amount,
           status='pending',
           bank_account_id=request.data[
           'bank_account_id'
           ]
        )



        LedgerEntry.objects.create(
           merchant=merchant,
           amount_paise=amount,
           entry_type='debit'
        )



        IdempotencyKey.objects.create(
           merchant=merchant,
           key=key,
           payout=payout
        )



        process_payout.delay(
        payout.id
        )



        return Response({
        "message":"Payout created",
        "payout_id":payout.id
        })