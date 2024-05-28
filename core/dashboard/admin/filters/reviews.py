from django.db.models import Q
import django_filters
from review.models import ReviewProductModel, ReviewStatusType


class AdminReviewFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_q')
    status = django_filters.ChoiceFilter(choices=ReviewStatusType.choices)

    class Meta:
        model = ReviewProductModel
        fields = []

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        ordering = self._get_ordering()
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset


    def filter_by_q(self, queryset, name, value):
        return queryset.filter(
            Q(product__title__icontains=value) |
            Q(user__profile__last_name__icontains=value)
        )

    def _get_ordering(self):
        ordering_choices = {
            'date': 'created_date',
            '-date': '-created_date',
            'rate': 'rate',
            '-rate': '-rate',
        }
        ordering = self.data.get('order_by', None)
        if ordering:
            for k, v in ordering_choices.items():
                if ordering == k:
                    return v
        return None
