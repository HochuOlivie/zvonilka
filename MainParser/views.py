from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginuser, logout as logoutuser
from MainParser.models import Ad, Profile, User

#Registration
from .forms import RegisrationForm



def login(request):
    if request.user.is_authenticated:
        pass
        #return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
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
        print(0)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            username = username.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if username[0] == '8':
                username = username[1:]

            if len(username) < 11:
                form.add_error('username', 'Такого номера не существует')
                print(1)
                return render(request, 'MainParser/Register.html', context={'form': form})

            print(2)
            raw_password = form.cleaned_data.get('password1')
            name = form.cleaned_data.get('name')
            print(3)
            print(username)
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Такой номер уже существует')
                return render(request, 'MainParser/Register.html', context={'form': form})

            print(4)
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
    ads = Ad.objects.order_by('-date')
    for ad in ads:
        ad.date = ad.date.strftime("%d-%m-%Y %H:%M:%S")
    context = {'ads': ads}
    return render(request, 'MainParser/Index.html', context=context)
