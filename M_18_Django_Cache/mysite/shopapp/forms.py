from django import forms
from .models import Product, Order


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "delivery_address", "promocode", "products"


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
