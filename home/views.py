from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile, FAQ
from product.models import Product, Category, Images, Comment


def index(request):
    setting=Setting.objects.get(pk=1)
    sliderdata=Product.objects.all()[:4]
    category=Category.objects.all()
    dayproducts=Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]

    context={'setting':setting, 'category':category,'page':'home','sliderdata':sliderdata,'dayproducts':dayproducts,'lastproducts':lastproducts,'randomproducts':randomproducts}
    return render(request,'index.html',context)


def hakkimizda(request):
    category = Category.objects.all()
    setting=Setting.objects.get(pk=1)
    context={'setting':setting, 'page':'hakkimizda', 'category':category}
    return render(request,'hakkimizda.html',context)


def referanslar(request):
    category = Category.objects.all()
    setting=Setting.objects.get(pk=1)
    context={'setting':setting, 'page':'referanslar', 'category':category}
    return render(request,'referanslarimiz.html',context)

def iletisim(request):
    if request.method=="POST":
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz")
            return HttpResponseRedirect('/iletisim')

    category = Category.objects.all()
    setting=Setting.objects.get(pk=1)
    form=ContactFormu
    context={'setting':setting, 'form':form, 'category':category}
    return render(request,'iletisim.html',context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categoryname = Category.objects.get(id=id)
    categorydata = Category.objects.filter(parent_id=id)
    productss=Product.objects.filter(category_id=id,status=True)
    products=[]
    for cat in categorydata:
        products += Product.objects.filter(category_id=cat.id,status=True)
    context={'products':products, 'category':category, 'categorydata':categorydata,'productss':productss,'categoryname':categoryname}
    return render(request,'products.html',context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    product = Product.objects.get(pk=id)
    images=Images.objects.filter(product_id=id)
    comments=Comment.objects.filter(product_id=id,status='True')
    context = {'category': category,'setting':setting,'product':product,'images':images,'comments':comments}
    return render(request,'product_detail.html',context,)

def product_search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            category=Category.objects.all()
            query=form.cleaned_data['query']
            products=Product.objects.filter(title__icontains=query)
            context = {'category': category, 'products': products,}
            return  render(request,'product_search.html',context)

    return  HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Lütfen Kullanıcı Adınız Veya Şifrenizi Kontrol Ediniz.")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,'setting':setting}
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #create data in profile table for user
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/defaulticon.png"
            data.save()
            return HttpResponseRedirect('/')

    form=SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category, 'setting': setting, 'form': form,}
    return render(request, 'signup.html', context)

def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'category': category,
        'setting': setting,
        'faq': faq,
    }
    return render(request, 'faq.html', context)