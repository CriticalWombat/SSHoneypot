# SSH Intelligence Wrapper Honeypot

An asynchronous SSH proxy that wraps around a [Cowrie](https://github.com/cowrie/cowrie) honeypot and performs live intelligence gathering on every incoming connection.

## 🔍 Features

- Collects IP intelligence from:
  - AbuseIPDB
  - Shodan (IP + SSH banner)
  - Nmap (quick port scan)
- Caches results in SQLite
- Async performance using `asyncio` and `aiohttp`
- Uses Tor for anonymous API queries
- Forwards connections to Cowrie on port `2222`
- Containerized with Docker and Compose

---

## 🚀 Quick Start

### 1. Clone the project

```bash
git clone https://github.com/yourusername/ssh-intel-wrapper.git
cd ssh-intel-wrapper
```

### 2. Create your ```.env``` file

```bash
# .env
ABUSEIPDB_API_KEY=your_abuseipdb_api_key
SHODAN_API_KEY=your_shodan_api_key
DB_BACKEND=sqlite
DB_URL=sqlite:///data/intel.db
COWRIE_HOST=cowrie
COWRIE_PORT=2222
LISTEN_PORT=22
```
📌 Don't commit this file — add .env to .gitignore!

### 3. Build & run with Docker Compose

```bash
docker-compose up --build
```

### 4. Logs and Intellegence

- Logs are streamed to stdout (use docker logs ssh_wrapper)
- Data is cached in ```./data/intel.db```

## Sample Log Output

```bash
{
  "timestamp": "2025-06-26T15:43:12.183Z",
  "source_ip": "104.248.47.234",
  "ssh_fingerprint": "SSH-2.0-OpenSSH_7.6p1",
  "abuseipdb": {...},
  "shodan_ip": {...},
  "shodan_ssh_fp": {...},
  "nmap": "Nmap scan report for ..."
}
```

## Requirements

- Docker Engine & Docker Compose
- API keys from:
    - AbuseIPDB
    - Shodan

## Project Structure

```bash
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── intelligence.py
│   ├── db.py
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

