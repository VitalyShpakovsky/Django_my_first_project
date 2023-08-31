from django.urls import path, include


from rest_framework.routers import DefaultRouter

from .views import shop_index, \
    groups_list, \
    ProductsListView, \
    ProductsDetailsView, \
    ProductCreateView, \
    OrderCreateView, \
    ProductUpdateView, \
    ProductDeleteView, \
    OrderListView,\
    OrderDetailView,\
    OrderUpdateView,\
    OrderDeleteView, \
    OdersDataExportView, \
    ProductViewSet, \
    OrderViewSet, \
    LatestProductsFeed, \
    UserOrdersListView, \
    UserOrdersDataExportView

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)


urlpatterns = [
    path("", shop_index, name="index"),
    path("api/", include(routers.urls)),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),
    path("products/<int:pk>/", ProductsDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_archived"),
    path("order/", OrderListView.as_view(), name="order_list"),
    path("order/export/", OdersDataExportView.as_view(), name="export_orders"),
    path("order/create/", OrderCreateView.as_view(), name="create_order"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("order/<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("users/<int:user_id>/orders/export/", UserOrdersDataExportView.as_view(), name="export_user_orders"),


]