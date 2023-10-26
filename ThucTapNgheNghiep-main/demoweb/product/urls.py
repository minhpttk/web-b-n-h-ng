from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


from django.contrib.auth.views  import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView,PasswordResetView

app_name = "product"
urlpatterns = [
     path('',views.index, name="index"),
     path('<int:id>/',views.detail, name="detail"),
     path('information/<int:id>/',views.infor, name="information"),
     

     path('create_product/',views.create_product,name='create_product'),
     path('list_product/',views.list_product,name='list_product'),
     path('update_product/<int:id>/',views.update_product,name='update_product'),
     path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
     # path('add_product_information/<int:id>/',views.add_product_information,name='add_product_information'),

     path('list_category/',views.list_category,name='list_category'),
     path('create_category/',views.create_category,name='create_category'),
     path('update_category/<int:id>/',views.update_category,name='update_category'),
     path('delete_category/<int:id>/',views.delete_category,name='delete_category'),

     path('register/',views.register,name='register'),
     path( 'login/',auth_views.LoginView.as_view(template_name="product/login.html"), name="login"),
     path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),

     path('add_to_cart/<int:id>/',views.add_to_cart, name="add_to_cart"),
     path('remove_orderDetail/<int:id>/',views.remove_orderDetail, name="remove_orderDetail" ),
     path('minus_quantity/<int:id>/',views.minus_quantity, name="minus_quantity" ),
     path('plus_quantity/<int:id>/',views.plus_quantity, name="plus_quantity" ),
     path('show_cart/',views.show_cart, name="show_cart"),
     path('checkout/',views.checkout, name="checkout"),
     path('review_order/<int:id>/',views.review_order, name="review_order"),
     path('order_list/',views.order_list, name="order_list"),
     path('product/',views.product_select, name="product"),
     path('product/<int:id>/',views.product_select_main, name="product_select_main"),
     path('about_us/',views.about_us, name="about_us"),
     path('contact/',views.contact, name="contact"),
     path('search/',views.search,name="search"),
     path('password_change/',PasswordChangeView.as_view(
          template_name='product/password.html',
          success_url= reverse_lazy('product:password_change_done'),

          ),name="password_change"),
     path('password_change/done/',PasswordChangeDoneView.as_view(template_name='product/passwordone.html'),name="password_change_done"),
     path('load-wards/',views.load_wards,name="load-wards"),
     path('load-districts/',views.load_districts,name="load-districts"),

     path('profile/',views.profile,name="profile"),
    
     path('product_list/',views.product_list,name='product_list'),
     path('contact/', views.contact, name='contact'),

    

     path('forgot_password_question/', views.forgot_password_question, name='forgot_password_question'),
     path('reset_password_question/<int:user_id>/', views.reset_password_question, name='reset_password_question'),

]
