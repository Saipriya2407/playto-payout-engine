import React,{useEffect,useState}
from "react";

import axios from "axios";

function App(){

const [balance]=useState(50000);

const [payouts,setPayouts]=useState([]);



const loadPayouts=async()=>{

try{

const res=await axios.get(
"http://127.0.0.1:8000/api/v1/payouts/"
);

setPayouts(
res.data
);

}catch(e){
console.log(e);
}

};


useEffect(()=>{
loadPayouts()
},[]);



return(

<div style={{
padding:"40px"
}}>

<h1>
Playto Dashboard
</h1>


<h2>
Balance:
₹ {balance/100}
</h2>



<h2>
Request Payout
</h2>
<form
action="http://127.0.0.1:8000/api/v1/payout-request/"
method="POST"
encType="application/x-www-form-urlencoded"
>
<input
name="amount_paise"
defaultValue="1000"
/>

<input
name="bank_account_id"
defaultValue="bank123"
/>
<input
type="hidden"
name="Idempotency-Key"
value={Date.now()}
/>

<button type="submit">
Withdraw
</button>

</form>



<h2>
Payout History
</h2>


<ul>

{payouts.map(p=>(

<li key={p.id}>
Amount: {p.amount_paise} | Status: {p.status}
</li>

))}

</ul>

</div>

)

}

export default App;