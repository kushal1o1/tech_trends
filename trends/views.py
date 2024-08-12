from rest_framework import viewsets
from .models import Trend
from .serializers import TrendSerializer

class TrendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trend.objects.all().order_by('-timestamp')[:10]
    serializer_class = TrendSerializer
