from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from MainParser.models import Ad, Profile, User
from django.http import JsonResponse

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
    ads = list(Ad.objects.order_by('-date'))
    ads = ads[:min(300, len(ads))]
    for ad in ads:
        ad.date = ad.date.strftime("%d-%m-%Y %H:%M:%S")
    context = {'ads': ads}
    return render(request, 'MainParser/Index.html', context=context)


def get_table(request):
    ads = list(Ad.objects.order_by('-date'))
    ads = ads[:min(300, len(ads))]
    ans = []
    for ad in ads:
        micro_ans = {'date': ad.date.strftime("%d-%m-%Y %H:%M:%S"),
                     'site': ad.site, 'title': ad.title,
                     'address': ad.address, 'price': ad.price,
                     'phone': ad.phone, 'city': ad.city,
                     'person': ad.person, 'link': ad.link,
                     'done': ad.done}
        ans.append(micro_ans)

    return JsonResponse({'respond': ans})


def logout(request):
    if request.user.is_authenticated:
        logoutuser(request)

    return redirect('main-login')


def valid_phone(phone: str):
    phone = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if phone[0] == '8':
        phone = '7' + phone[1:]
    return phone
