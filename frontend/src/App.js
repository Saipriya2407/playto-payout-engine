import React,{useEffect,useState}
from "react";

import axios from "axios";

function App(){

const [balance]=
useState(50000);

const [amount,setAmount]=
useState("");

const [payouts,setPayouts]=
useState([]);



const loadPayouts=async()=>{

try{

const res=await axios.get(
"http://localhost:8000/api/v1/payouts/"
);

setPayouts(
res.data
);

}catch(e){

console.log(e);

alert(
"Error loading payouts"
)

}

};



const submitPayout=async()=>{

try{

const res=await fetch(
"http://localhost:8000/api/v1/payout-request/",
{
method:"POST",

headers:{
"Content-Type":
"application/json",

"Idempotency-Key":
Date.now().toString()
},

body:JSON.stringify({
amount_paise:Number(
amount
),
bank_account_id:
"bank123"
})

}
);

const data=
await res.json();

console.log(data);

alert(
"Payout Requested"
);

loadPayouts();

}catch(err){

console.log(err);

alert(
"Request Failed"
)

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


<input
value={amount}
onChange={(e)=>
setAmount(
e.target.value
)}
placeholder="Amount in paise"
/>


<button
onClick={submitPayout}
>
Withdraw
</button>


<h2>
Payout History
</h2>


<ul>

{payouts.map(p=>(

<li key={p.id}>

Amount:
{p.amount_paise}
{" "}
Status:
{p.status}

</li>

))}

</ul>

</div>

)

}

export default App;