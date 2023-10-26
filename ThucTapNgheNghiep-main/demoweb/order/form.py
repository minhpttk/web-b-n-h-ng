from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Users, Order_detail


class paymentmenthods_form(forms.Form):
    paymentmenthods_field = forms.ChoiceField(
        choices=Order.paymentmenthods_choices, widget=forms.Select(), required=True
    )
