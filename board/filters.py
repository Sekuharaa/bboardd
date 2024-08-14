from django.forms import DateInput
from django_filters import FilterSet, CharFilter
from .models import Comment, Ad
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AdFilter(FilterSet):

    class Meta:
        model = Comment
        fields = {
            'ad'
        }

    def __init__(self, *args, **kwargs):
        super(AdFilter, self).__init__(*args, **kwargs)
        self.filters['ad'].queryset = Ad.objects.filter(user__id=kwargs['request'])