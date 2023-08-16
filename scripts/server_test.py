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


async def get_db_connection() -> asyncpg.Connection:
    return await asyncpg.connect(**DB_AUTH)


async def listen_create_channel(callback: callable):
    conn = await get_db_connection()
    print("Init create channel...")
    await conn.add_listener(DB_CREATE_CHANNEL, callback)
    while True:
        await asyncio.sleep(10)


async def listen_update_channel(callback: callable):
    conn = await get_db_connection()
    await conn.add_listener(DB_UPDATE_CHANNEL, callback)


async def clear_old_ads():
    while True:
        try:
            current_ads[:] = [x for x in current_ads if x.date + timedelta(minutes=2, hours=3) > datetime.now()]
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

# Thread(target=targets_wrapper).start()
# if not DEBUG:
#    Thread(target=gui).start()


async def main(websocket: WebSocketServerProtocol, path):
    client = Client(websocket)
    clients.append(client)
    if DEBUG:
        print('New client!')

    while True:
        try:
            recv = await websocket.recv()
            await client.parse_recv(recv, current_ads)

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
        listen_update_channel(on_create_ad),
    ]
    await asyncio.gather(*tasks)


def run():
    asyncio.run(run_main())
