import websockets
from websockets.legacy.server import WebSocketServerProtocol
from scripts.server.protocol import PROTOCOL
from asgiref.sync import sync_to_async
from MainParser.models import Ad, User, Profile, TargetAd
import datetime
import json
from scripts.server.settings import DEBUG
import asyncio

from zvonilka_test_phones.models import TestCall


class Client:

    def __init__(self, websocket: WebSocketServerProtocol):
        self.ready: bool = True

        self.authorized: bool = False
        self.name = ''
        self.user = None
        self.phone = ''
        self.ip = websocket.remote_address[0]

        self.websocket = websocket
        self.lastCall = datetime.datetime.now() - datetime.timedelta(seconds=15)

    async def parse_recv(self, recv, ads, target_ads):
        recv = recv.replace('\n', '')
        try:
            recv = json.loads(recv)
            if DEBUG:
                print(f"{self.ip}: {recv}")
        except Exception as e:
            if DEBUG:
                print(f'[RECV ERROR]: {recv}, {e}')
            return

        if recv['type'] == PROTOCOL.NEW_PHONE:
            self.phone = recv["value"]

            user, name = await self.authorize(self.phone)

            if not name:
                await self.websocket.send(json.dumps({"type": "auth", "status": "False"}))
            else:
                self.user = user
                self.name = name
                self.authorized = True

                # Check default calls
                await self.websocket.send(json.dumps({'type': 'auth', 'status': 'True', 'value': name}))
                await self._try_to_call(ads)

                # Check target calls
                print("Check target ads...")

                @sync_to_async
                def get_users():
                    return [x.user for x in target_ads]

                @sync_to_async
                def tmp_foo_1(target_ad):
                    return target_ad.ad

                target_ads_users = await get_users()
                print("Users in target ads:", target_ads_users)
                if self.user in target_ads_users:
                    target_ad = [x for x in target_ads if x.user == self.user][0]
                    print("Making target call!!")
                    await self.makeTargetCall(await tmp_foo_1(target_ad))
                    print("Deleting...")
                    del target_ads[target_ads.index(target_ad)]

        elif recv['type'] == PROTOCOL.STATUS:
            if recv.get('value') == "ready" and self.lastCall + datetime.timedelta(seconds=3) < datetime.datetime.now():
                self.ready = True
                if self.user and ads:
                    await self._try_to_call(ads)
            else:
                self.ready = False

        elif recv.get('type') == 'call' and recv.get('state') == 'accept':
            id = recv.get('id').split('_')
            if id[1] == 'test':
                return await self.test_call_done(int(id[0]))

            elif id[1] == 'target':
                await self.target_done(int(id[0]))

            await self.ad_done(int(id[0]))

        elif recv.get('type') == 'call' and recv.get('state') == 'decline':
            await self.ad_tmp_undone(recv.get('id'))

    async def _try_to_call(self, ads):
        print("Try to make call!")
        is_working = await self.working()
        if ads and is_working:
            async with asyncio.Lock():
                cur_ads = ads[-1]
                del ads[-1]
                await self.makeCall(cur_ads)

    async def makeCall(self, call: Ad):
        time_now = datetime.datetime.now()
        self.ready = False
        call.date_done = time_now
        call.tmpDone = True
        await sync_to_async(call.save)()
        self.lastCall = time_now
        phone = call.phone

        await self.websocket.send(json.dumps({"type": PROTOCOL.CALL, "value": phone,
                                              'id': str(call.id) + '_default'}))

        if DEBUG:
            print(f'New call: {phone}')

    async def makeTargetCall(self, call: Ad):
        time_now = datetime.datetime.now()
        self.ready = False
        self.lastCall = time_now
        phone = call.phone
        call.date_done = time_now
        call.tmpDone = True
        await sync_to_async(call.save)()
        await self.websocket.send(json.dumps({"type": PROTOCOL.CALL, "value": phone,
                                              'id': str(call.id) + '_target'}))

        if DEBUG:
            print(f'New call: {phone}')

    async def make_test_call(self, test_call: TestCall, test_phone: str):
        await self.websocket.send(json.dumps({"type": PROTOCOL.CALL, "value": test_phone,
                                              'id': str(test_call.id) + '_test'}))

    @sync_to_async
    def check_target(self):
        ads = list(TargetAd.objects.filter(user=self.user, done=False))
        if len(ads):
            return ads[0].ad

    @sync_to_async
    def working(self):
        print(self.user, "user")
        profile = Profile.objects.get(user=self.user)
        return profile.working

    @sync_to_async
    def test_call_done(self, id):
        datetime_now = datetime.datetime.now()
        test_call = TestCall.objects.get(id=id)
        test_call.date_done = datetime_now
        test_call.save(update_fields=['date_done'])

    @sync_to_async
    def target_done(self, id):
        ads = TargetAd.objects.all()
        ads = [x for x in ads if x.ad.id == id]
        if not ads:
            return

        ad = ads[0]
        ad.delete()

    @sync_to_async
    def ad_done(self, id):
        ad = Ad.objects.filter(id=int(id))
        if not ad:
            return

        ad = ad[0]
        ad.done = True
        ad.person = self.user
        ad.save()

    @sync_to_async
    def ad_tmp_done(self, id):
        ad = Ad.objects.filter(id=int(id))
        if not ad:
            return
        ad = ad[0]
        ad.tmpDone = True
        ad.save()

    @sync_to_async
    def ad_tmp_undone(self, id):
        id = id.split('_')[0]
        ad = Ad.objects.filter(id=int(id))
        if not ad:
            return

        ad = ad[0]
        ad.tmpDone = False
        ad.save()

    @sync_to_async
    def authorize(self, phone):
        phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')

        if phone[0] == '8':
            phone = '7' + phone[1:]

        user = User.objects.filter(username=phone)
        if not user:
            return False, False

        profile = Profile.objects.filter(user=user[0])
        if profile:
            return user[0], profile[0].name

        return False, False
