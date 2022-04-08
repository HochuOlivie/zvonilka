#!/bin/python3
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from time import sleep
import json
from datetime import datetime

from MainParser.models import Ad, User, Profile

from asgiref.sync import sync_to_async

# for timezones
import pytz

utc = pytz.UTC


@sync_to_async
def get_last_ads():
    ads = list(Ad.objects.filter(tmpDone=False))
    ads.sort(key=lambda x: x.date)
    ads.reverse()
    ads = ads[:min(len(ads), 10)]
    ads = [x for x in ads if x.phone]
    return ads


@sync_to_async
def ad_done(id, name):
    ad = Ad.objects.filter(id=int(id))
    if not ad:
        print("NO AD IN TALBE???")
        return

    ad = ad[0]
    ad.done = True
    ad.person = name
    ad.save()
    print('saving ad with done')


@sync_to_async
def ad_tmp_done(id):
    ad = Ad.objects.filter(id=int(id))
    if not ad:
        print("No ad in table...")
        return
    ad = ad[0]
    ad.tmpDone = True
    ad.save()
    print('saved tmpDone = True')


@sync_to_async
def ad_tmp_undone(id):
    ad = Ad.objects.filter(id=int(id))
    if not ad:
        return
    ad = ad[0]
    ad.tmpDone = False
    ad.save()


@sync_to_async
def authorize_user(phone: str):
    phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')

    if phone[0] == '8':
        phone = '7' + phone[1:]

    user = User.objects.filter(username=phone)
    if not user:
        return False

    profile = Profile.objects.filter(user=user[0])
    if profile:
        return profile[0].name

    print("Нет профиля((()))")
    return False


async def main(websocket: WebSocketServerProtocol, path):
    start_moment = utc.localize(datetime.now())

    print(f"Connected to client: {websocket.remote_address[0]}")

    ans = await websocket.recv()
    my_phone = ""
    ready = True
    name = ""

    while True:
        ans = json.loads(ans)
        if ans['type'] != "new_phone":
            ans = await websocket.recv()
            print(ans)
            continue

        my_phone = ans["value"]
        name = await authorize_user(my_phone)

        if not name:
            await websocket.send(json.dumps({"type": "auth", "status": "False"}))
            ans = await websocket.recv()
            continue

        await websocket.send(json.dumps({'type': 'auth', 'status': 'True', 'value': name}))

        break

    print(f"Got phone: {my_phone}")

    while True:
        try:
            ans = await websocket.recv()
            print(ans)
            ans = json.loads(ans)
            print(f"{websocket.remote_address[0]}: {ans}")
            if ans['type'] == 'status':
                if ans.get('value') == "ready":
                    ready = True
                else:
                    ready = False

            if ans.get('type') == 'call' and ans.get('state') == 'accept':
                await ad_done(ans.get('id'), name)

            elif ans.get('type') == 'call' and ans.get('state') == 'decline':
                await ad_tmp_undone(ans.get('id'))

            if ready:
                ads = await get_last_ads()

                for a in ads:
                    date = a.date
                    phone = a.phone
                    print(f"{a.id}) Check {date}, {phone}, Done: {a.done}")
                    if date > start_moment or True:
                        print(f"Send {phone}")
                        await websocket.send(json.dumps({"type": "call", "value": a.phone, 'id': a.id}))
                        await ad_tmp_done(a.id)
                        ready = False
                        break

        except Exception as e:
            print(e)
            print(f"{websocket.remote_address[0]} Connection closed")
            return


def run():
    start_server = websockets.serve(main, "164.92.239.167", 32222)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
