import React, { useState, useEffect } from "react";
import { fetchMarkets, fetchBets, subscribeMarkets } from "./api";

export default function App() {
  const [markets, setMarkets] = useState([]);
  const [bets, setBets] = useState([]);

  useEffect(() => {
    fetchMarkets().then(setMarkets);
    fetchBets().then(setBets);
    const unsub = subscribeMarkets(data => {
      setMarkets(data);
      fetchBets().then(setBets);
    });
    return unsub;
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Polymarket Auto-Bet Dashboard</h1>
      <h2>Markets (Top 50 by volume)</h2>
      <table border="1" cellPadding="8">
        <thead><tr><th>Question</th><th>Volume</th><th>Yes %</th><th>No %</th></tr></thead>
        <tbody>
          {markets.map(m => (
            <tr key={m.id}>
              <td>{m.question}</td>
              <td>{m.volume.toLocaleString()}</td>
              <td>{(m.probabilities.yes*100).toFixed(1)}%</td>
              <td>{(m.probabilities.no*100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Your Auto-Bets</h2>
      <table border="1" cellPadding="8">
        <thead><tr><th>Market ID</th><th>Side</th><th>Amount</th></tr></thead>
        <tbody>
          {bets.map((b, i) => (
            <tr key={i}>
              <td>{b.market_id}</td>
              <td>{b.side}</td>
              <td>{b.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
);
}
