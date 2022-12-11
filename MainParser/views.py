from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from MainParser.models import Ad, Profile, User, TargetAd
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta, datetime
import pytz

# Registration
from .forms import RegisrationForm

MONTH_ROD = [
    'Января',
    'Фебраля',
    'Марта',
    'Апреля',
    'Мая',
    'Июня',
    'Июля',
    'Августа',
    'Сентября',
    'Откября',
    'Ноября',
    'Декабря',
]

MONTH = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь'
]


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_users(ads):
    info = {'users': {}, 'total_closed': 0, 'average_calls': 0}

    for ad in ads:
        if ad.person is None:
            continue
        user_name = ad.person.profile.name
        if ad.person.profile.name not in info['users']:
            info['users'][user_name] = {'total': 0, 'first': 0, 'second': 0, 'done': 0}

        info['users'][user_name]['total'] += 1
        if ad.is_first is True:
            info['users'][user_name]['first'] += 1
        elif ad.is_first is False:
            info['users'][user_name]['second'] += 1

        if ad.frontDone is True:
            info['users'][user_name]['done'] += 1

    total_closed = sum(info['done'] for name, info in info['users'].items())
    total_calls = sum(info['total'] for name, info in info['users'].items())
    total_calls_first = sum(info['first'] for name, info in info['users'].items())

    if total_calls > 0:
        average_calls = round((total_calls_first / total_calls) * 100, 2)
    else:
        average_calls = 0

    info['total_closed'] = total_closed
    info['average_calls'] = average_calls

    return info


def statistic(request):
    UTC = pytz.UTC

    date = datetime.now()
    date = f"{date.day} {MONTH_ROD[date.month - 1]}"
    current_date = datetime.now()

    ads = Ad.objects.all()

    current_day = datetime(year=current_date.year, month=current_date.month, day=current_date.day) - timedelta(hours=7)
    current_month = datetime(year=current_date.year, month=current_date.month, day=1) - timedelta(hours=7)

    current_day = UTC.localize(current_day)
    current_month = UTC.localize(current_month)

    month_ads = list(filter(lambda x: x.date >= current_month, ads))
    day_ads = list(filter(lambda x: x.date >= current_day, month_ads))

    avito_day = list(filter(lambda x: x.site == 'av', day_ads))
    avito_month = list(filter(lambda x: x.site == 'av', month_ads))

    cian_day = list(filter(lambda x: x.site == 'ci', day_ads))
    cian_month = list(filter(lambda x: x.site == 'ci', month_ads))

    # Avito day
    avito_day_info = calculate_users(avito_day)
    avito_month_info = calculate_users(avito_month)
    cian_day_info = calculate_users(cian_day)
    cian_month_info = calculate_users(cian_month)

    return render(request, 'MainParser/Statistic.html', context={'date': date,
                                                                 'avito_day_info': avito_day_info,
                                                                 'avito_month_info': avito_month_info,
                                                                 'cian_day_info': cian_day_info,
                                                                 'cian_month_info': cian_month_info,
                                                                 'month': MONTH[current_date.month - 1]
                                                                 })


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
            return redirect('main-index')
        else:
            return render(request, 'MainParser/Login.html', {'error': True})
    return render(request, 'MainParser/Login.html')


def register(request):
    if request.user.is_authenticated and request.method == 'GET' and request.user.username == '79154037045':
        form = RegisrationForm()
        return render(request, 'MainParser/Register.html', {'form': form})

    elif request.user.is_authenticated and request.method == 'POST' and request.user.username == '79154037045':
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

            return redirect('main-index')

    if request.user.is_authenticated:
        return redirect('main-index')

    return redirect('main-index')


def index(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['work_status'] = profile.working
        context['name'] = profile.name

    return render(request, 'MainParser/Index.html', context=context)


def get_table(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

    utc = pytz.UTC
    now = utc.localize(datetime.now())

    need_len = int(request.GET['length'])
    ads = list(Ad.objects.filter(~Q(phone='+74954760059')).order_by('-id')[:need_len])

    ans = []
    for ad in ads:
        color = ''
        if ad.noCall or ad.date + timedelta(minutes=2, hours=3) < now or ad.clearColor:
            color = 'gray'
        elif ad.site == 'av':
            color = 'orange'
        elif ad.site == 'ci':
            color = 'blue'

        if ad.date_done is None:
            time_diff = ""
        else:
            time_diff = ad.date_done - ad.date
            if time_diff.seconds > 10:
                time_diff = f">10s"
            else:
                time_diff = f"{time_diff.seconds}.{str(time_diff.microseconds)[:2]}s"

        micro_ans = {'date': (ad.date + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M:%S"),
                     'site': ad.site, 'title': ad.title,
                     'address': ad.address, 'price': ad.price,
                     'phone': ad.phone, 'city': ad.city,
                     'person': ad.person.profile.name if ad.person else '', 'link': ad.full_link,
                     'done': ad.done, 'id': ad.id,
                     'color': color, 'frontDone': ad.frontDone,
                     'noCall': ad.noCall, 'focused': ad.focused,
                     'views': ad.views, 'clearColor': ad.clearColor,
                     'taken_time': time_diff, 'done_first': False if ad.is_first is None else True,
                     'is_first_status': ad.is_first if request.user.username == '79154037045' else None}

        ans.append(micro_ans)

    return JsonResponse({'respond': ans})


def clear_ad(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

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
    ad.clearColor = not ad.clearColor
    ad.save()

    return JsonResponse({'status': 'ok'})


def no_call(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

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
    new_status = not ad.noCall
    all_ads = Ad.objects.filter(phone=ad.phone)
    for my_ad in all_ads:
        my_ad.noCall = new_status
        my_ad.save()

    return JsonResponse({'status': 'ok'})


def is_first(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

    params = dict(request.GET)
    ad_ids = params['id']

    status = params['status'][0]
    if status == 'true':
        status = True
    else:
        status = False

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
    if request.user != ad.person:
        return JsonResponse({'status': 'error', 'message': 'not allowed'})

    if ad.is_first is not None:
        return JsonResponse({'status': 'error', 'message': 'not allowed'})

    ad.is_first = status
    ad.save()

    return JsonResponse({'status': 'ok'})


def closed(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

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


def focus_ad(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

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
    ad.focused = not ad.focused
    ad.save()

    return JsonResponse({'status': 'ok'})


def target_ad(request):
    if not request.user.is_authenticated:
        return JsonResponse({'respond': []})

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


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def addAd(request):
    try:
        ad = Ad(date=datetime.now(), **({k: v for k, v in request.POST.items()}))
        ad.save()
        return JsonResponse({'status': 'OK', 'id': str(ad.id)})
    except Exception as e:
        return JsonResponse({'status': 'ERROR', 'message': f'{e}'})


@csrf_exempt
def addViews(request):
    try:
        info = dict(request.POST.items())
        ad = Ad.objects.get(id=info['id'])
        ad.views = int(info['views'])
        ad.save()
        return JsonResponse({'status': 'OK'})
    except Exception as e:
        return JsonResponse({'status': 'ERROR', 'message': f'{e}'})
