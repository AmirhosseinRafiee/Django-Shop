import django_filters
from shop.models import ProductModel
from order.models import CuponModel

class AdminProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='iexact')

    class Meta:
        model = ProductModel
        fields = []

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        ordering = self._get_ordering()
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset

    def _get_ordering(self):
        ordering_choices = {
            'date': 'created_date',
            '-date': '-created_date',
            'price': 'price',
            '-price': '-price',
            '-discount_percent': '-discount_percent',
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None


class AdminCouponFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = CuponModel
        fields = []

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        ordering = self._get_ordering()
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset

    def _get_ordering(self):
        ordering_choices = {
            'date': 'created_date',
            '-date': '-created_date',
            '-discount_percent': '-discount_percent',
            'discount_percent': 'discount_percent',
            '-max_discount_amount': '-max_discount_amount',
            'max_limit_usage': 'max_limit_usage',
            '-max_limit_usage': '-max_limit_usage',
            'num_users_used': 'num_users_used',
            '-num_users_used': '-num_users_used',
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None
