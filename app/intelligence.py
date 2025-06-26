# app/intelligence.py
import aiohttp
import asyncio
import subprocess
from config import ABUSEIPDB_API_KEY, SHODAN_API_KEY, TOR_SOCKS_PROXY, LOOKUP_TIMEOUT

async def fetch_json(session, url, headers=None):
    try:
        async with session.get(url, headers=headers, timeout=LOOKUP_TIMEOUT) as resp:
            return await resp.json()
    except Exception as e:
        return {"error": str(e)}

async def abuseipdb_lookup(ip, session):
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    return await fetch_json(session, url, headers=headers)

async def shodan_lookup_ip(ip, session):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    return await fetch_json(session, url)

async def shodan_search_fingerprint(fingerprint, session):
    query = f"ssh {fingerprint}".replace(' ', '%20')
    url = f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}"
    return await fetch_json(session, url)

async def nmap_scan(ip):
    try:
        proc = await asyncio.create_subprocess_exec(
            "nmap", "-sS", "-Pn", "-T4", "-F", ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
        return stdout.decode()
    except Exception as e:
        return f"nmap_error: {e}"

async def collect_all_intel(ip, fingerprint):
    async with aiohttp.ClientSession(
        trust_env=True,
        connector=aiohttp.ProxyConnector.from_url(TOR_SOCKS_PROXY)
    ) as session:
        abuse_task = abuseipdb_lookup(ip, session)
        shodan_task = shodan_lookup_ip(ip, session)
        shodan_fp_task = shodan_search_fingerprint(fingerprint, session)
        nmap_task = nmap_scan(ip)

        abuse, shodan, shodan_fp, nmap_result = await asyncio.gather(
            abuse_task, shodan_task, shodan_fp_task, nmap_task
        )

        return {
            "abuseipdb": abuse,
            "shodan_ip": shodan,
            "shodan_ssh_fp": shodan_fp,
            "nmap": nmap_result
        }
