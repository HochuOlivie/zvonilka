from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from MainParser.models import Ad, Profile, User, TargetAd
from django.http import JsonResponse

from datetime import timedelta, datetime
import pytz

# Registration
from .forms import RegisrationForm


def login(request):
    if request.user.is_authenticated:
        pass
        # return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        username = valid_phone(username)

        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            loginuser(request, user)
            return redirect('main-register')
        else:
            return render(request, 'MainParser/Login.html', {'error': True})
    return render(request, 'MainParser/Login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('main-index')

    if request.method == 'POST':
        form = RegisrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            name = form.cleaned_data.get('name')

            username = valid_phone(username)

            if len(username) < 11:
                form.add_error('username', 'Такого номера не существует')
                return render(request, 'MainParser/Register.html', context={'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Такой номер уже существует')
                return render(request, 'MainParser/Register.html', context={'form': form})

            form.save()
            user = authenticate(username=username, password=raw_password)

            profile = Profile.objects.get(user=user)
            profile.name = name
            profile.save()

            if user is not None:
                loginuser(request, user)
                return redirect('main-index')
    else:
        form = RegisrationForm()
    return render(request, 'MainParser/Register.html', {'form': form})


def index(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['work_status'] = profile.working

    return render(request, 'MainParser/Index.html', context=context)


def get_table(request):
    utc = pytz.UTC
    now = utc.localize(datetime.now())
    ads = list(Ad.objects.order_by('-date'))
    ads = ads[:min(300, len(ads))]
    ans = []
    for ad in ads:
        color = ''
        if ad.noCall or ad.date + timedelta(minutes=2) < now:
            color = 'gray'
        elif ad.site == 'av':
            color = 'orange'
        elif ad.site == 'ci':
            color = 'blue'

        micro_ans = {'date': ad.date.strftime("%d-%m-%Y %H:%M:%S"),
                     'site': ad.site, 'title': ad.title,
                     'address': ad.address, 'price': ad.price,
                     'phone': ad.phone, 'city': ad.city,
                     'person': ad.person, 'link': ad.link,
                     'done': ad.done, 'id': ad.id,
                     'color': color, 'frontDone': ad.frontDone,
                     'noCall': ad.noCall}
        ans.append(micro_ans)

    return JsonResponse({'respond': ans})


def no_call(request):
    params = dict(request.GET)
    ad_ids = params['id']

    if len(ad_ids) == 0:
        return JsonResponse({'status': 'error', 'message': 'no ids in query'})

    ad_id = ad_ids[0]
    if not ad_id.isnumeric():
        return JsonResponse({'status': 'error', 'message': 'id is not a number'})
    ad_id = int(ad_id)

    ad = Ad.objects.filter(id=ad_id)

    if len(ad) == 0:
        return JsonResponse({'status': 'error', 'message': 'no such ides'})

    ad = ad[0]
    all_ads = Ad.objects.filter(phone=ad.phone)
    for my_ad in all_ads:
        my_ad.noCall = not my_ad.noCall
        my_ad.save()

    return JsonResponse({'status': 'ok'})


def closed(request):
    params = dict(request.GET)
    ad_ids = params['id']

    if len(ad_ids) == 0:
        return JsonResponse({'status': 'error', 'message': 'no ids in query'})

    ad_id = ad_ids[0]
    if not ad_id.isnumeric():
        return JsonResponse({'status': 'error', 'message': 'id is not a number'})
    ad_id = int(ad_id)

    ad = Ad.objects.filter(id=ad_id)

    if len(ad) == 0:
        return JsonResponse({'status': 'error', 'message': 'no such ides'})

    ad = ad[0]
    ad.frontDone = not ad.frontDone
    ad.save()

    return JsonResponse({'status': 'ok'})


def target_ad(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'login required'})

    params = dict(request.GET)
    ad_ids = params['id']

    if len(ad_ids) == 0:
        return JsonResponse({'status': 'error', 'message': 'no ids in query'})

    ad_id = ad_ids[0]
    if not ad_id.isnumeric():
        return JsonResponse({'status': 'error', 'message': 'id is not a number'})
    ad_id = int(ad_id)

    ad = Ad.objects.filter(id=ad_id)

    if len(ad) == 0:
        return JsonResponse({'status': 'error', 'message': 'no such ides'})

    ad = ad[0]
    TargetAd(user=request.user, ad=ad).save()

    return JsonResponse({'status': 'ok'})


def working_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'login require'})

    profile = Profile.objects.get(user=request.user)
    profile.working = not profile.working
    profile.save()

    return JsonResponse({'status': 'ok', 'work': profile.working})


def logout(request):
    if request.user.is_authenticated:
        logoutuser(request)

    return redirect('main-login')


def valid_phone(phone: str):
    phone = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if phone[0] == '8':
        phone = '7' + phone[1:]
    return phone
