#!/usr/bin/env python
 
import asyncio
import time
import websockets
import websockets.client
 
 
async def hello():
    async with websockets.client.connect("ws://localhost:8765") as websocket:
        while True:
            # await websocket.send("Hello world!")
            message = await websocket.recv()
            print(f"Received: {message}")
            time.sleep(1)
 
 
asyncio.get_event_loop().run_until_complete(hello())