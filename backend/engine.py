import asyncio
from typing import List, Dict
from pydantic import BaseModel

class Bet(BaseModel):
    market_id: str
    side: str
    amount: float

PLACED_BETS: List[Bet] = []

async def run_betting_engine(markets: List[Dict]):
    for m in markets:
        yes_prob = m["probabilities"]["yes"]
        if yes_prob < 0.5:
            bet = Bet(market_id=m["id"], side="yes", amount=1.0)
            PLACED_BETS.append(bet)
            print(f"[engine] placed bet -> {bet}")
            break
    await asyncio.sleep(0)
