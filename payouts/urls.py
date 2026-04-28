from django.urls import path
from .views import create_payout, list_payouts, merchant_balance, get_payout

urlpatterns = [
    path('payout-request/', create_payout),
    path('payouts/', list_payouts),
    path('payouts/<int:payout_id>/', get_payout),   # ✅ single payout
    path('balance/', merchant_balance),
]