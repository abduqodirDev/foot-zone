import datetime
from datetime import date, timedelta

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import BronStadion, TASDIQLANGAN
from order.serializers import BronStadionSerializer, BronStadionPostSerializer, MyBronstadionSerializer, \
    MyStadionBronSerializer, VerifyBronSerializer
from stadion.models import Stadion


class BronStadionAPIView(APIView):
    queryset = BronStadion.objects.all()
    serializer_class = BronStadionPostSerializer
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

    def post(self, request, id):
        data = request.data
        serializer = BronStadionPostSerializer(data=data)
        try:
            if not serializer.is_valid():
                context = {
                    'status': False,
                    'message': 'Invalid_data'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            for dict in data['brons']:
                if BronStadion.ActiveBronStadion.filter(date=dict['date'], time=str(dict['bron'])).exists():
                    content = {
                        "status": False,
                        "message": "Bu vaqtda stadion bron qilingan!!!"
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            stadion = Stadion.objects.get(id=id)
            bron_id = []
            for dict in data['brons']:
                time = dict['bron']
                date = dict['date']
                bron = BronStadion.objects.create(stadion=stadion, time=time, date=date)
                bron_id.append(bron.id)

            context = {
                "status": True,
                "message": "Bron stadions was saved successfully",
                "bron_id": bron_id
            }

            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion topilmadi!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                "status": False,
                "message": str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class MyBronStadion(ListAPIView):
    serializer_class = MyBronstadionSerializer
    queryset = BronStadion.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class MyStadionBronListAPIView(ListAPIView):
    serializer_class = MyStadionBronSerializer
    queryset = BronStadion.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        current_time = date.today()
        stadion = Stadion.objects.filter(user=self.request.user).last()
        return self.queryset.filter(stadion=stadion, date__gte=current_time-datetime.timedelta(days=7), user__isnull=False)


class VerifyBronAPIView(APIView):
    serializer_class = VerifyBronSerializer
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        context_data = {
            "status": False,
            "message": "Invalid_data"
        }
        serializer = VerifyBronSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(context_data, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data
            bron_id = data.get('bron_id', None)
            is_active = data.get('is_active', None)
            bron = BronStadion.objects.get(id=bron_id)
            bron.is_active = is_active
            bron.save()
            context = {
                'status': True,
                'is_active':bron.is_active,
                'bron_id': bron.id
            }
            return Response(context)

        except BronStadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Bron stadion topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionBronDiagrammaAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            context = {}
            stadion = Stadion.objects.get(user=user)
            current_time = date.today()
            bronstadion = BronStadion.objects.filter(stadion=stadion)
            for i in range(7):
                time = current_time-timedelta(days=i)
                just = bronstadion.filter(date=time)
                if just:
                    context[f"{time}"] = len(just)

            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Bu userda stadion mavjud emas'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
