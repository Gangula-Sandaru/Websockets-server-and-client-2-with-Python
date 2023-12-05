import asyncio
import websockets

connected_users = {}


async def handle_websocket(websocket, path):
    user_id = path.lstrip('/')
    connected_users[user_id] = websocket
    print(f"User {user_id} connected.")

    try:
        while True:
            message = await websocket.recv()
            print(f"Received message from user {user_id}: {message}")
            await process_message(user_id, message)
    except websockets.exceptions.ConnectionClosed:
        del connected_users[user_id]
        print(f"User {user_id} disconnected.")


async def process_message(sender_id, message):

    if message.startswith("Broadcast:"):
        b_mgs = message[len("Broadcast:"):]
        for user_id, user_ws in connected_users.items():
            await user_ws.send(f"Broadcast message from {sender_id}: {b_mgs}")

    elif message.startswith("Specific:"):
        _, r_id, specific_msg = message.split(':', 2)
        if r_id in connected_users:
            recipient_ws = connected_users[r_id]
            await recipient_ws.send(f"Message for {r_id} from {sender_id}: {specific_msg}")


async def main():
    async with websockets.serve(handle_websocket, "", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
