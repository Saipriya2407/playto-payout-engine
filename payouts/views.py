from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

from .models import Merchant, Payout, LedgerEntry, IdempotencyKey, get_balance
from .tasks import process_payout


@api_view(['POST'])
def create_payout(request):

    # ✅ Validate amount safely
    try:
        amount = int(request.data.get('amount_paise'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid amount format"}, status=400)

    if amount <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    with transaction.atomic():

        merchant = Merchant.objects.select_for_update().first()

        # ✅ Idempotency check FIRST
        key = request.headers.get('Idempotency-Key') or request.data.get('Idempotency-Key')

        if not key:
            return Response({"error": "Idempotency-Key required"}, status=400)

        existing = IdempotencyKey.objects.filter(
            merchant=merchant,
            key=key
        ).first()

        if existing:
            return Response({
                "message": "Already processed",
                "payout_id": existing.payout.id
            })

        # ✅ Check balance
        balance = get_balance(merchant)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        # ✅ Create payout
        payout = Payout.objects.create(
            merchant=merchant,
            amount_paise=amount,
            status='pending',
            bank_account_id=request.data['bank_account_id']
        )

        # ✅ HOLD entry
        LedgerEntry.objects.create(
            merchant=merchant,
            payout=payout,
            amount_paise=amount,
            entry_type='hold'
        )

        # ✅ Save idempotency
        IdempotencyKey.objects.create(
            merchant=merchant,
            key=key,
            payout=payout
        )

        # ✅ Trigger async task
        process_payout.delay(payout.id)

        return Response({
            "message": "Payout created",
            "payout_id": payout.id
        })


@api_view(['GET'])
def list_payouts(request):
    payouts = Payout.objects.all().values()
    return Response(list(payouts))


@api_view(['GET'])
def merchant_balance(request):
    merchant = Merchant.objects.first()
    balance = get_balance(merchant)
    return Response({"balance": balance})


@api_view(['GET'])
def get_payout(request, payout_id):
    payout = Payout.objects.filter(id=payout_id).values().first()
    return Response(payout)