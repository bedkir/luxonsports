from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.template.context_processors import csrf
from .models import AuthUser, Продукт, ShopCurrency
from django.db import models
from django.db.models import F
from django.contrib import messages
import requests
from django.db.utils import IntegrityError
import pytz
from bs4 import BeautifulSoup as bs
import datetime
from django.contrib.auth.hashers import check_password, make_password
products = Продукт.objects.all()
accounts = AuthUser.objects.all()
timezone = pytz.timezone('Europe/Kiev')

def register(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        email = request.POST.get('email', '')
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        d = datetime.datetime.now()
        upper_case = 0
        lower_case = 0
        number = 0

        for i in password2:
            if i.isupper():
                upper_case += 1
            elif i.islower():
                lower_case += 1
            elif i.isdigit():
                number += 1
        if password1 == password2:
            if len(password2) >= 8:
                if number > 0 and upper_case > 0:
                            try:
                                user = AuthUser(username=username, password=make_password(password2, salt=None, hasher='default'), email=email, last_login=d, date_joined=d, is_superuser=0, is_staff=0, is_active=1)
                                user.save()
                                usery = auth.authenticate(username=username, password=password2)
                                auth.login(request, usery)
                                return redirect("/accounts/"+str(user.id))
                            except IntegrityError:
                                error_code = 'Пользователь с таким именем уже существует'
                                return render(request, "accounts/auth/register.html", {'error_code': error_code,})
                else:
                    error_code = 'Пароль должен содержать по крайней мере одну заглавную букву и одну цифру'
                    return render(request, "accounts/auth/register.html", {'error_code': error_code,})
            else:
                error_code = 'Ваш пароль слишком короткий'
                return render(request, "accounts/auth/register.html", {'error_code': error_code,})
        else:
            error_code = 'Пароли не совпадают'
            return render(request, "accounts/auth/register.html", {'error_code': error_code,})

    else:
        return render(request, "accounts/auth/register.html", args)
    '''if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/auth/register.html', {'form': form})'''
    
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args["login_error"] = "Wrong username or password!"
            return render(request, "accounts/auth/failed.html", args)

    else:
        return render(request, "accounts/auth/login.html", args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def userProfilePage(request, uid):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    context = {
        'auth_status': auth_status,
        "userId": str(request.user.id),
        "account": str(uid),
        'currentUser': AuthUser.objects.get(id=request.user.id)
    }
    template = "accounts/profilePage/profilePage.html"
    return render(request, template, context)


def userOrders(request, uid):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    class ShopOrdery(models.Model):
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=10000, blank=True, null=True)
        #order = models.ManyToManyField(Продукт)
        сумма_заказа = models.FloatField(blank=True, null=True)
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'
    a = ShopOrdery.objects.all()
    orders=[]
    for i in a:
        if str(i.user_id) == str(request.user.id):
            orders.append(i)
    context = {
        'auth_status': auth_status,
        "userId": str(request.user.id),
        "account": str(uid),
        "orders": orders,
    }
    template = "accounts/profilePage/orders.html"
    return render(request, template, context)

now = datetime.datetime.now()

def userCart(request, uid):
    template = "accounts/profilePage/cart.html"
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=45)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

    # ADD TO CART
    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_cart"

    summary = 0
    # DELETE FROM CART
    if request.POST:
        itemToDelete = request.POST.get("delete", "")
        addOneMore = request.POST.get("plus", "")
        removeOneMore = request.POST.get("minus", "")
        makeorder = request.POST.get('makeorder', '')
        if addOneMore:
            item = request.POST.get("item_plus", "")
            carts = ShopCarty.objects.get(item=item)
            carts.amount += 1
            carts.save()
            return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif removeOneMore:
            item = request.POST.get("item_minus", "")
            carts = ShopCarty.objects.get(item=item)
            carts.amount -= 1
            if carts.amount == 0:
                messages.error(request, "Количество товара не может быть меньше 1")
                return redirect("/accounts/" + str(request.user.id) + "/cart")
            else:
                carts.save()
                return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif itemToDelete:
            ShopCarty.objects.filter(item=itemToDelete).delete()
            return redirect("/accounts/" + str(request.user.id) + "/cart")
        elif makeorder:
            '''b = 0
            userAccount = AuthUser.objects.get(id=request.user.id)
            userCarts = ShopCarty.objects.all()
            currencys = ShopCurrency.objects.all()
            needed = currencys[len(currencys) - 1]
            currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
            a = []
            bob = []
            d = datetime.datetime.now()
            for i in userCarts:
                if str(i.user_id) == str(request.user.id):
                    b += 1
            if b == 0:
                return HttpResponse('your cart is empty!')#Have to add speial error message for this situation
            else:
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        a.append(i.name)
                for i in a:
                    local = ShopCarty.objects.get(name=i)
                    if local.currency == 'UAH':
                        bob.append(round(float(local.price) * float(local.amount), 2))
                    else:
                        bob.append(round(float(local.price) * currency * float(local.amount), 2))
                intbob = [float(elem) for elem in bob]
                order = ShopOrdery(user_id=request.user.id, имя=userAccount.first_name, фамилия=userAccount.last_name, почта=userAccount.email, сумма_заказа=sum(intbob), дата_заказа=d, телефон=userAccount.phone_number, адрес_заказа=userAccount.address, валюта_заказа='UAH', заказ=a, статус_оплаты='np', статус_заказа='nd')
                order.save()
                for i in userCarts:
                    if str(i.user_id) == str(request.user.id):
                        i.delete()'''
            return redirect('/accounts/' + str(request.user.id) + '/make-order')
    else:
        currencys = ShopCurrency.objects.all()
        needed = currencys[len(currencys) - 1]
        currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
        carts = ShopCarty.objects.all()
        cartItems = carts[0 : len(carts):]
        a = []
        b = []
        c = []
        for cartItem in cartItems:
            if str(cartItem.user_id) == str(request.user.id):
                a.append(cartItem.name)
                b.append(cartItem.amount)
                c.append(cartItem)
        for i in carts:
            if int(i.user_id) == request.user.id:
                if i.currency == 'UAH':
                    local_sum = int(i.price) * int(i.amount)
                elif i.currency == 'USD':
                    local_sum = round(int(i.price) * int(i.amount) * currency, 2)
                    small_sum = round(int(i.price) * currency, 2)
                summary += local_sum
        try:
            context = {
                'auth_status': auth_status,
                "items": c,
                "amounts": b,
                "userId": str(request.user.id),
                "account": str(uid),
                "sum": summary,
                'currency': currency,
                'small_sum': small_sum,
            }
        except UnboundLocalError:
            context = {
            'auth_status': auth_status,
            "items": cartItems,
            "amounts": b,
            "userId": str(request.user.id),
            "account": str(uid),
            "sum": summary,
            'currency': currency,
        }
        context.update(csrf(request))
        return render(request, template, context)


def userFavourites(request, uid):
    template = "accounts/profilePage/favourites.html"
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    else:
        auth_status = 'success'
    class ShopFavourite(models.Model):
        favourite_id = models.AutoField(primary_key=True)
        user_id = models.CharField(max_length=45)
        favourite_item = models.CharField(max_length=45, blank=True, null=True)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=45, blank=True, null=True)
        currency = models.CharField(max_length=45, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_favourite"

    if request.POST:
        itemToDelete = request.POST.get("delete", "")
        if itemToDelete:
            ShopFavourite.objects.filter(favourite_item=itemToDelete).delete()
        return redirect("/accounts/" + str(request.user.id) + "/favourites")
    else:
        favourites = ShopFavourite.objects.all()
        a = []
        for i in favourites:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
        context = {
            'auth_status': auth_status,
            "favourites": a,
            'userId': str(request.user.id),
            'account': str(uid),
        }
        context.update(csrf(request))
        return render(request, template, context)


def editProfilePage(request, uid):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    new_name = request.POST.get('new_name', '')
    new_last_name = request.POST.get('new_last_name', '')
    new_email = request.POST.get('new_email', '')
    new_phonenumber = request.POST.get('new_phonenumber', '')
    new_city = request.POST.get('new_city', '')
    new_street = request.POST.get('new_street', '')
    new_house = request.POST.get('new_house', '')
    password = request.POST.get('password', '')
    if request.POST:
        userProfile = AuthUser.objects.get(id=uid)
        userProfile.first_name = new_name
        userProfile.last_name = new_last_name
        userProfile.email = new_email
        userProfile.phone_number = new_phonenumber
        userProfile.city = new_city
        userProfile.street = new_street
        userProfile.house = new_house
        if check_password(password=password, encoded=userProfile.password) == True:
            userProfile.save()
            return redirect('/accounts/'+ str(uid))
        else:
            template = 'accounts/editProfile/edit.html'
            context = {
                'error_message': 'Неправильный пароль',
            }
            context.update(csrf(request))
            return render(request, template, context)  
    else:
        userProfile = AuthUser.objects.get(id=uid)
        template = 'accounts/editProfile/edit.html'
        context = {
            'userProfile': userProfile,
        }
        context.update(csrf(request))
        return render(request, template, context)

def editPasswordPage(request, uid):
    if request.user.is_authenticated == False:
        return HttpResponse('404')
    old_pwd = request.POST.get('old_pwd', '')
    new_pwd = request.POST.get('new_pwd', '')
    repeat_new_pwd = request.POST.get('repeat_new_pwd', '')
    userProfile = AuthUser.objects.get(id=request.user.id)
    template = 'accounts/editProfile/editPassword.html'
    if request.POST:
        if check_password(password=old_pwd , encoded=userProfile.password) == True:
            if new_pwd == repeat_new_pwd:
                username = userProfile.username
                hashed_pwd = make_password(repeat_new_pwd, salt=None, hasher='default')
                userProfile.password = hashed_pwd
                userProfile.save()
                user = auth.authenticate(username=username, password=repeat_new_pwd)
                auth.login(request, user)
                return redirect('/accounts/'+ str(uid))
            else:
                error_code = 'Новые пароли не совпадают. Повторите попытку'
                context = {
                'error_message': error_code,
            }
            return render(request, template, context)
        else:
            error_code = 'Неверный старый пароль. Попробуйте снова'
            context = {
                'error_message': error_code,
            }
            return render(request, template, context)
    else:
        template = 'accounts/editProfile/editPassword.html'
        return render(request, template)

def makeOrder(request, uid):
    if request.user.is_authenticated == False:
        auth_status = 'failed'
        return HttpResponse('404')
    else: 
        auth_status = 'success'
    class ShopOrdery(models.Model):
        user_id = models.CharField(max_length=10000, blank=True, null=True)
        фамилия = models.CharField(max_length=45)
        имя = models.CharField(max_length=45)
        отчество = models.CharField(max_length=45, blank=True, null=True)
        телефон = models.CharField(max_length=45, blank=True, null=True)
        почта = models.CharField(max_length=60)
        заказ = models.CharField(max_length=45)
        сумма_заказа = models.CharField(max_length=45, blank=True, null=True)     
        валюта_заказа = models.CharField(max_length=45, blank=True, null=True)    
        статус_оплаты = models.CharField(max_length=45)
        статус_заказа = models.CharField(max_length=45)
        дата_заказа = models.DateTimeField(blank=True, null=True)
        user_id = models.CharField(max_length=1000, blank=True, null=True)
        city = models.CharField(max_length=50, blank=True, null=True)
        street = models.CharField(max_length=50, blank=True, null=True)
        house = models.CharField(max_length=50, blank=True, null=True)
        payment_type = models.CharField(max_length=20, blank=True, null=True)
        delivery_type = models.CharField(max_length=20, blank=True, null=True)
        nova_pochta = models.CharField(max_length=1000, blank=True, null=True)
        ukr_pochta = models.CharField(max_length=1000, blank=True, null=True)

        class Meta:
            managed = False
            db_table = 'shop_order'

    class ShopCarty(models.Model):
        user_id = models.CharField(max_length=45)
        item = models.CharField(max_length=45, blank=True, null=True)
        cart_id = models.AutoField(primary_key=True)
        amount = models.IntegerField(blank=True, null=True, default=1)
        name = models.CharField(max_length=300, blank=True, null=True)
        price = models.CharField(max_length=30, blank=True, null=True)
        currency = models.CharField(max_length=30, blank=True, null=True)

        class Meta:
            managed = False
            db_table = "shop_cart"

    if request.user.is_anonymous:
        anon = True
    template = 'accounts/profilePage/makingOrder.html'
    try:
        user = AuthUser.objects.get(id=str(request.user.id))
    except ValueError:
        user = AuthUser.objects.get(id=str(1))
    cart = ShopCarty.objects.all()
    a = []
    price = 0
    if request.POST:
        go = request.POST.get('go', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        orderFromHtml = request.POST.get('order', '')
        priceFromHtml = request.POST.get('price', '')
        typeOfDelivery = request.POST.get('typeOfDelivery', '')
        typeOfPayment = request.POST.get('typeOfPayment', '')
        city = request.POST.get('city', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        ukr_pochta = request.POST.get('ukr_pochta', '')
        nova_pochta = request.POST.get('nova_pochta', '')
        normalPrice = max(float(i) for i in priceFromHtml.replace(',','.').split())
        if orderFromHtml == None:
            return redirect('/')
        if go:
            d = datetime.datetime.now()
            userCarts = ShopCarty.objects.all()
            currencys = ShopCurrency.objects.all()
            a={}
            '''for i in orderFromHtml:
                a.update({'name': 
                })'''
            needed = currencys[len(currencys) - 1]
            currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
            order = ShopOrdery(user_id=request.user.id, имя=first_name, фамилия=last_name, почта=email, сумма_заказа=normalPrice, дата_заказа=d, телефон=phone_number, city=city, street=street, house=house, валюта_заказа='UAH', заказ=orderFromHtml, статус_оплаты='np', статус_заказа='nd', delivery_type=typeOfDelivery, payment_type=typeOfPayment, nova_pochta=nova_pochta, ukr_pochta=ukr_pochta)
            order.save()
            for i in userCarts:
                if str(i.user_id) == str(request.user.id):
                    i.delete()
            return redirect('/')
    else:
        for i in cart:
            if str(i.user_id) == str(request.user.id):
                a.append(i)
                if i.currency == 'UAH':
                    price += int(i.price) * int(i.amount)
                else:
                    currencys = ShopCurrency.objects.all()
                    needed = currencys[len(currencys) - 1]
                    currency = max(float(i) for i in needed.usd_to_uah.replace(',','.').split())
                    price += int(i.price) * currency * int(i.amount)
        '''b = max(a)
        newUser = ShopCarty.objects.get(cart_id=b)'''
        context = {
            'auth_status': auth_status,
            'user': user,
            'userCart': a,
            'price': price,
            'userId': str(request.user.id),
            'account': str(uid),
        }
        return render(request, template, context)