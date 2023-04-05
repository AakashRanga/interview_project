import requests
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os



def signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]

        user_register(name=name,email=email,password=password).save()
        messages.success(request, 'Sucessfully Signed Up.')
    else:
        messages.success(request, 'Something Went Wrong.')

    return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp = user_register.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['dashboard'] = emp.email
            return redirect('/home/')

        except:
            messages.success(request, 'Invalid Email And Password')
            return redirect('/')

    return render(request,'signup.html')

def logout(request):
    if 'dashboard' in request.session:
        request.session.pop('dashboard',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/')

def home(request):
    users = user_register.objects.count()
    sers = user_register.objects.all()

    user = request.session.get('dashboard')
    n = user_register.objects.get(email=user)

    data = {"username": "hari",
            "card2": {"title": "Lorem Ipsum",
                      "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."},
            "card3": {
                    "table_headers": ["s.No", "Name", "City"],
                    "data": [
                        ["1", "Hari", "Chennai"],
                        ["2", "Aakash", "Thanjavur"],
                        ["3", "Kathir", "Madurai"],
                        ["4", "Praveen", "Coimbatore"],
                        ["5", "Deepan", "Trichy"]
                    ]},
            "card4": {"users": users}
            }

    city = "Chennai"
    api_key = "5bcdc9824051fa3994ba65b16ecc4ca7"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    d = response.json()
    temperature = d["main"]["temp"]

    name = [user.name for user in sers]
    ids = [user.id for user in sers]
    plt.plot(ids, name)
    plt.xlabel('User ID')
    plt.ylabel('name')
    plt.title('User name')
    filename = os.path.join('userportal', 'static', 'image_slider', 'images')
    plt.savefig(filename)

    return render(request,'home.html',{'data':data,'n':n,'temperature':temperature})




