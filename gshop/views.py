from django.shortcuts import render,redirect,HttpResponse
from app.models import Category,Product,Contact_us,Order
from django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.models import User
# add to cart


from django.contrib.auth.decorators import login_required
from cart.cart import Cart





def Master(request):

    return render(request,'master.html')

def index(request):
    category =  Category.objects.all()
   
    catergoryID = request.GET.get('category')
    if catergoryID:
        product = Product.objects.filter(sub_category=catergoryID)
    else:
            product = Product.objects.all()
   

    context = {
        'category':category,
        'product':product,
    }
    return render(request, 'index.html',context)    


#sigup page

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context = {
        'form':form,
    }
    return render(request,'registration/signup.html',context)


def cart_detail(request):
    
     return render(request,'cart_detail.html')

    #  add to cart

 

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart/cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart/cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart/cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart/cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')



# contact page


def Contact_Page(request):
    if request.method =='POST':
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request, 'contact.html')

def entery(request):
    if request.method=="POST":
        
        name=request.POST.get('name')
        price=request.POST.get('price')
        # desc=request.POST.get('desc')
        image=request.FILES.get('image')

       
        contactme=Product(name=name,price=price,image=image)
        contactme.save()       

    return render(request,'product.html')

    # checkout page


def Checkout(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        print(cart)


      
        print(address,phone,pincode,cart,user)
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b
            order = Order(
                 user = user,
                 product = cart[i]['name'],
                 price = cart[i]['price'],
                 quantity = cart[i]['quantity'],
                 image = cart[i]['image'],
                 address = address,
                 phone = phone,
                 pincode = pincode,
                 total = total,
             )
            order.save()
        request.session['cart'] = {}   
        return redirect('index')
    return HttpResponse("This page is check out")  



def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user = user)
    context = {
        'order':order,
    }
    return render(request,'order.html',context)          

def Product_page(request):
    category =  Category.objects.all()
   
    catergoryID = request.GET.get('category')
    if catergoryID:
        product = Product.objects.filter(sub_category=catergoryID)
    else:
            product = Product.objects.all()
   

    context = {
        'category':category,
        'product':product,
    }
    return render(request,'product.html',context)



def Search(request):
    query = request.GET['query']
    # filter(name__icontains = querry)

    product = Product.objects.filter(name__icontains = query)
    context = {
        'product':product,
    #     'query': query,
    }
    return render(request, 'search.html',context)    



def Product_Detail(request,id):
    product = Product.objects.filter(id = id).first()
    context = {
        'product':product,
    }

    return render(request,'Product_detail.html',context)




#     <a href="{% url 'cart_add' product.id %}">Add To Cart</a>
# <a href="{% url 'cart_clear' %}">Clear Cart</a>
# <a href="{% url 'item_increment' value.product_id %}">Increament</a>
# <a href="{% url 'item_decrement' value.product_id %}">Decrement</a>
# <a href="{% url 'item_clear' key %}">Item clear</a>


# Load Cart Tag
# {% load cart_tag %}

# {% for key,value in request.session.cart.items %}

#    {{value.name}} 
#    {{value.price}} 
#    {{value.quantity}} 
#    {{value.image}} 
#    Total 
#    {{ value.price|multiply:value.quantity }}
 
# {% endfor %}




#search code

# def Search(request):
#     # Get the query string from the search form
#     query = request.GET.get('query')

#     # Filter the products based on the query
#     product = Product.objects.filter(name__icontains = query)

#     # Create a dictionary with the search results
#     context = {
#         'product': product,
#         'query': query,
#     }

#     # Render the search results template with the context dictionary
#     return render(request, 'search.html', context)