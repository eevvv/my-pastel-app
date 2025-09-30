# myapp/views.py
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from myproject import settings


def home(request):
    name = request.GET.get('name')
    message = request.GET.get('message')
    # Обработка формы "Контакт"
    if request.method == 'POST' and 'contact_form' in request.POST:
        email = request.POST.get('email')
        contact_message = request.POST.get('contact_message')
        if email and contact_message:
            messages.success(request, _("Thank you for your message!"))
        else:
            messages.error(request, _("Please fill all fields."))
    # Обработка формы "Заказ"
    elif request.method == 'POST' and 'order_form' in request.POST:
        order_name = request.POST.get('order_name')
        phone = request.POST.get('phone')
        product = request.POST.get('product')
        product_names = {
            'laptop': _('laptop'),
            'phone': _('smartphone'),
            'book': _('book'),
        }
        if order_name and phone and product:
            product_display = product_names.get(product, product)
            success_message = _("Your order for {product} has been received!").format(product=product_display)
            messages.success(request, success_message)
        else:
            messages.error(request, _("Please fill all fields."))
    # Изменение языка
    if 'lang' in request.GET:
        lang_code = request.GET['lang']
        if lang_code in [lang[0] for lang in settings.LANGUAGES]:
            request.session['language'] = lang_code
            query_string = request.META.get('QUERY_STRING', '')
            new_query = '&'.join([param for param in query_string.split('&') if not param.startswith('lang=')])
            redirect_url = '/' + ('?' + new_query if new_query else '')
            return HttpResponseRedirect(redirect_url)
    context = {
        'name': name,
        'message': message,
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, _("All fields are required."))
        elif password1 != password2:
            messages.error(request, _("Passwords do not match."))
        elif User.objects.filter(username=username).exists():
            messages.error(request, _("Username already taken."))
        else:
            user = User(username=username)
            user.password = make_password(password1)
            user.save()
            login(request, user)
            messages.success(request, _("Registration successful! You are now logged in."))
            return redirect('home')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, _("You have successfully logged in."))
                return redirect('home')
            else:
                messages.error(request, _("Invalid username or password."))
        except User.DoesNotExist:
            messages.error(request, _("Invalid username or password."))
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect('home')


@login_required
def protected_view(request):
    return render(request, 'protected.html')