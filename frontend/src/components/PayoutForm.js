import { useEffect, useState } from "react";

function PayoutList() {
  const [payouts, setPayouts] = useState([]);

  const fetchPayouts = () => {
    fetch("http://localhost:8000/api/v1/payouts/")
      .then(res => res.json())
      .then(data => setPayouts(data))
      .catch(err => console.error("Error:", err));
  };

  useEffect(() => {
    fetchPayouts();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchPayouts();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // ✅ ADD HERE (inside component, before return)
  const getColor = (status) => {
    if (status === "completed") return "green";
    if (status === "failed") return "red";
    return "orange"; // pending
  };

  return (
    <div>
      <h3>Payout History</h3>

      {payouts.map(p => (
        <div key={p.id} style={{ color: getColor(p.status) }}>
          ₹{p.amount_paise} - {p.status} - retry: {p.retry_count}
        </div>
      ))}
    </div>
  );
}

export default PayoutList;