from rest_framework import generics
from .models import Viloyat
from .serializerz import ViloyatSerializer


class ViloyatListAPIView(generics.ListAPIView):
    queryset = Viloyat.objects.prefetch_related('tumanlar').all()
    serializer_class = ViloyatSerializer
