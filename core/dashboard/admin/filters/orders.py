import django_filters
from order.models import OrderModel

class AdminOrderFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='id', lookup_expr='contains')
    status = django_filters.NumberFilter(field_name='status')

    class Meta:
        model = OrderModel
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
            'price': 'total_price',
            '-price': '-total_price',
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None



