import asyncio
import websockets
import queue

MESSAGE_TYPE = 0
SHOOT_MESSAGE = 0  # [0]
MOVE_MESSAGE = 1  # [1, up, down, left, right]
START_MESSAGE = 69
UPDATING_LIFE = 0  # [2, amount]
UPDATING_SCORE = 1
DEATH = 2

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


class MoveMessage:
    def __init__(self, client_id, up, down, left, right):
        self.client_id = client_id
        self.up = up
        self.down = down
        self.left = left
        self.right = right


class NewPlayerMessage:
    pass


class StartMessage:
    pass


class KillPlayerMessage:
    def __init__(self, client_id):
        self.client_id = client_id


class ShootMessage:
    def __init__(self, client_id):
        self.client_id = client_id


class WebsocketServer:
    COUNT = 0

    def __init__(self):
        # init of all functions
        self.new_player = lambda id: print("Player ", id, " connected")
        self.on_move = lambda id, a, b, c, d: print("Recv data from", id, ":", a, b, c, d)
        self.shoot = lambda id: print("Player ", id, " is shooting")
        self.clients = []
        self.gameClientId = []

    async def set_life(self, client_id, life):
        print("Player", client_id, "have", life, "life(s)")
        await self.send_to_client(client_id, bytes([UPDATING_LIFE, life]))
        await self.send_to_client(client_id, bytes([3]))

    async def set_score(self, client_id, score):
        print("Player", client_id, "have a score of", score)
        await self.send_to_client(client_id, bytes([UPDATING_SCORE, *score.to_bytes(4, "big")]))

    async def die(self, client_id):
        await self.send_to_client(client_id, bytes([DEATH]))

    async def send_to_client(self, client_id, data):
        print(data)
        await self.clients[client_id].send(data)

    def send_die_message(self, client_id):
        self.gameClientId = list(map(lambda x: x[1] - 1 if x[0] > client_id else x[1], enumerate(self.gameClientId)))
        self.queue.put(KillPlayerMessage(client_id))
        del self.clients[client_id]
        WebsocketServer.COUNT -= 1

    async def handle_usr(self, websocket):
        self.clients.append(websocket)
        client_id = WebsocketServer.COUNT
        self.gameClientId.append(client_id)
        WebsocketServer.COUNT += 1
        self.new_player(client_id)
        self.queue.put(NewPlayerMessage())
        while True:
            try:
                data_ws = await websocket.recv()
                await self.try_handle_ptw()
                if not (repr(type(data_ws)) == "<class 'bytes'>"):
                    print("Incorrect type")
                    await websocket.close()
                    self.send_die_message(client_id)
                    return

                # In case of move message
                if data_ws[MESSAGE_TYPE] == MOVE_MESSAGE:
                    message = MoveMessage(self.gameClientId[client_id], data_ws[UP], data_ws[DOWN], data_ws[LEFT],
                                          data_ws[RIGHT])
                    self.queue.put(message)
                # In case of a shooting message
                if data_ws[MESSAGE_TYPE] == SHOOT_MESSAGE:
                    self.queue.put(ShootMessage(self.gameClientId[client_id]))

                if data_ws[MESSAGE_TYPE ] == START_MESSAGE:
                    self.queue.put(StartMessage())

            # If connection lost
            except websockets.exceptions.WebSocketException:
                print("Player ", client_id, " disconnected")
                await websocket.close()
                self.send_die_message(client_id)
                break

    async def try_handle_ptw(self):
        try:
            message = self.ptw.get(block=False)
            if message[0] == UPDATING_LIFE:
                client_id = self.gameClientId.index(message[1])
                if client_id == 0 and not self.ph:
                    return
                life = message[2]
                await self.set_life(client_id, life)
                print("UPDATTTEDDDD")
            if message[0] == UPDATING_SCORE:
                client_id = self.gameClientId.index(message[1])
                if client_id == 0 and not self.ph:
                    return
                score = message[2]
                await self.set_score(client_id, score)
                print("UPDATTTEDDDD")
        except queue.Empty:
            pass

    async def run(self, queue, ph, ptw):
        self.queue = queue
        self.ptw = ptw
        self.ph = ph
        if not ph:
            WebsocketServer.COUNT += 1
            self.gameClientId.append(0)
            self.clients.append(0)
        print("Started websockets")
        async with websockets.serve(self.handle_usr, "0.0.0.0", 8000):
            await asyncio.Future()
        print("end")


async def main():
    ws = WebsocketServer()
    await ws.server()


if __name__ == "__main__":
    asyncio.run(main())
