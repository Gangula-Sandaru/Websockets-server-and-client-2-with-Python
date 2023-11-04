import websockets
import asyncio


async def hello(websocket):
    name = await websocket.recv()
    print(f"<<<{name}")

    greeting = f"hello {name}!"
    await  websocket.send(greeting)
    print(f">>{greeting}")


async def main():
    async with websockets.serve(hello, "", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
