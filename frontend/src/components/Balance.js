import { useEffect, useState } from "react";

function Balance() {
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/balance/")
      .then(res => res.json())
      .then(data => setBalance(data.balance));
  }, []);

  return (
    <div>
      <h3>Balance: ₹{balance}</h3>
    </div>
  );
}

export default Balance;