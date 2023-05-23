import os

from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect

from djangoProject import settings
from products.forms import ProductCreateForms
from products.models import Products
from products import forms

from datetime import date

current_date = date.today()
print(current_date)


# Create your views here.

def main_page_view(request):
    if request.method == "GET":
        return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == "GET":
        products = Products.objects.all()

        data = {
            'products': products

        }

        return render(request, 'products/products.html', context=data)


def products_detail_view(request, id_):
    if request.method == 'GET':
        products = Products.objects.get(id=id_)

        context = {
            'products': products,
            'comments': products.comments_set.all()
        }

        return render(request, 'products/detail.html', context=context)


def products_create_vies(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForms
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'PRODUCT':
        data, files = request.POST, request.FILES
        form = ProductCreateForms(data, files)

        if form.is_valid():
            Products.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate')
            )

            return redirect('/products/')

        return render(request, 'products/create.html', context={
            'form': form
        })


class FormValidator:

    def __init__(self, fields: dict = None, non_reqiured: list = None):
        self.fields = fields
        self.non_required = non_reqiured

    def is_valid(self):
        """
        this method need for check fields
        """
        pass

    def validated_data(self) -> dict:
        """
        return dict of validated data
        ATTENTION: call this method after call is_valid()
        """
        pass
