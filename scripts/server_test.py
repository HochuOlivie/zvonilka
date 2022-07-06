# !/bin/python3
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from time import sleep
import json
from datetime import datetime, timedelta
from threading import Thread

from MainParser.models import Ad, User, Profile, TargetAd

from asgiref.sync import sync_to_async
from scripts.server.client import Client

# for timezones
import pytz

utc = pytz.UTC

clients = []


def getCalls():
    while True:
        try:
            ads = list(Ad.objects.filter(tmpDone=False, done=False, noCall=False))
            ads.sort(key=lambda x: x.date)
            ads.reverse()
            calls = ads[:min(len(ads), 30)]
            calls = [call for call in calls if
                     call.date + timedelta(minutes=10, hours=3) > utc.localize(datetime.now())]
            if len(calls) != 0:
                print('Calls:', len(calls))

            can_call = [x for x in clients if x.ready and x.lastCall + timedelta(seconds=3) < datetime.now()]
            for call in calls:
                for worker in can_call:
                    is_working = await worker.working()
                    if not is_working:
                        continue
                    await worker.makeCall(call)

        except Exception as e:
            print(f'Error: {e}')


Thread(target=getCalls).start()



@sync_to_async
def get_target_ads(user):
    ads = list(TargetAd.objects.filter(user=user, done=False))
    ads = [x.ad for x in ads]
    if ads:
        return ads
    return []


async def main(websocket: WebSocketServerProtocol, path):
    client = Client(websocket)
    clients.append(client)

    while True:
        try:
            recv = await websocket.recv()
            await client.parse_recv(recv)

        except Exception as e:
            print(e)
            clients.remove(Client)
            return


def run():
    start_server = websockets.serve(main, "213.108.4.86", 32212)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
