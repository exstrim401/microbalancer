import asyncio
import aiohttp
from aiohttp import web


SERVERS = ["http://127.0.0.1:8081", "http://127.0.0.1:8082"]
i = 0


async def handler(request):
    global i
    if i == len(SERVERS)-1:
        i = 0
    else:
        i += 1
    print(f"Request to {SERVERS[i]}")
    resp = None
    if request.method == "GET":
        async with session.get(SERVERS[i]+str(request.rel_url)) as r:
            resp = r
            text = await resp.text()
    elif request.method == "POST":
        data = await request.post()
        async with session.post(SERVERS[i]+str(request.rel_url),
                                data=data) as r:
            resp = r
            text = await resp.text()
    return web.Response(text=text, status=resp.status,
                        content_type=resp.content_type)


async def main():
    global session
    session = aiohttp.ClientSession()
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Serving")



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
loop.close()
