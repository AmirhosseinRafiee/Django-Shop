import django_filters
from .models import ProductModel

class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    price = django_filters.RangeFilter(field_name='discounted_price')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')

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
            '-price': '-discounted_price'
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None
