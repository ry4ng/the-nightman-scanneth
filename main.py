import asyncio

#
# Python port scanner
#
print("=" * 50)
print("The Nightman Scanneth")
print("=" * 50)

ports = [port for port in range(1, 10000)]
ports_map = {port: False for port in ports}


async def check_port(ip, port):
    try:
        # Try to open a connection with a timeout of 1 second
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=0.5
        )
        print(f"{ip}:{port} is open")
        ports_map[port] = True
        writer.close()
        await writer.wait_closed()
    except (asyncio.TimeoutError, ConnectionRefusedError):
        # print(f"{ip}:{port} is closed")
        pass
    except OSError as e:
        if e.errno == 10013:
            print(f"{ip}:{port} access denied (restricted port)")
        else:
            print(f"{ip}:{port} encountered an error: {e}")


async def main(host):
    batch_size = 500

    batch = []
    for i, port in enumerate(ports):
        batch.append(check_port(host, port))

        if (i + 1) % batch_size == 0:
            print(f"Scanning batch of [{batch_size}] ports [{i} out of {len(ports)}]")
            await asyncio.gather(*batch)
            batch = []

    if batch:
        print(f"Scanning final batch of [{len(batch)}] ports")
        await asyncio.gather(*batch)


host = "127.0.0.1"
asyncio.run(main(host))

print("=" * 50)
print("Open Ports")
print("=" * 50)
for port, alive in ports_map.items():
    if alive:
        print(f"127.0.0.1:{port}")
