import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

ERROR_MAIL_FROM = os.getenv("ERROR_MAIL_FROM")      # ex: tonmail@outlook.com
ERROR_MAIL_TO = os.getenv("ERROR_MAIL_TO")          # ex: tonmail@outlook.com
ERROR_MAIL_SMTP = os.getenv("ERROR_MAIL_SMTP", "smtp.office365.com")
ERROR_MAIL_PORT = int(os.getenv("ERROR_MAIL_PORT", "587"))
ERROR_MAIL_PASSWORD = os.getenv("ERROR_MAIL_PASSWORD")
DISCORD_ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

_MODEL_NAME = "kk08/CryptoBERT"

_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(_MODEL_NAME)

crypto_sentiment = pipeline(
    "sentiment-analysis",
    model=_model,
    tokenizer=_tokenizer,
)


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

def send_error_email(subject: str, body: str) -> None:
    """Envoie un mail simple en texte brut pour les erreurs du bot."""
    if not (ERROR_MAIL_FROM and ERROR_MAIL_TO and ERROR_MAIL_PASSWORD):
        # Config incomplète -> on ne tente rien
        return

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = ERROR_MAIL_FROM
    msg["To"] = ERROR_MAIL_TO

    with smtplib.SMTP(ERROR_MAIL_SMTP, ERROR_MAIL_PORT) as server:
        server.starttls()  # chiffrement TLS (port 587)
        server.login(ERROR_MAIL_FROM, ERROR_MAIL_PASSWORD)
        server.send_message(msg)

def send_discord_log(text: str) -> None:
    if not DISCORD_ERROR_WEBHOOK_URL:
        return

    payload = {
        "content": text[:1900]  # pour rester sous la limite 2000 caractères
    }
    try:
        requests.post(DISCORD_ERROR_WEBHOOK_URL, json=payload, timeout=5)
    except Exception:
        # on évite de faire planter le bot si Discord ne répond pas
        pass