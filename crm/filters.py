import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    nameIcontains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    emailIcontains = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    createdAtGte = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    createdAtLte = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    phonePattern = django_filters.CharFilter(method="filter_phone_pattern")

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = []

class ProductFilter(django_filters.FilterSet):
    nameIcontains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    priceGte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    priceLte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stockGte = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stockLte = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    lowStock = django_filters.BooleanFilter(method="filter_low_stock")

    def filter_low_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__lt=10)
        return queryset

    class Meta:
        model = Product
        fields = []

class OrderFilter(django_filters.FilterSet):
    totalAmountGte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    totalAmountLte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")
    orderDateGte = django_filters.DateFilter(field_name="order_date", lookup_expr="gte")
    orderDateLte = django_filters.DateFilter(field_name="order_date", lookup_expr="lte")
    customerName = django_filters.CharFilter(method="filter_customer_name")
    productName = django_filters.CharFilter(method="filter_product_name")
    productId = django_filters.NumberFilter(method="filter_product_id")

    def filter_customer_name(self, queryset, name, value):
        return queryset.filter(customer__name__icontains=value)

    def filter_product_name(self, queryset, name, value):
        return queryset.filter(products__name__icontains=value).distinct()

    def filter_product_id(self, queryset, name, value):
        return queryset.filter(products__id=value).distinct()

    class Meta:
        model = Order
        fields = []
