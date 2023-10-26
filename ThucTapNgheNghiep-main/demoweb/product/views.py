from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Product,Review
from order.models import Order, Users, Order_detail,Contact
from .forms import Product_create_form, Category_create_form, Register_form,UserInformationForm,AddAvatar,UpdateUser,Add_review,ContactForm,Reset_form
from vi_address.models import City, District, Ward
from django.core.paginator import Paginator
from django.contrib import messages, sessions
from django.urls import reverse

from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# Create your views here.
def index(request):
    ds = Category.objects.all()
    return render(request, "product/index1.html", {"loaisp": ds})


def detail(request, id):
    lsp = Category.objects.all()
    sp = Product.objects.filter(category=id)
    paginator = Paginator(sp, 10)  # mỗi trang hiển thị 1 đối tượng
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    nums = "a" * page_obj.paginator.num_pages
    return render(
        request,
        "product/detail.html",
        {"sanpham": sp, "loaisp": lsp, "page_obj": page_obj, "nums": nums},
    )


def infor(request, id):
    sp = Product.objects.get(pk=id)
    avg_rating = []
    x = sp.rating()
    for i in range(5):
        if x >= 1:
            avg_rating += [1]
        elif x >= 0.5:
            avg_rating += [2]
        else:
            avg_rating += [3]
        x -= 1
    if request.user.is_authenticated:
        form = Add_review
        if Review.objects.filter(user=request.user, product=sp).count() > 0:
            message = "Khách hàng đã đánh giá sản phẩm này !"
            is_review = False

        else:
            is_review = True
            message = ""
            if request.method == "POST":
                form = Add_review(request.POST)
                if form.is_valid():
                    new_review = Review.objects.create(
                        user=request.user,
                        product=sp,
                        created_time=timezone.now(),
                        rating=request.POST.get("rating"),
                        review=request.POST.get("review"),
                    )
                    return redirect('product:information',id)
                else:
                    print(form.errors.as_data())
        return render(
            request,
            "product/product_detail.html",
            {
                "sp": sp,
                "form": form,
                "is_review": is_review,
                "message": message,
                "avg_rating": avg_rating,
            },
        )
    else:
        login_message = "Vui lòng đăng nhập để có thể đánh giá sản phẩm !"
    return render(
        request,
        "product/product_detail.html",
        {"sp": sp, "login_message": login_message},
    )


def create_product(request):
    pr = Product_create_form()
    if request.method=="POST":
        print(request.POST)
        pr = Product_create_form(request.POST, request.FILES)
        if pr.is_valid():
            pr.save()
            return HttpResponse("Save success")
        else:
            print(pr.errors.as_data())
            return render(
                request, template_name="product/create_product.html", context={"pr": pr}
            )
    return render(request, "product/create_product.html", {"pr": pr})


def list_product(request):
    sp = Product.objects.all()
    s = []
    for i in range(1, sp.count()):
        s += [i]

    return render(request, "product/list_product.html", {"sp": sp, "s": s})


def update_product(request, id):
    sp = Product.objects.get(pk=id)
    pr = Product_create_form(instance=sp)
    if request.method == "POST":
        pr = Product_create_form(request.POST, request.FILES, instance=sp)
        if pr.is_valid():
            pr.save()
            return HttpResponse("Update success")
        else:
            return HttpResponse("Fail")
    return render(
        request,
        "product/create_product.html",
        {
            "sp": sp,
            "pr": pr,
        },
    )


def delete_product(request, id):
    sp = Product.objects.get(pk=id)
    if request.method == "POST":
        sp.delete()
        return redirect("/list_product/")
    return render(request, "product/delete_product.html", {"sp": sp})


# def add_product_information(request,id):
#     form = Add_Product_information()
#     sp=Product.objects.get(pk=id)
#     if request.method == 'POST':
#         form = Add_Product_information(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse ('Add information success')
#         else:
#             print(form.errors.as_data())

#     return render(request, 'product/add_product_information.html',{'form':form})


def list_category(request):
    lsp = Category.objects.all()
    return render(request, "product/list_category.html", {"lsp": lsp})


def create_category(request):
    form = Category_create_form()
    if request.method == "POST":
        form = Category_create_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Success")
        else:
            print(form.errors.as_data())
            return HttpResponse("Fail")
    return render(request, "product/create_category.html", context={"form": form})


def update_category(request, id):
    category = Category.objects.get(pk=id)
    form = Category_create_form(instance=category)
    if request.method == "POST":
        print(request.POST)
        category = Category_create_form(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse("Update success")
        else:
            return HttpResponse("Fail")
    return render(
        request, "product/create_category.html", {"category": category, "form": form}
    )


def delete_category(request, id):
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        category.delete()
        return redirect("/list_category/")
    return render(request, "product/delete_category.html", {"category": category})


def register(request):
    form = Register_form()
    if request.method == "POST":
        form = Register_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    return render(request, "product/register.html", {"form": form})

# def show_question(request):
#     form_question=Question()
#     return render(request,'product/show_question.html',{'form_question1':form_question})

def add_to_cart(request,id):

    
    user = request.user
    if user.is_authenticated:
        product = Product.objects.get(pk=id)
        order, created = Order.objects.get_or_create(user=request.user, status=1)
        orderdetail, created1 = Order_detail.objects.get_or_create(
            order=order, product=product
        )
        if not created1:
            orderdetail.quantity += 1
            orderdetail.save()

        orderDetail = Order_detail.objects.filter(order=order)
        request.session["count_cartitem"] = orderDetail.count()

        return redirect(reverse(viewname="product:information", args=[id]))

    else:
        return redirect("product:login")


def remove_orderDetail(request, id):
    item = Order_detail.objects.get(pk=id)
    item.delete()
    request.session["count_cartitem"] -= 1
    if request.session["count_cartitem"] == 0:
        context = {
            "error_message": "Chưa có sản phẩm trong giỏ hàng.",
            "is_order": False,
        }
        return render(request, "product/cart.html", context)
    return redirect("product:show_cart")


def show_cart(request):
    if (
        Order.objects.filter(user=request.user, status=1).exists() is False
        or Order.objects.filter(order__isnull=True).exists() is True
    ):
        context = {
            "error_message": "Chưa có sản phẩm trong giỏ hàng.",
            "is_order": False,
        }
        return render(request, "product/cart.html", context)
    else:
        order = Order.objects.get(user=request.user, status=1)
        orderDetail = Order_detail.objects.filter(order=order)
        order.quantity = sum(obj.quantity for obj in orderDetail)
        order.total_price = sum(
            obj.product.discount_cost() * obj.quantity for obj in orderDetail
        )
        order.save()

        request.session["count_cartitem"] = orderDetail.count()
        context = {"orderDetail": orderDetail, "order": order, "is_order": True}
        return render(request, "product/cart.html", context)


def checkout(request):
    user = Users.objects.get(pk=request.user.pk)
    order = Order.objects.get(user=user, status=1)
    orderdetail = Order_detail.objects.filter(order=order)

    # address dropdownlist:
    user = request.user
    if user.city == None:
        selectedcity = "Chọn Tỉnh/Thành phố"
        selectedcity_id=""
        print(111,selectedcity,selectedcity_id)
    else:
        selectedcity = user.city
        selectedcity_id=user.city.id
        print(222,selectedcity,selectedcity_id)
    if user.district == None:
        selecteddistrict = "Chọn Quận/Huyện"
        selecteddistrict_id=""
    else:
        selecteddistrict = user.district
        selecteddistrict_id=user.district.id
    if user.ward == None:
        selectedward = "Chọn Phường/Xã"
        selectedward_id=""

    else:
        selectedward = user.ward
        selectedward_id=user.ward.id
    cityId = request.GET.get("city", None)
    districtId = request.GET.get("district", None)
    ward = None
    district = None
    if cityId:
        getCity = City.objects.get(pk=cityId)
        district = District.objects.filter(parent_code=getCity)
        selecteddistrict = "Chọn Quận/Huyện"
    if districtId:
        getDistrict = District.objects.get(pk=districtId)
        ward = Ward.objects.filter(parent_code=getDistrict)
        selectedward = "Chọn Phường/Xã"
    city = City.objects.all()

    form = UserInformationForm(instance=user)

    return render(
        request,
        "product/checkout.html",
        {
            "form": form,
            "orderdetail": orderdetail,
            "order": order,
            "city": city,
            "district": district,
            "ward": ward,
            "selectedcity": selectedcity,
            "selecteddistrict": selecteddistrict,
            "selectedward": selectedward,
            "selectedcity_id": selectedcity_id,
            "selecteddistrict_id": selecteddistrict_id,
            "selectedward_id": selectedward_id,
        },
    )


def minus_quantity(request, id):
    item = Order_detail.objects.get(pk=id)
    if item.quantity == 1:
        item.delete()
    else:
        item.quantity -= 1
        item.save()
    print(item.quantity)
    return redirect("product:show_cart")


def plus_quantity(request, id):
    item = Order_detail.objects.get(pk=id)
    item.quantity += 1
    item.save()
    print(item.quantity)
    return redirect("product:show_cart")


def review_order(request, id):
    order = Order.objects.get(pk=id)
    orderdetail = Order_detail.objects.filter(order=order)

    return render(
        request,
        "product/review_order.html",
        {"order": order, "orderdetail": orderdetail},
    )


def order_list(request):
    user = Users.objects.get(pk=request.user.pk)
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(pk=order_id)

        form = UserInformationForm(
            request.POST, instance=user
        )
        if form.is_valid():
            user.city = City.objects.get(pk=request.POST.get("city"))
            user.district = District.objects.get(pk=request.POST.get("district"))
            user.ward = Ward.objects.get(pk=request.POST.get("ward"))
            form.save()
            order.datetime = timezone.now()
            order.status = 2
            del request.session["count_cartitem"]
        else:
            print(form.errors.as_data())
        order.save()
        user.save()
    # lọc đơn hàng theo thời gian:
    get_startdate = request.GET.get("start_date")
    get_enddate = request.GET.get("end_date")

    if get_startdate and get_enddate:
        startdate = datetime.strptime(get_startdate, "%Y-%m-%d")
        enddate = datetime.strptime(get_enddate, "%Y-%m-%d") + timedelta(days=1)

        # lọc:
        order = Order.objects.filter(datetime__range=(startdate, enddate))
    else:
        order = Order.objects.filter(user=request.user, status=2).order_by("-id")

    return render(
        request,
        "product/order_list.html",
        {"order": order, "get_startdate": get_startdate, "get_enddate": get_enddate},
    )


# trang product
def product_list(request):
    loaisp = Category.objects.all()

    # sắp xếp sản phẩm theo giá:

    sort_by = request.GET.get("sort", "page")

    if sort_by == "l2h":
        sort_sp = Product.objects.order_by("cost")
        # sort_sp = Product.objects.annotate(discountcost=round('cost' * (1 - ('discount' / 100)))).order_by("discountcost")
    elif sort_by == "h2l":
        sort_sp = Product.objects.order_by("-cost")
        # sort_sp = Product.objects.annotate(discountcost=round('cost' * (1 - ('discount' / 100)))).order_by("-discountcost")
    else:
        sort_sp = Product.objects.order_by("-id")
    paginator = Paginator(sort_sp, 10)  # mỗi trang hiển thị 10 đối tượng
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    nums = "a" * page_obj.paginator.num_pages
    # lọc sản phẩm theo giá:
    mincost = request.GET.get("min_cost")
    maxcost = request.GET.get("max_cost")
    if mincost and maxcost:
        product_filtered = Product.objects.filter(cost__range=(mincost, maxcost))
        if product_filtered.count() > 0:
            message = ""
        else:
            message = "Không tìm thấy sản phẩm !"
        return render(
            request,
            "product/product_list.html",
            {
                "loaisp": loaisp,
                "product_filtered": product_filtered,
                "mincost": mincost,
                "maxcost": maxcost,
                "message": message,
            },
        )
    return render(
        request,
        "product/product_list.html",
        {"loaisp": loaisp, "page_obj": page_obj, "nums": nums, "sort_sp": sort_sp},
    )


# hien sản phẩm khi click vào sidebar
def product_select_main(request, id):
    lsp = Category.objects.all()
    lsp_name = Category.objects.get(id=id)
    sp = Product.objects.filter(category=id)
    paginator = Paginator(sp, 5)  # mỗi trang hiển thị 5 đối tượng
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    nums = "a" * page_obj.paginator.num_pages
    # return render(request, 'product/product.html', {})
    return render(
        request,
        "product/product.html",
        {
            "sanpham": sp,
            "loaisp": lsp,
            "lsp_name": lsp_name,
            "page_obj": page_obj,
            "nums": nums,
        },
    )


# dhien ds loai sp sidebar
def product_select(request):
    lsp = Category.objects.all()
    return render(request, "product/product.html", {"loaisp": lsp})


# (modifié)
# trang about us
def about_us(request):
    return render(request, "product/aboutus.html")


# trang contact
def contact(request):
    return render(request, "product/contact.html")


def search(request):
    q=request.GET.get('q')
    a=q.lower()
    query=a.split()
 
   
    queries = [Q(title__icontains=query) for query in query]
    query1 = queries.pop()
    for item in queries:
        query1 |= item
    sp = Product.objects.filter(query1)

    return render(request, "product/search.html", {"sp": sp, "q": q})




# load districts:
def load_districts(request):
    city_id = request.GET.get("city")
    districts = District.objects.filter(parent_code=city_id)
    return render(request, "product/district_option.html", {"districts": districts})


def load_wards(request):

    district_id = request.GET.get("district")
    wards = Ward.objects.filter(parent_code=district_id)
    return render(request, "product/ward_option.html", {"wards": wards})


def profile(request):
    user = Users.objects.get(pk=request.user.pk)

    initial_dict = {
        "email": user.email,
        "username": user.username,
    }
    form_avt = AddAvatar

    # address dropdownlist:
    user = request.user
    if user.city == None:
        selectedcity = "Chọn Tỉnh/Thành phố"
        selectedcity_id = ""
        print(111,selectedcity,selectedcity_id)
    else:
        selectedcity = user.city
        selectedcity_id=user.city.id
        print(222,selectedcity,selectedcity_id)
    if user.district == None:
        selecteddistrict = "Chọn Quận/Huyện"
        selecteddistrict_id=""
    else:
        selecteddistrict = user.district
        selecteddistrict_id=user.district.id
        
    if user.ward == None:
        selectedward = "Chọn Phường/Xã"
        selectedward_id=""
    else:
        selectedward = user.ward
        selectedward_id=user.ward.id
        
    cityId = request.GET.get("city", None)
    districtId = request.GET.get("district", None)
    ward = None
    district = None
    if cityId:
        getCity = City.objects.get(pk=cityId)
        district = District.objects.filter(parent_code=getCity)
        selecteddistrict = "Chọn Quận/Huyện"
    if districtId:
        getDistrict = District.objects.get(pk=districtId)
        ward = Ward.objects.filter(parent_code=getDistrict)
        selectedward = "Chọn Phường/Xã"
    city = City.objects.all()

    form = UpdateUser(instance=user, initial=initial_dict)
    if request.method == "POST":
        form_avt = AddAvatar(request.POST, request.FILES, instance=user)
        if form_avt.is_valid():
            form_avt.save()
    if request.method == "POST" and "city" in request.POST:
        form = UpdateUser(request.POST, instance=user)
        if form.is_valid():
            user.city = City.objects.get(pk=request.POST.get("city"))
            user.district = District.objects.get(pk=request.POST.get("district"))
            user.ward = Ward.objects.get(pk=request.POST.get("ward"))
            user.username = request.POST.get("username")
            user.email = request.POST.get("email")
            form.save()
            return redirect('product:profile')
        else:
            print(form.errors.as_data())
        user.save()
        
    return render(
        request,
        "product/test_profile.html",
        {
            "user": user,
            "form": form,
            "form_avt": form_avt,
            "city": city,
            "district": district,
            "ward": ward,
            "selectedcity": selectedcity,
            "selecteddistrict": selecteddistrict,
            "selectedward": selectedward,
            "selectedcity_id": selectedcity_id,
            "selecteddistrict_id": selecteddistrict_id,
            "selectedward_id": selectedward_id,
        },
    )

# trang contact
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(
                name=form.cleaned_data["name"],
                number=form.cleaned_data["number"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            contact.save()
            return render(request, "product/contact_label.html")
    else:
        form = ContactForm()

    return render(request, "product/contact.html", {"form": form})



from django.contrib import messages

def forgot_password_question(request):
    form = Reset_form(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        answer = request.POST['answer']

        question = request.POST['question']
        print(question)
        try:
            user = Users.objects.get(username=username)
            if user.question and user.answer:
                if question == user.question :  
                
                    if answer == user.answer :
                        # Cung cấp câu trả lời khớp, cho phép người dùng nhập mật khẩu mới
                        return redirect('product:reset_password_question', user_id=user.id)
                    else:
                        # Câu trả lời không khớp
                        messages.error(request, 'Câu trả lời không đúng.')
                else:
                # Câu hỏi không khớp
                    messages.error(request, 'Câu hỏi không đúng.')
            else:
                # Người dùng không có câu hỏi xác thực
                messages.error(request, 'Người dùng không có câu hỏi xác thực.')
        except Users.DoesNotExist:
            # Người dùng không tồn tại
            messages.error(request, 'Người dùng không tồn tại.')
    

    return render(request, 'product/forgot_password_question.html',{'form':form})
from django.contrib.auth.hashers import make_password

def reset_password_question(request,user_id):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user = Users.objects.get(id=user_id)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('product:login')
        else:
            messages.error(request, 'Xác nhận mật khẩu không khớp.')

    return render(request, 'product/reset_password_question.html', {'user_id': user_id})
from django.http import JsonResponse


def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        exists = Users.objects.filter(username=username).exists()
        print(username)
        return JsonResponse({'exists': exists})

def test1(request):
    user = request.user
    if user.city == None:
        selectedcity = "Chọn Tỉnh/Thành phố"
    else:
        selectedcity = user.city
    if user.district == None:
        selecteddistrict = "Chọn Quận/Huyện"
    else:
        selecteddistrict = user.district
    if user.ward == None:
        selectedward = "Chọn Phường/Xã"
    else:
        selectedward = user.ward
    cityId = request.GET.get("city", None)
    districtId = request.GET.get("district", None)
    ward = None
    district = None
    if cityId:
        getCity = City.objects.get(pk=cityId)
        district = District.objects.filter(parent_code=getCity)
        selecteddistrict = "Chọn Quận/Huyện"
    if districtId:
        getDistrict = District.objects.get(pk=districtId)
        ward = Ward.objects.filter(parent_code=getDistrict)
        selectedward = "Chọn Phường/Xã"
    city = City.objects.all()
    return render(
        request,
        "product/test1.html",
        {
            "city": city,
            "district": district,
            "ward": ward,
            "selectedcity": selectedcity,
            "selecteddistrict": selecteddistrict,
            "selectedward": selectedward,
        },
    )
