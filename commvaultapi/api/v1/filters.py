import django_filters
from api.v1.models import BackupRequest

from django_filters.filters import DateFilter

class WithinDateFilter(DateFilter):

    def filter(self, qs, value):
        from datetime import timedelta

        if value:
            filter_lookups = {
                "%s__range" % (self.name, ): (
                    value,
                    value + timedelta(days=1),
                ),
            }

            qs = qs.filter(**filter_lookups)

        return qs

class BackupRequestFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type="icontains")
    location = django_filters.CharFilter(name="location", lookup_type="exact")
    created = WithinDateFilter(name="created")

    class Meta:
        model = BackupRequest 
        fields = ['name', 'location', 'created']
