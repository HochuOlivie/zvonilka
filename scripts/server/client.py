import websockets
from websockets.legacy.server import WebSocketServerProtocol
from scripts.server.protocol import PROTOCOL
from asgiref.sync import sync_to_async
from MainParser.models import Ad, User, Profile, TargetAd
import datetime
import json
from scripts.server.settings import DEBUG


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

    async def parse_recv(self, recv):
        recv = recv.replace('\n', '')
        try:
            recv = json.loads(recv)
            if DEBUG:
                print(recv)
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
                await self.websocket.send(json.dumps({'type': 'auth', 'status': 'True', 'value': name}))

        elif recv['type'] == PROTOCOL.STATUS:
            if recv.get('value') == "ready" and self.lastCall + datetime.timedelta(seconds=3) < datetime.datetime.now():
                self.ready = True
            else:
                self.ready = False

        elif recv.get('type') == 'call' and recv.get('state') == 'accept':
            id = recv.get('id').split('_')
            if id[1] == 'target':
                await self.target_done(int(id[0]))

            await self.ad_done(int(id[0]))

        elif recv.get('type') == 'call' and recv.get('state') == 'decline':
            await self.ad_tmp_undone(recv.get('id'))

    async def makeCall(self, call: Ad):
        self.ready = False
        self.lastCall = datetime.datetime.now()
        phone = call.phone
        await self.ad_tmp_done(call.id)
        await self.websocket.send(json.dumps({"type": PROTOCOL.CALL, "value": phone,
                                              'id': str(call.id) + '_default'}))
        if DEBUG:
            print(f'New call: {phone}')
            
    async def makeTargetCall(self, call: Ad):
        self.ready = False
        self.lastCall = datetime.datetime.now()
        phone = call.phone
        await self.ad_tmp_done(call.id)
        await self.websocket.send(json.dumps({"type": PROTOCOL.CALL, "value": phone,
                                              'id': str(call.id) + '_target'}))
        if DEBUG:
            print(f'New call: {phone}')

    @sync_to_async
    def check_target(self):
        ads = list(TargetAd.objects.filter(user=self.user, done=False))
        if len(ads):
            return ads[0].ad

        
    @sync_to_async
    def working(self):
        profile = Profile.objects.get(user=self.user)
        return profile.working

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
        ad.person = self.name
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
