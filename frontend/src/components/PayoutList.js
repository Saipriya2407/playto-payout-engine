import { useEffect, useState } from "react";

function PayoutList() {
  const [payouts, setPayouts] = useState([]);

  // ✅ function to fetch payouts
  const fetchPayouts = () => {
    fetch("http://localhost:8000/api/v1/payouts/")
      .then(res => res.json())
      .then(data => setPayouts(data))
      .catch(err => console.error("Error:", err));
  };

  // ✅ initial load
  useEffect(() => {
    fetchPayouts();
  }, []);

  // ✅ auto refresh every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchPayouts();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h3>Payout History</h3>

      {payouts.map(p => (
        <div key={p.id}>
          ₹{p.amount_paise} - {p.status} - retry: {p.retry_count}
        </div>
      ))}
    </div>
  );
}

export default PayoutList;