"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.п.
"""
import logging
from django.core.cache import cache
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed
from django.views import View
from django.views.generic import ListView, \
    DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    UserPassesTestMixin

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from .serializers import ProductSerializer, OrderSerializer

from ..mysite.settings import ALLOWED_HOSTS


log = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,

    ]
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class OrderViewSet(ModelViewSet):
    """
    Набор представлений для действий над Order.

    Полный CRUD для сущностей заказа.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,

    ]
    filterset_fields = [
        "user",
        "promocode",
    ]
    ordering_fields = [
        "pk",
        "user",
        "promocode",
    ]


def shop_index(request: HttpRequest):
    """Функция отображения главной страницы интернет-магазина."""
    urls = [
        "http://195.80.51.79:8000/admin/",
        "http://195.80.51.79:8000/shop/groups/",
        "http://195.80.51.79:8000/shop/order/",
        "http://195.80.51.79:8000/shop/products/",
        "http://195.80.51.79:8000/shop/products/create/",
        "http://195.80.51.79:8000/shop/order/create/",
        "http://195.80.51.79:8000/accounts/login/",
        "http://195.80.51.79:8000/accounts/profiles/",
        "http://195.80.51.79:8000/accounts/about-me/",
        "http://195.80.51.79:8000/api/",
        "http://195.80.51.79:8000/ru/api/products/",
        "http://195.80.51.79:8000/ru/api/orders/",
        "http://195.80.51.79:8000/api/schema/swagger/",
        "http://195.80.51.79:8000/api/schema/redoc/",
        "http://195.80.51.79:8000/blogapp/article/",
        "http://195.80.51.79:8000/sitemap.xml",
        "http://195.80.51.79:8000/ru/shop/products/latest/feed/",
        "http://195.80.51.79:8000/ru/users/1/orders/",
        "http://195.80.51.79:8000/ru/users/1/orders/export/",

    ]
    context = {
        "urls": urls,
    }
    log.debug("Products for shop index: %s", urls)
    log.info("Rendering shop index")
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    """Функция вывода групп."""
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


class ProductsDetailsView(DetailView):
    """Детальный вывод информации о товаре."""

    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    """Вывод списка товаров."""

    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Создание нового товара."""

    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "description", "price", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        """Функция проверки разрешения на создание товара."""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """Изменение описания товара."""

    def test_func(self):
        """Функция проверки разрешения на обновление товара."""
        if self.request.user.is_superuser\
                or self.request.user.id == self.get_object().created_by_id\
                or self.request.user.has_perm("shopapp.change_product"):
            return True
        else:
            return False

    model = Product
    fields = "name", "description", "price", "discount", "preview"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        """Функция автоматического возвращения на страницу товара."""
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )


class ProductDeleteView(DeleteView):
    """Архивация товара."""

    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        """Функция архивирующая товар."""
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save(update_fields=['archived'])
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    """Вывод списка всех заказов."""

    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderDetailView(DetailView):
    """Вывод детальной информации о заказе."""

    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderCreateView(CreateView):
    """Создание нового заказа."""

    model = Order
    fields = "user", "delivery_address", "promocode", "products"
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    """Внесение изменений в существующий заказ."""

    model = Order
    fields = "user", "delivery_address", "promocode", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        """Функция автоматического возвращения на страницу заказа."""
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    """Удаление заказа."""

    model = Order
    success_url = reverse_lazy("shopapp:order_list")


class OdersDataExportView(UserPassesTestMixin, View):
    """Экспорт заказов в json формате."""

    def test_func(self):
        """Проверка прав пользователя."""
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        """Функция GET запроса."""
        orders = Order.objects.select_related(
            "user").prefetch_related("products").order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        elem = orders_data[0]
        name = elem['pk']
        print("pk:", name)
        return JsonResponse({"orders": orders_data})


class LatestProductsFeed(Feed):
    title = "df"
    description = "dsgd"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects.filter(created_at__isnull=False).order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class UserOrdersListView(ListView):
    model = Order
    template_name = "shopapp/user_orders_list.html"

    def get_queryset(self):
        self.owner = get_object_or_404(User.objects.all(), pk=self.kwargs['user_id'])
        return super().get_queryset().filter(user=self.owner).prefetch_related("products")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context


class UserOrdersDataExportView(APIView):

    def get(self, request: Request, **kwargs) -> Response:
        """Функция GET запроса."""
        cache_key = f"user_{self.kwargs['user_id']}_orders_export"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            user = get_object_or_404(User.objects.all(), pk=self.kwargs['user_id'])
            orders = Order.objects.order_by("pk").filter(user=user).prefetch_related("products")
            orders_data = [
                {
                    "pk": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "user": order.user.id,
                    "products": [product.name for product in order.products.all()]
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 300)
        return Response({"orders": orders_data})

