from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path('revenue/',views.revenue, name="revenue"),
    path('statistics/',views.statistics, name="statistics"),
   
    
]
