from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, Users, Order_detail
from product.models import Product
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
# Create your views here.
def revenue(request):
   
    

    get_startdate = request.GET.get("start_date")
    get_enddate = request.GET.get("end_date")

    if get_startdate and get_enddate:
        startdate = datetime.strptime(get_startdate, "%Y-%m-%d")
        enddate = datetime.strptime(get_enddate, "%Y-%m-%d") + timedelta(days=1)

        # lọc:
        order = Order.objects.filter(datetime__range=(startdate, enddate))
    else:
        order = Order.objects.filter(status=2).order_by("-id")

    sumquantity = sum(obj.quantity for obj in order)
    sumprice = sum(obj.total_price for obj in order)
    sumorder = order.count()
    sumorder = order.count()
    return render(request, 'order/revenue.html',{'sumprice':sumprice,'sumquantity':sumquantity, 'order':order, "get_startdate": get_startdate, "get_enddate": get_enddate,'sumorder':sumorder})


# def bestseller(request):
#     pass

def statistics(request):
    order = Order.objects.filter(status=2)
    inventory = Product.objects.all()
    pr_sold = sum(obj.quantity for obj in order)
    pr_inventory = sum(obj.quantity for obj in inventory)
    x = round((pr_sold/pr_inventory)*100,2)
    y = 100 - x

    # pie chart:
    labels = ['Tỉ lệ hàng đã bán', 'Tỉ lệ hàng tồn kho']
    data = [x,y]

    #bar chart:
    labels_bar =[]
    data_bar = []
    top5 = Order_detail.objects.values('product__title').annotate(total_sold = Sum('quantity')).order_by("-total_sold")[:5]
    for i in top5:
        labels_bar.append(i['product__title'])
        data_bar.append(i['total_sold'])
    # labels_bar=top5
    
    return render (request, 'order/statistics.html',{'x':x,'y':y,'pr_sold':pr_sold,'pr_inventory':pr_inventory,'labels': labels,'data': data,'labels_bar': labels_bar,'data_bar': data_bar,})



