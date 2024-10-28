import asyncio
from ArgHandler import ArgHandler


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
            ports_map[port] = True
        else:
            print(f"{ip}:{port} encountered an error: {e}")


async def main(host, batch_size):
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


def get_ports_list(ports_arg: str) -> list:
    ports = []

    # Range
    if "-" in ports_arg:
        pr = ports_arg.split("-")
        port_start, port_end = pr
        ports = [port for port in range(int(port_start), int(port_end) + 1)]

    # Specified list
    if "," in ports_arg:
        ports_split = ports_arg.split(",")
        ports = ports_split

    # Default
    if len(ports) == 0:
        # if no ports built into list, fallback to default (1-100)
        ports = [port for port in range(1, 101)]

    return ports


if __name__ == "__main__":
    #
    # Python port scanner
    #
    print("=" * 50)
    print("The Nightman Scanneth")
    print("=" * 50)

    args = ArgHandler().get_args()

    host = args.host
    ports = get_ports_list(args.ports)
    ports_map = {port: False for port in ports}
    batch_size = args.concurrent
    protocol = "TCP"

    print(f"Scanning Host:\t\t[{host}]")
    print(f"Scanning Ports:\t\t[{ports[0]}-{ports[-1]}][{protocol}]")
    print(f"Concurrent Requests:\t[{batch_size}]")
    print("\n")

    asyncio.run(main(host, batch_size))

    print("=" * 50)
    print("Open Ports")
    print("=" * 50)
    for port, alive in ports_map.items():
        if alive:
            print(f"127.0.0.1:{port}")
