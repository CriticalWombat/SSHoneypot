# app/main.py
import asyncio
import socket
import json
from datetime import datetime, timezone
from config import COWRIE_HOST, COWRIE_PORT, LISTEN_PORT
from intelligence import collect_all_intel
from db import cache_result

BUFFER_SIZE = 4096

async def log(data):
    data["timestamp"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(data))

async def handle_client(reader, writer):
    peername = writer.get_extra_info('peername')
    source_ip = peername[0] if peername else "unknown"

    # Read banner for SSH fingerprint
    try:
        banner = await asyncio.wait_for(reader.read(1024), timeout=3)
        ssh_fingerprint = banner.decode(errors='ignore').strip()
    except Exception as e:
        ssh_fingerprint = f"error: {e}"

    # Perform intelligence lookups
    intel = await collect_all_intel(source_ip, ssh_fingerprint)
    await cache_result(source_ip, ssh_fingerprint, intel)
    await log({"source_ip": source_ip, "ssh_fingerprint": ssh_fingerprint, **intel})

    # Forward connection to Cowrie
    try:
        cowrie_reader, cowrie_writer = await asyncio.open_connection(COWRIE_HOST, COWRIE_PORT)

        async def forward(src_reader, dst_writer):
            try:
                while not src_reader.at_eof():
                    data = await src_reader.read(BUFFER_SIZE)
                    if not data:
                        break
                    dst_writer.write(data)
                    await dst_writer.drain()
            except:
                pass
            finally:
                dst_writer.close()

        await asyncio.gather(
            forward(reader, cowrie_writer),
            forward(cowrie_reader, writer)
        )

    except Exception as e:
        print(f"[!] Failed to connect to Cowrie: {e}")
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, host='0.0.0.0', port=LISTEN_PORT)
    addr = server.sockets[0].getsockname()
    print(f"[+] Listening on {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
