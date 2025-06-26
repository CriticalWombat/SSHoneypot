# app/config.py
import os

# API Keys (set in .env or docker-compose environment)
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

# Database backend (sqlite or postgresql)
DB_BACKEND = os.getenv("DB_BACKEND", "sqlite")
DB_URL = os.getenv("DB_URL", "sqlite:///data/intel.db")

# Cowrie honeypot connection (container DNS hostname is 'cowrie')
COWRIE_HOST = os.getenv("COWRIE_HOST", "cowrie")
COWRIE_PORT = int(os.getenv("COWRIE_PORT", 2222))

# Wrapper listener port
LISTEN_PORT = int(os.getenv("LISTEN_PORT", 22))

# Tor SOCKS proxy
TOR_SOCKS_PROXY = "socks5h://localhost:9050"

# Timeout settings
LOOKUP_TIMEOUT = 10  # seconds
