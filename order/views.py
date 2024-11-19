from datetime import date, timedelta

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import BronStadion, TASDIQLANGAN
from order.serializers import BronStadionSerializer, BronStadionPostSerializer
from stadion.models import Stadion


class BronStadionAPIView(APIView):
    queryset = BronStadion.objects.all()
    # serializer_class = BronStadionPostSerializer
    http_method_names = ['get', 'post']

    def get(self, request, id, *args, **kwargs):
        just = {}
        just1 = {}
        current_date = date.today()
        try:
            stadion = Stadion.objects.get(id=id)
            bronstadions = stadion.stadion_bronorders.filter(date__gte=current_date, is_active=True, status=TASDIQLANGAN)
            for i in range(7):
                brons = bronstadions.filter(date=current_date)
                serializer = BronStadionSerializer(brons, many=True).data
                just[f"{current_date}"] = serializer
                current_date = current_date + timedelta(days=1)
            just1["start_time"] = stadion.start_time
            just1["end_time"] = stadion.end_time
            just1["price"] = stadion.price
            data = {
                'stadion': just1,
                'brons': just
            }
            return Response(data)

        except Stadion.DoesNotExist:
            data = {
                'status': False,
                'message': "Stadion_topilmadi!!!"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {
                'status': False,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BronStadionPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)



