from rest_framework import viewsets
from .models import TechNews
from .serializers import TechNewsSerializer, NewsSourcesSerializer
from rest_framework.exceptions import MethodNotAllowed

class TechNewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TechNews.objects.all()
    serializer_class = TechNewsSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('?')
    
    
    # def create(self, request, *args, **kwargs):
    #     raise MethodNotAllowed('POST')
    
    # def update(self, request, *args, **kwargs):
    #     raise MethodNotAllowed('PUT')
    
    # def partial_update(self, request, *args, **kwargs):
    #     raise MethodNotAllowed('PATCH')
    
    # def destroy(self, request, *args, **kwargs):
    #     raise MethodNotAllowed('DELETE')
    
class NewsSourcesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TechNews.objects.all()
    serializer_class = NewsSourcesSerializer
    