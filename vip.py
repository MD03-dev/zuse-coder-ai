#!/usr/bin/env python3
import asyncio, json, platform, os, time, socket

def get_system_info():
    info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "uptime_seconds": int(time.time() - os.stat('/proc/1').st_ctime) if os.path.exists('/proc/1') else None,
        "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None,
        "environment": dict(os.environ)
    }
    return info

async def handle(reader, writer):
    request = await reader.read(1024)  # read request (ignore content)
    info = get_system_info()
    body = json.dumps(info, indent=2).encode()
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json; charset=utf-8\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n" + body
    )
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 8080)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"VIP system info server running on {addrs} (access http://localhost:8080)")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
