from django.shortcuts import render,redirect
from django.http import JsonResponse
from FoodApp import forms
from FoodApp.models import Food,UserProfile,Cart,OrderSummery1,Orders
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group,User
import datetime
from django.contrib.auth.decorators import permission_required,login_required
import smtplib as s
ob=s.SMTP('smtp.gmail.com',587)
ob.starttls()
print(ob)
ob.login('vaishnavnair699@gmail.com','7757904263')


def index(request):
    return render(request,"foodapp/index.html")
def addFood(request):
    form=forms.FoodForm()
    print("////",form)
    if request.method=='POST':
        form=forms.FoodForm(request.POST,request.FILES)
        if form.is_valid():
            print("/////",form)
            form.save(commit=True)
            
    return render(request,'Foodapp/addfood.html',{'form':form})
def menu(request):
    food=Food.objects.all()
    return render(request,'FoodApp/menu.html',{'food':food})
#@permission_required()

def updateFood(request,id):
    food=Food.objects.get(id=id)
    # form=forms.Foodform(food)
  
    if request.method=='POST':
        form=forms.FoodForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            print("/////",form)
            form.save(commit=True)
            return redirect("/menu")
            
    return render(request,'FoodApp/updatefood.html',{'food':food})
def deleteFood(request,id):
    food=Food.objects.get(id=id)
    food.delete()
    return render(request,'foodapp/updatefood.html',{'food':food})
def signup(request):
    form=forms.SignUpForm(request.POST)
    profile=forms.Profileform(request.POST)
    role=request.POST.get('Role')
    print('role........',role)
    email=request.POST['email']
    if request.method=='POST':
        form=forms.SignUpForm(request.POST)
        profile=forms.Profileform(request.POST)
        role=request.POST['Role']
        email=request.POST['email']
        print(email,'............')
        sub='ThankYou For Registration'
        body='Sucesfully registered'
        msg='Subject:{}\n\n{}'.format(sub,body)



        ob.sendmail("vaishnavnair699@gmail.com","vaishnavnair787@gmail.com",msg)
        ob.quit()





        if form.is_valid() and profile.is_valid():
            user=forms.save(commit=True)
            print(user,"user")
            profile=profile.save(commit=False)
            profile.user=user

            profile.save()

        user.set_password(user.password)
        user.save()
    if role=="customer":
            cust=Group.objects.get(name="customer")
            user.group.add(cust)
    elif role=="admin":
            admin=Group.objects.get(name="admin")
            user.groups.add(admin)
        
    return render(request,'foodapp/signup.html',{'form':forms,'profile':forms})


def updateProfile(request):
    curntUser= request.user

    userdata=UserProfile.objects.get(user=curntUser)
    userdata1=User.objects.get(username=curntUser)

    if request.method=='POST':
        profile=forms.Profileform(request.POST,instance=userdata)
        form=forms.Signupform(request.POST, instance=userdata.user)

        if form.is_valid() and profile.is_valid():
            user=form.save(commit=True)
            profile=profile.save(commit=False)
            profile.user=user
            profile.save()
            form.save()

            return redirect('/menu')
    return render(request,'foodapp/index.html')

def loginUser(request):
    form=AuthenticationForm()
    if request.method=="POST":
        uname=request.POST['username']
        pwd=request.POST.get('password')
        user=authenticate(username=uname,password=pwd)
        if user is not None:
            login(request,user)
            return render(request,"foodapp/index.html",{'success':'welcome'})
        else:
            return render(request,"foodapp/index.html",{'failure':'invalid','form':form})
        
        
        form=AuthenticationForm(request.POST)
       
        
    return render(request,'foodapp/login.html')
    """if request.method=="POST":
        user=authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
        print(user)
        if user is not None:
            login(request,user)
            print(request.session)
            return redirect('/menu')
        else:
            return render(request,'foodapp/login.html',{'failure':'Invalid Username or Password'})"""
        
def logoutUser(request):
    logout(request)

    return render(request,'foodapp/index.html')

@login_required()
def userProfile(request):
    currentuser=request.user
    print(currentuser)
    data=User.objects.get(username=currentuser)
    data1=UserProfile.objects.get(user=currentuser)
    qset=Group.objects.filter(user=currentuser)
    for q in qset:
        global role
        role=q.name
        print(role)

    return render(request,'foodapp/profile.html',{'data':data,'data1':data1,'role':role})


def addCart(request):
    user=request.user
    fid=request.GET['foodid']
    food=Food.objects.get(id=fid)
    price=request.GET['price']
    print(user,fid.price)
    Cart(currentuser=user,fid=food,total=price).save()
    return render(request,'foodapp/index.html')
def showCart(request):
    user = request.user
    data = Cart.objects.filter(currentuser=user)

    return render(request, "foodapp/cart.html", {'cart': data})


def updateCart(request):
    quantity = request.POST.get('q')
    price = request.POST.get('p')
    cartId = request.POST.get('id')
    Cart.objects.filter(id=cartId).update(itemquantity=quantity, total=price)
    return JsonResponse({'status': 'true'})


def deleteCart(request):
    cartId = Cart.objects.get(id=id)
    cartId.delete()
    return redirect('/cart')

def placeOrder(request):
    amount = request.POST.get('totalbill')
    user = request.user
    print(amount)
    ob = OrderSummery1.objects.create(totalamount=amount, customer=user)
    oid = ob.id
    ob.save()
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # to compare current date in order summery table
    try:

        ordobj = OrderSummery1.objects.get(customer=user,  id=oid)  # will return object of current date and current user
        cart = list(Cart.objects.filter(currentuser=user))  # retrive all cart details of current user
        print(cart)
        for c in cart:
            Orders(order=ordobj, food=c.fid, total=c.total, foodQuant=c.itemquantity).save()
            c.delete()

            return render(request, 'foodapp/index.html', {'success': user + 'order has been placed'})
    except Exception as e:


        return render(request, 'foodapp/index.html', {'success': str(user) + 'order has been placed'})

from django.db import connection, transaction
cursor = connection.cursor()

def showOrders(request):
    user=request.user
    osdata=OrderSummery1.objects.filter(customer=request.user) #retriving all records of loggdin user frrom ordersummery table
    print(osdata,'ordersumry data')
    data=[]
    for i in osdata:
        ordersdata1=Orders.objects.filter(order=i).order_by('id')#retriving all details of food item from orders table
        #on basis of unique ordersummery object e.g=orderid 1 has 3 food product
        for ob in ordersdata1:
            data.append(ob) #maintaining all orders object in single list

    print(data)

    # sql='select total from orders as os left join ordersummery as o on os.ordersobj_id=os.id'
    return render(request,'foodapp/myorders.html',{'orders':data})

def allOrders(request):
    user=request.user
    isadmin= request.user.groups.filter(name='admin').exists()
    if user.groups.filter(name='admin').exists():
        data=OrderSummery1.objects.all().order_by('id')
        return render(request,'foodapp/allorder.html',{'orders':data})
    else:
        return render(request,'foodapp/allorder.html',{'msg':'you are not authorized'+str(user),'isadmin':isadmin})


    9