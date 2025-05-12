export async function fetchMarkets() {
  const res = await fetch("/markets");
  return await res.json();
}

export async function fetchBets() {
  const res = await fetch("/bets");
  return await res.json();
}

export function subscribeMarkets(onData) {
  const ws = new WebSocket((location.protocol === "https:" ? "wss" : "ws") + "://" + location.host + "/ws");
  ws.onmessage = e => {
    const msg = JSON.parse(e.data);
    if (msg.type === "update") onData(msg.data);
  };
  return () => ws.close();
}
