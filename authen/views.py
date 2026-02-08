from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from base.models import CartModel
import re


# ---------------------------- Login ----------------------------
def login_(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pasw = request.POST.get('pasw')

        a = authenticate(username=uname, password=pasw)
        if a:
            login(request, a)
            return redirect('home')
        else:
            return render(request, 'login_.html', {'error': True})

    return render(request, 'login_.html', {'error': False, 'login_nav': True})


# ---------------------------- Password Validator ----------------------------
def valid_pasw(pasw):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return re.match(pattern, pasw)


# -------------------------- Register ----------------------------
def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        uname = request.POST.get('uname')
        pasw = request.POST.get('pasw')

        if User.objects.filter(username=uname).exists():
            return render(request, 'register.html', {'error': True})

        if not valid_pasw(pasw):
            return render(request, 'register.html', {'pasw': 'Password should be Combination'})

        a = User.objects.create(
            username=uname,
            first_name=fname,
            last_name=lname,
            email=email,
        )
        a.set_password(pasw)
        a.save()

        return redirect('login_')

    return render(request, 'register.html', {'login_nav': True})


# ------------------------------- Logout -----------------------------
@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')


# ----------------------------- Profile -------------------------------
@login_required(login_url='login_')
def profile(request):
    cartproductcount = CartModel.objects.filter(host=request.user).count()
    return render(request, 'profile.html', {
        'cartproductscount': cartproductcount,
        'profile_nav': True
    })


# ------------------------------ Forgot ----------------------
def forgot(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')

        try:
            a = User.objects.get(username=uname)
            request.session['fp_user'] = a.username
            return redirect('new_pasw')
        except User.DoesNotExist:
            return render(request, 'forgot.html', {'error': True})

    return render(request, 'forgot.html', {'login_nav': True})


# ----------------------------------- New Password --------------------------------
def new_pasw(request):
    username = request.session.get('fp_user')

    if username is None:
        return redirect('forgot')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('forgot')

    if request.method == 'POST':
        new_pasw = request.POST.get('new_pasw')
        confirm_pasw = request.POST.get('confirm_pasw')

        if new_pasw != confirm_pasw:
            return render(request, 'new_pasw.html', {
                'error': 'Passwords do not match'
            })

        if user.check_password(new_pasw):
            return render(request, 'new_pasw.html', {
                'error': 'New Password should not be similar to old password'
            })

        if not valid_pasw(new_pasw):
            return render(request, 'new_pasw.html', {
                'error': 'Password should be Combination'
            })

        user.set_password(new_pasw)
        user.save()

        del request.session['fp_user']
        return redirect('login_')

    return render(request, 'new_pasw.html', {'login_nav': True})


# ----------------------------------- Reset -----------------------------------------
@login_required(login_url='login_')
def reset(request):
    user = request.user

    if request.method == 'POST':

        # STEP 1 — check old password
        if 'old_pasw' in request.POST:
            old_pasw = request.POST.get('old_pasw')
            auth_user = authenticate(username=user.username, password=old_pasw)

            if auth_user:
                return render(request, 'reset.html', {'new_pasw': True})
            else:
                return render(request, 'reset.html', {'error': True})

        # STEP 2 — set new password
        if 'new_pasw' in request.POST:
            new_pasw = request.POST.get('new_pasw')

            if not valid_pasw(new_pasw):
                return render(request, 'reset.html', {
                    'pasw': 'Password should be Combination',
                    'new_pasw': True
                })

            user.set_password(new_pasw)
            user.save()
            return redirect('login_')

    return render(request, 'reset.html', {'profile_nav': True})


# ------------------------------------ Update --------------------------------------
@login_required(login_url='login_')
def update(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.email = request.POST.get('email')
        user.username = request.POST.get('uname')

        pasw = request.POST.get('pasw')
        if pasw:
            user.set_password(pasw)

        user.save()
        return redirect('profile')

    return render(request, 'update.html', {
        'user': user,
        'profile_nav': True
    })
