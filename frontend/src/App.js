import Balance from "./components/Balance";
import PayoutForm from "./components/PayoutForm";
import PayoutList from "./components/PayoutList";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Payout Dashboard</h1>

      <Balance />
      <PayoutForm />
      <PayoutList />
    </div>
  );
}

export default App;