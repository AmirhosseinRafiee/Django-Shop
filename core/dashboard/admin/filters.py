import django_filters
from shop.models import ProductModel

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
            'price': 'discounted_price',
            '-price': '-discounted_price',
            '-discount_percent': '-discount_percent',
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None
