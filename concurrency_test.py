import threading
import requests

url="http://127.0.0.1:8000/api/v1/payouts/"

def payout(key):

    data={
      "amount_paise":7000,
      "bank_account_id":"bank123"
    }

    headers={
      "Idempotency-Key":key
    }

    r=requests.post(
      url,
      json=data,
      headers=headers
    )

    print(
      key,
      r.text
    )

t1=threading.Thread(
target=payout,
args=('newkey101',)
)

t2=threading.Thread(
target=payout,
args=('newkey102',)
)

t1.start()
t2.start()

t1.join()
t2.join()