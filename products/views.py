import os

from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect

from djangoProject import settings
from products.forms import ProductCreateForms
from products.models import Products
from products import forms
from products.constans import PAGINATION_LIMIT

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
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)

        data = {
            'products': products,
            'user': request.user,
            'page': range(1, max_page + 1)

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
