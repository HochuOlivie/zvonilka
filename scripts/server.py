#!/bin/python3
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from time import sleep
import json
from datetime import datetime

from MainParser.models import Ad, User, Profile, TargetAd

from asgiref.sync import sync_to_async
import logging

# for timezones
import pytz

utc = pytz.UTC

FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO)
server = logging.FileHandler('logs/server.log')
server.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger('server')
logger.addHandler(sheetParser)
logger.propagate = False


@sync_to_async
def get_last_ads():
    ads = list(Ad.objects.filter(tmpDone=False, done=False, noCall=False))
    ads.sort(key=lambda x: x.date)
    ads.reverse()
    ads = ads[:min(len(ads), 10)]
    ads = [x for x in ads if x.phone]
    return ads


@sync_to_async
def get_target_ads(user):
    ads = list(TargetAd.objects.filter(user=user, done=False))
    ads = [x.ad for x in ads]
    if ads:
        return ads
    return []


@sync_to_async
def working(user):
    profile = Profile.objects.get(user=user)
    return profile.working


@sync_to_async
def ad_done(id, name):
    ad = Ad.objects.filter(id=int(id))
    if not ad:
        return

    ad = ad[0]
    ad.done = True
    ad.person = name
    ad.save()


@sync_to_async
def target_done(id):
    ads = TargetAd.objects.all()
    ads = [x for x in ads if x.ad.id == id]
    if not ads:
        return

    ad = ads[0]
    ad.delete()


@sync_to_async
def ad_tmp_done(id):
    ad = Ad.objects.filter(id=int(id))
    if not ad:
        return
    ad = ad[0]
    ad.tmpDone = True
    ad.save()


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
    if not phone:
        return False, False

    phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')

    if phone[0] == '8':
        phone = '7' + phone[1:]

    user = User.objects.filter(username=phone)
    if not user:
        return False, False

    profile = Profile.objects.filter(user=user[0])
    if profile:
        logger.info(f"Authorized: {profile[0].name} - {phone}")
        return user[0], profile[0].name

    return False, False


async def main(websocket: WebSocketServerProtocol, path):
    start_moment = utc.localize(datetime.now())

    logger.info(f"Connected: {websocket.remote_address[0]}")

    ans = await websocket.recv()
    my_phone = ""
    ready = True
    user, name = None, ""

    while True:
        ans = ans.replace('\n', '')
        ans = json.loads(ans)
        if ans['type'] != "new_phone":
            ans = await websocket.recv()
            continue

        my_phone = ans["value"]
        user, name = await authorize_user(my_phone)

        if not name:
            logger.info(f"Bad authorize: {my_phone}")
            await websocket.send(json.dumps({"type": "auth", "status": "False"}))
            ans = await websocket.recv()
            continue

        await websocket.send(json.dumps({'type': 'auth', 'status': 'True', 'value': name}))
        break

    while True:
        try:
            ans = await websocket.recv()
            ans = ans.replace('\n', '')
            logger.info(f"Got message: {websocket.remote_address[0]} - {ans}")
            ans = json.loads(ans)

            if ans['type'] == 'status':
                if ans.get('value') == "ready":
                    ready = True
                else:
                    ready = False

            if ans.get('type') == 'call' and ans.get('state') == 'accept':
                id = ans.get('id').split('_')
                if id[1] == 'target':
                    await target_done(int(id[0]))

                await ad_done(int(id[0]), name)

            elif ans.get('type') == 'call' and ans.get('state') == 'decline':
                await ad_tmp_undone(ans.get('id'))

            db_ready = await working(user)
            if ready and db_ready:
                ads = await get_target_ads(user)

                for a in ads:
                    phone = a.phone
                    logger.info(f"Target call to {name} - {phone}")
                    await websocket.send(json.dumps({"type": "call", "value": phone, 'id': str(a.id) + '_target'}))
                    await ad_tmp_done(a.id)
                    ready = False
                    break

                ads = await get_last_ads()

                for a in ads:
                    date = a.date
                    phone = a.phone
                    if date > start_moment:
                        logger.info(f"New call to {name} - {phone}")
                        await websocket.send(
                            json.dumps({"type": "call", "value": phone, 'id': str(a.id) + '_default'}))
                        await ad_tmp_done(a.id)
                        ready = False
                        break

        except Exception as e:
            logger.error(f"{websocket.remote_address[0]}: {e}")
            logger.info(f"{websocket.remote_address[0]} Connection closed")
            return


def run():
    start_server = websockets.serve(main, "164.92.239.167", 32222)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
