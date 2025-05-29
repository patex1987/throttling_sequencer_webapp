import asyncio, json, websockets

from websockets import Subprotocol


async def main():
    uri = "ws://localhost:8080/graphql"
    async with websockets.connect(uri, subprotocols=[Subprotocol("graphql-ws")]) as ws:
        # 1) Init
        await ws.send(json.dumps({"type": "connection_init"}))
        await ws.recv()

        # 2) Start the subscription
        with open("subscription_example.json", "r") as f:
            query_body = json.load(f)

        await ws.send(json.dumps(query_body))
        # await ws.send(json.dumps({
        #     "id": "1",
        #     "type": "start",
        #     "payload": {
        #         "query": """
        #             subscription SubscribeSteps($gameStateInput: GameStateInputType!) {
        #               generateSteps(gameStateInput: $gameStateInput) {
        #                 coordinate { x y }
        #                 throttle
        #               }
        #             }
        #         """,
        #         "variables": {
        #             "gameStateInput": {
        #                 "playerUnits": [
        #                     {
        #                         "coordinate": { "x": 0.0, "y": 0.0 },
        #                         "speed": 0.0,
        #                         "mass": 10.0,
        #                         "friction": 0.01
        #                     }
        #                 ],
        #                 "enemyUnits": [
        #                     {
        #                         "coordinate": { "x": 0.0, "y": 5000.0 },
        #                         "speed": 0.0,
        #                         "mass": 50.0,
        #                         "friction": 0.8
        #                     }
        #                 ]
        #             }
        #         }
        #     }
        # }))

        # 3) Receive data
        try:
            while True:
                message = await ws.recv()
                msg = json.loads(message)
                if msg.get("type") == "data":
                    payload = msg["payload"]["data"]["generateSteps"]
                    print("Step:", payload)
                elif msg.get("type") == "complete":
                    print("Subscription complete")
                    break
        except websockets.ConnectionClosed:
            print("WebSocket closed")

asyncio.run(main())
