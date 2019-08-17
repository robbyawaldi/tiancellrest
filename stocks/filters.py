from stocks.models import Sale
from django_filters import FilterSet, DateRangeFilter, DateFilter


class SaleFilter(FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr=('gt'),)
    end_date = DateFilter(field_name='date', lookup_expr=('lt'))
    date_range = DateRangeFilter(field_name='date')

    class Meta:
        model = Sale
        fields = []
