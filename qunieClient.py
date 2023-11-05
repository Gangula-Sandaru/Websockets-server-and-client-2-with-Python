import asyncio
import websockets

# Store connected users
connected_users = {}


async def handle_websocket(websocket, path):
    user_id = path.lstrip('/')  # Extracting user ID from the URL path

    # Store the WebSocket connection for the specific user
    connected_users[user_id] = websocket
    print(f"User {user_id} connected.")

    try:
        while True:
            # Receive message from the user
            message = await websocket.recv()
            print(f"Received message from user {user_id}: {message}")

            # Process the message - check for broadcasting or sending to a specific user
            await process_message(user_id, message)
    except websockets.exceptions.ConnectionClosed:
        # Remove the user from the connected users dictionary upon disconnection
        del connected_users[user_id]
        print(f"User {user_id} disconnected.")


async def process_message(sender_id, message):
    # Broadcast message to all connected users
    if message.startswith("Broadcast:"):
        broadcast_msg = message[len("Broadcast:"):]
        for user_id, user_ws in connected_users.items():
            await user_ws.send(f"Broadcast message from {sender_id}: {broadcast_msg}")
    # Send message to a specific user
    elif message.startswith("Specific:"):
        _, recipient_id, specific_msg = message.split(':', 2)
        if recipient_id in connected_users:
            recipient_ws = connected_users[recipient_id]
            await recipient_ws.send(f"Message for {recipient_id} from {sender_id}: {specific_msg}")


async def main():
    async with websockets.serve(handle_websocket, "", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
