# !/bin/python3
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from time import sleep
import json
from datetime import datetime, timedelta
from threading import Thread

from MainParser.models import Ad, Profile, TargetAd

import asyncpg
from asgiref.sync import sync_to_async
from scripts.server.client import Client
import os
from scripts.server.settings import DEBUG
from random import shuffle

# for timezones
import pytz

utc = pytz.UTC

clients = []
ready_calls = 0

DB_AUTH = {
    'database': os.getenv('DB_DATABASE', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '17628312D'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
}

DB_CREATE_CHANNEL = 'new_ads_channel'
DB_UPDATE_CHANNEL = 'update_ads_channel'


async def get_db_connection() -> asyncpg.Connection:
    return await asyncpg.connect(**DB_AUTH)


async def listen_create_channel(callback: callable):
    conn = await get_db_connection()
    await conn.add_listener(DB_CREATE_CHANNEL, callback)


async def listen_update_channel(callback: callable):
    conn = await get_db_connection()
    await conn.add_listener(DB_UPDATE_CHANNEL, callback)


# @sync_to_async
# def getAds():
#     return list(Ad.objects.filter(tmpDone=False, done=False, no_call=False).order_by('-id')[:50])


async def on_create_ad(*args):
    connection, pid, channel, payload = args
    record: Ad = await sync_to_async(Ad.objects.get)(id=int(payload))
    if record.noCall or record.phone == '+74954760059' or record.clearColor:
        return
    await make_call(record)


async def make_call(ad: Ad):
    shuffle(clients)

    workers = [x for x in clients if
               x.ready and x.lastCall + timedelta(seconds=3) < datetime.now() and x.authorized]

    for worker in workers:
        is_working = await worker.working()
        if not is_working:
            continue
        worker.ready = False
        await worker.makeCall(ad)


# async def getCalls():
#     global ready_calls
#     while True:
#         try:
#             ads = await getAds()
#
#             calls = [call for call in ads if
#                      call.date + timedelta(minutes=2, hours=3) > utc.localize(datetime.now())]
#
#             calls = [call for call in calls if
#                      call.views <= 700 and call.phone != '+74954760059' and not call.clearColor]
#
#             ready_calls = len(calls)
#             shuffle(clients)
#
#             for call in calls:
#                 workers = [x for x in clients if
#                            x.ready and x.lastCall + timedelta(seconds=3) < datetime.now() and x.authorized]
#                 for worker in workers:
#                     is_working = await worker.working()
#                     if not is_working:
#                         continue
#                     print(f"wanna call: {worker.ready}, {call.phone}")
#                     worker.ready = False
#                     await worker.makeCall(call)
#                     break
#
#         except Exception as e:
#             if DEBUG or 1 == 1:
#                 print(f'Error: {e}')
#             await asyncio.sleep(5)


# def calls_wrapper():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(getCalls())
#     loop.close()


async def checkTargets():
    while True:
        try:
            for worker in clients:
                if not worker.ready or worker.lastCall + timedelta(seconds=3) > datetime.now() or not worker.authorized:
                    continue

                ad = await worker.check_target()
                if ad:
                    await worker.makeTargetCall(ad)
            await asyncio.sleep(5)

        except Exception as e:
            if DEBUG:
                print(f'Targets error: {e}')
            await asyncio.sleep(5)


def targets_wrapper():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(checkTargets())
    loop.close()


def gui():
    while True:
        ans = f'SERVER IS RUNNING!\n\n'
        ans += f'Total clients online: {len(clients)}\n'
        ans += f'Free phones: {ready_calls}\n\n'
        for client in clients:
            ans += f"{client.ip}\t"
            if client.authorized:
                ans += f'{client.phone}\t{client.name}\t'
                if client.ready:
                    ans += f'ready'
                else:
                    ans += f'not ready'
            ans += '\n'

        os.system('clear')
        print(ans)
        sleep(3)


# Thread(target=calls_wrapper).start()

# TODO: await listen_create_channel(on_create_ad)

Thread(target=targets_wrapper).start()
if not DEBUG:
    Thread(target=gui).start()


async def main(websocket: WebSocketServerProtocol, path):
    client = Client(websocket)
    clients.append(client)
    if DEBUG:
        print('New client!')

    while True:
        try:
            recv = await websocket.recv()
            await client.parse_recv(recv)

        except Exception as e:
            if DEBUG:
                print(e)
            clients.remove(client)
            return


def run():
    start_server = websockets.serve(main, "10.31.12.48", 33925)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
