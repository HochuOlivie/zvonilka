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
current_ads = []
current_target_ads = [*TargetAd.objects.filter(done=False).all()]
print("Current target ads: ", current_target_ads)
ready_calls = 0

DB_AUTH = {
    'database': os.getenv('DB_DATABASE', 'postgres'),
    'user': os.getenv('DB_USER', 'zvonilka'),
    'password': os.getenv('DB_PASSWORD', 'zv0n1lka342kk'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '33924'),
}

DB_CREATE_CHANNEL = 'new_ads_channel'
DB_UPDATE_CHANNEL = 'update_ads_channel'
DB_CREATE_TARGET_CHANNEL = 'new_target_channel'


async def get_db_connection() -> asyncpg.Connection:
    return await asyncpg.connect(**DB_AUTH)


async def listen_create_channel(callback: callable):
    conn = await get_db_connection()
    print("Init create channel...")
    await conn.add_listener(DB_CREATE_CHANNEL, callback)
    while True:
        await asyncio.sleep(10)


async def lister_create_target_channel(callback: callable):
    conn = await get_db_connection()
    print("Init create target channel...")
    await conn.add_listener(DB_CREATE_TARGET_CHANNEL, callback)
    while True:
        await asyncio.sleep(10)


async def clear_old_ads():
    while True:
        try:
            current_ads[:] = [x for x in current_ads if x.date + timedelta(minutes=2, hours=3) > datetime.now()]
            print("Current ads:", current_ads)
            await asyncio.sleep(60)
        except Exception as e:
            if DEBUG:
                print(f'Clear old ads error: {e}')
            await asyncio.sleep(60)


async def on_create_ad(*args):
    print("New ad was created!")
    connection, pid, channel, payload = args
    record: Ad = await sync_to_async(Ad.objects.get)(id=int(payload))
    print(record)
    if record.no_call or record.phone == '+74954760059' or record.clearColor:
        return
    await make_call(record)


async def on_create_target_ad(*args):
    print("New target ad was created!")
    connection, pid, channel, payload = args
    record: TargetAd = await sync_to_async(TargetAd.objects.get)(id=int(payload))
    print(record)
    await make_target_call(record)


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
        break
    else:
        current_ads.append(ad)


async def make_target_call(ad: TargetAd):
    users = [x.user for x in clients if x.authorized and x.ready]
    target_user = ad.user
    print("Target user:", target_user)
    if target_user in users:
        client = [x for x in clients if x.user == target_user][0]
        client.ready = False
        print("Making target call!!")
        await client.makeTargetCall(ad)


async def main(websocket: WebSocketServerProtocol, path):
    client = Client(websocket)
    clients.append(client)
    if DEBUG:
        print('New client!')

    while True:
        try:
            recv = await websocket.recv()
            await client.parse_recv(recv, current_ads, current_target_ads)

        except Exception as e:
            if DEBUG:
                print(e)
            clients.remove(client)
            return


async def run_main():
    start_server = websockets.serve(main, "10.31.12.48", 33925)
    tasks = [
        start_server,
        clear_old_ads(),
        listen_create_channel(on_create_ad),
        lister_create_target_channel(on_create_target_ad)
    ]
    await asyncio.gather(*tasks)


def run():
    asyncio.run(run_main())
