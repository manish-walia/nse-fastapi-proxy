from fastapi import FastAPI, HTTPException
import requests, random, traceback
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/option-chain/{symbol}")
def get_option_chain(symbol: str):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        warmup = session.get("https://www.nseindia.com", timeout=5)
        if warmup.status_code != 200:
            raise Exception(f"NSE warmup failed with status {warmup.status_code}")

        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        resp = session.get(url, timeout=10)

        if resp.status_code != 200:
            raise Exception(f"NSE API returned status {resp.status_code}")

        return resp.json()

    except Exception as e:
        err_msg = f"Proxy error for {symbol}: {e}\n{traceback.format_exc()}"
        print(err_msg)  # Logs appear on Railway
        raise HTTPException(status_code=500, detail=err_msg)
