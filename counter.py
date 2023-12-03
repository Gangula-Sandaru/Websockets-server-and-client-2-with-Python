import asyncio
import json
import logging
import websockets
import random
logging.basicConfig()

USERS = set()

VALUE = 0

MESSAGE = ""


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def value_event():
    return json.dumps({"type": "value", "value": VALUE})


def message_event(MESSAGE):
    return json.dumps({"type": "message", "value": MESSAGE})

def userID():
    return random.randint(000, 999)


async def counter(websocket):
    global USERS, VALUE, MESSAGE
    try:
        # register user
        # uKey = userID()
        # if uKey not in USERS:
        #     USERS[uKey] = websocket
        # else:
        #     while True:
        #         uKey = userID()
        #         if uKey not in USERS:
        #             USERS[uKey] = websocket
        #             break
        #
        #
        #
        # print(USERS)

        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())
        # send current state to user
        await websocket.send(value_event())
        # manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(USERS)
            if "action" in event:
                if event["action"] == "minus":
                    VALUE -= 1
                    websockets.broadcast(USERS, value_event())
                elif event["action"] == "plus":
                    VALUE += 1
                    websockets.broadcast(USERS, value_event())
                else:
                    logging.error("unsupported event: %s", event)
            elif "mgs" in event:

                if not (websocket in USERS == websocket):
                    print("hi")
                    websockets.broadcast(USERS, message_event(event["mgs"]))
            else:
                print("invalid key")
    finally:
        # USERS.pop(websocket)
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())


async def main():
    async with websockets.serve(counter, "localhost", 6789):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
