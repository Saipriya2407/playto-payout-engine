from django.urls import path

from .views import (
create_payout,
payout_list
)

urlpatterns = [

path(
'payouts/',
payout_list
),

path(
'payout-request/',
create_payout
),

]