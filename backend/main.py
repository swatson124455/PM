import asyncio, os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from engine import run_betting_engine, PLACED_BETS
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("POLY_API_URL", "https://api.polymarket.com/graphql")

app = FastAPI()
transport = AIOHTTPTransport(url=API_URL)
gql_client = Client(transport=transport, fetch_schema_from_transport=True)

QUERY = gql(""" 
  query Markets($skip: Int!) {
    markets(where: { state: "TRADING" }, first: 50, skip: $skip, orderBy: volume, orderDirection: desc) {
      id question volume probabilities { yes no }
    }
  }
""")

latest_markets: List[Dict] = []
clients: List[WebSocket] = []

async def poll_and_bet():
    global latest_markets
    while True:
        all_markets = []
        skip = 0
        while True:
            data = await gql_client.execute_async(QUERY, variable_values={"skip": skip})
            batch = data["markets"]
            if not batch:
                break
            all_markets.extend(batch)
            skip += len(batch)
            if skip >= 200:
                break
        latest_markets = all_markets
        for ws in clients.copy():
            try:
                await ws.send_json({"type": "update", "data": latest_markets})
            except:
                clients.remove(ws)
        await run_betting_engine(latest_markets)
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(poll_and_bet())

@app.get("/markets")
async def get_markets():
    return latest_markets

@app.get("/bets")
async def get_bets():
    return PLACED_BETS

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    await ws.send_json({"type": "update", "data": latest_markets})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)
