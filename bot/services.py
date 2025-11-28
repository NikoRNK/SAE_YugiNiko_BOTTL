import requests

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Mapping symbol -> id CoinGecko
SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    # ajoute ce que tu veux ici
}


def normalize_coin(user_input: str) -> str:
    """
    Normalise l'entrée utilisateur :
    - met en minuscule
    - mappe les symboles connus vers les ids CoinGecko
    - sinon, renvoie tel quel (pour 'bitcoin', 'solana', etc.)
    """
    s = user_input.lower()
    return SYMBOL_TO_ID.get(s, s)


def get_price_usd(coin_id: str) -> float:
    url = f"{COINGECKO_BASE_URL}/simple/price"
    params = {"ids": coin_id, "vs_currencies": "usd"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data[coin_id]["usd"])


def get_multi_prices_usd(coin_ids: list[str]) -> dict[str, float]:
    if not coin_ids:
        return {}
    url = f"{COINGECKO_BASE_URL}/simple/price"
    params = {"ids": ",".join(coin_ids), "vs_currencies": "usd"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {cid: float(data[cid]["usd"]) for cid in coin_ids if cid in data}


def get_market_snapshot(coin_ids: list[str]) -> dict:
    markets_url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {"vs_currency": "usd", "ids": ",".join(coin_ids)}
    r = requests.get(markets_url, params=params, timeout=10)
    r.raise_for_status()
    items = r.json()

    coins = {}
    for item in items:
        cid = item["id"]
        coins[cid] = {
            "price": float(item["current_price"]),
            "change_24h": float(item["price_change_percentage_24h"] or 0),
            "volume_24h": float(item["total_volume"]),
        }

    global_url = f"{COINGECKO_BASE_URL}/global"
    g = requests.get(global_url, timeout=10)
    g.raise_for_status()
    gdata = g.json()
    btc_dom = float(gdata["data"]["market_cap_percentage"]["btc"])

    return {"coins": coins, "btc_dominance": btc_dom}


def get_ohlc(coin_id: str, days: int) -> list[list[float]]:
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/ohlc"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()
